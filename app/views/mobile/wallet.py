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

from app.helpers import (
    render_template,
    log_info,
    toint,
    url_push_query
)
from app.helpers.user import (
    check_login,
    get_uid
)

from app.services.api.funds import FundsStaticMethodsService

from app.models.order import Order
from app.models.funds import (
    Funds,
    FundsDetail
)

wallet = Blueprint('mobile.wallet', __name__)


@wallet.route('/')
def root():
    """手机站 - 我的钱包"""

    if not check_login():
        session['weixin_login_url'] = request.headers['Referer']
        return redirect(url_for('api.weixin.login'))
    uid = get_uid()

    funds      = Funds.query.filter(Funds.uid == uid).first()
    details    = FundsStaticMethodsService.details(uid, {})
    log_info('details:%s' % details)
    paging_url = url_for('mobile.wallet.paging', **request.args)

    return render_template('mobile/wallet/index.html.j2', funds=funds, details=details, paging_url=paging_url)


@wallet.route('/paging')
def paging():
    """加载分页"""

    if not check_login():
        session['weixin_login_url'] = request.headers['Referer']
        return redirect(url_for('api.weixin.login'))
    uid = get_uid()

    details = FundsStaticMethodsService.details(uid, request.args.to_dict())

    return render_template('mobile/wallet/paging.html.j2', details=details)


@wallet.route('/recharge')
def recharge():
    """手机站 - 钱包充值"""

    if not check_login():
        session['weixin_login_url'] = request.headers['Referer']
        return redirect(url_for('api.weixin.login'))
    uid = get_uid()

    order_id        = toint(request.args.get('order_id', '0'))
    is_weixin       = toint(request.args.get('is_weixin', '0'))
    recharge_amount = 0
    redirect_url    = url_push_query(request.url, 'is_weixin=1')

    # 订单付款
    if order_id > 0:
        # 检查
        order = Order.query.filter(Order.order_id == order_id).filter(Order.uid == uid).first()
        if not order:
            return redirect(request.headers['Referer'])
        
        recharge_amount = order.pay_amount

    data = {'order_id':order_id, 'recharge_amount':recharge_amount, 'is_weixin':is_weixin, 'redirect_url':redirect_url}
    return render_template('mobile/wallet/recharge.html.j2', **data)


@wallet.route('/detail/<int:fd_id>')
def detail(fd_id):
    """手机站 - 交易明细详情"""

    if not check_login():
        session['weixin_login_url'] = request.headers['Referer']
        return redirect(url_for('api.weixin.login'))
    uid = get_uid()

    detail = FundsDetail.query.filter(FundsDetail.fd_id == fd_id).filter(FundsDetail.uid == uid).first()
    if not detail:
        return redirect(request.headers['Referer'])

    return render_template('mobile/wallet/detail.html.j2', detail=detail)
