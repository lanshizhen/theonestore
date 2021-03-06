# -*- coding: utf-8 -*-
"""
    theonestore
    https://github.com/kapokcloud-inc/theonestore
    ~~~~~~~~~~~
    
    :copyright: © 2018 by the Kapokcloud Inc.
    :license: BSD, see LICENSE for more details.
"""

from flask import (
    request,
    session,
    Blueprint,
    redirect,
    url_for
)
from flask_babel import gettext as _
from flask_sqlalchemy import Pagination

from app.database import db

from app.helpers import (
    render_template,
    log_info,
    log_error,
    toint,
    get_count
)
from app.helpers.user import (
    check_login,
    get_uid
)

from app.services.api.order import (
    OrderStaticMethodsService,
    OrderCancelService,
    OrderDeliverService
)
from app.exception import OrderException
from app.forms.api.comment import CommentOrderGoodsForm

from app.models.comment import Comment
from app.models.shipping import Shipping
from app.models.aftersales import Aftersales
from app.models.item import Goods
from app.models.order import (
    Order,
    OrderAddress,
    OrderGoods
)


order = Blueprint('pc.order', __name__)


@order.route('/')
def index():
    """订单列表页"""

    if not check_login():
        session['weixin_login_url'] = request.url
        return redirect(url_for('api.weixin.login_qrcode'))
    uid = get_uid()

    data = OrderStaticMethodsService.orders(uid, request.args.to_dict(), True)

    # pc端订单列表支持，支付、详情、售后3个指令，其余指令排除，即排除[2,3,4,5,6]
    if data.get("orders"):
        excel_code = [2, 3, 4, 5, 6]
        action_code = data.get('codes')
        for order in data.get("orders"):
            temp = set(action_code[order.order_id])-set(excel_code)
            action_code[order.order_id] = list(temp)

    data['tab_status'] = request.args.get('tab_status', '0')

    return render_template('pc/order/index.html.j2', **data)


@order.route('/<int:order_id>')
def detail(order_id):
    """订单详情"""

    if not check_login():
        session['weixin_login_url'] = request.url
        return redirect(url_for('api.weixin.login_qrcode'))
    uid = get_uid()

    data = OrderStaticMethodsService.detail_page(order_id, uid)
    # pc端订单详情不支持再次购买，排除掉指令[5]
    data['code'] = list(set(data['code'])-set([5]))

    return render_template('pc/order/detail.html.j2', **data)


@order.route('/cancel')
def cancel():
    """取消订单"""

    if not check_login():
        session['weixin_login_url'] = request.url
        return redirect(url_for('api.weixin.login_qrcode'))
    uid = get_uid()

    args = request.args
    order_id = toint(args.get('order_id', 0))
    cancel_desc = args.get('cancel_desc', '').strip()

    if order_id <= 0:
        return ''

    ocs = OrderCancelService(order_id, uid, cancel_desc)
    try:
        ocs.cancel()
    except OrderException as e:
        msg = u'%s' % e.msg
        log_error(msg)
        return ''

    text, code = OrderStaticMethodsService.order_status_text_and_action_code(
        ocs.order)

    return render_template(
        'pc/order/order.html.j2',
        order=ocs.order,
        text=text,
        code=code)


@order.route('/deliver')
def deliver():
    """确认收货"""

    if not check_login():
        session['weixin_login_url'] = request.url
        return redirect(url_for('api.weixin.login_qrcode'))
    uid = get_uid()

    args = request.args
    order_id = toint(args.get('order_id', 0))

    if order_id <= 0:
        return ''

    ods = OrderDeliverService(order_id, uid)
    try:
        ods.deliver()
    except OrderException as e:
        msg = u'%s' % e.msg
        log_error(msg)
        return ''

    text, code = OrderStaticMethodsService.order_status_text_and_action_code(
        ods.order)

    return render_template(
        'pc/order/order.html.j2',
        order=ods.order,
        text=text,
        code=code)


@order.route('/create-comment/<int:og_id>')
def create_comment(og_id):
    """pc站 - 发表评价"""

    if not check_login():
        session['weixin_login_url'] = request.url
        return redirect(url_for('api.weixin.login_qrcode'))
    uid = get_uid()

    order_goods = OrderGoods.query.get(og_id)
    order = Order.query.filter(Order.order_id == order_goods.order_id).filter(
        Order.uid == uid).first()
    if not order:
        return redirect(url_for('pc.index.pagenotfound'))

    if order_goods.comment_id > 0:
        return redirect(url_for('pc.index.pagenotfound'))

    wtf_form = CommentOrderGoodsForm()

    return render_template('pc/order/create_comment.html.j2', order_goods=order_goods, wtf_form=wtf_form)


@order.route('/comment')
def comment(is_pagination=True):
    """pc站 - 评价中心"""

    if not check_login():
        session['weixin_login_url'] = request.url
        return redirect(url_for('api.weixin.login_qrcode'))
    uid = get_uid()

    data = OrderStaticMethodsService.order_comments(
        uid, request.args.to_dict(), True)

    return render_template('pc/order/comment.html.j2', **data)


@order.route('/comment/<int:og_id>')
def comment_detail(og_id):
    """pc站 - 查看评价"""

    if not check_login():
        session['weixin_login_url'] = request.url
        return redirect(url_for('api.weixin.login_qrcode'))
    uid = get_uid()

    order_goods = OrderGoods.query.get(og_id)
    good = Goods.query.get(order_goods.goods_id)
    comment = Comment.query.filter(
        Comment.comment_id == order_goods.comment_id).filter(Comment.uid == uid).first()

    if not comment:
        return redirect(url_for('pc.index.pagenotfound'))

    return render_template('pc/order/comment_detail.html.j2', order_goods=order_goods, comment=comment, good=good)
