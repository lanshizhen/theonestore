# -*- coding: utf-8 -*-
"""
    theonestore
    https://github.com/kapokcloud-inc/theonestore
    ~~~~~~~~~~~
    
    :copyright: © 2018 by the Kapokcloud Inc.
    :license: BSD, see LICENSE for more details.
"""
from flask_babel import gettext as _
from flask_wtf.file import (
    FileField, 
    FileAllowed, 
    FileRequired
)
from flask_uploads import UploadSet, TEXT

from wtforms import (
    IntegerField,
    StringField,
    DecimalField,
    SelectField,
    TextAreaField
)
from wtforms.validators import (
    Required,
    Length,
    EqualTo,
    NumberRange
)

from app.forms import Form

class WeixinMpForm(Form):
    appid = StringField(label=_(u'开发者(AppID)'),
                    description=_(u'如：wxf7337ac7caaac670<br>请查看您的公众号 “开发->基本设置” '),
                    validators=[Required(message=_(u'请填写开发者(AppID)'))])

    secret = StringField(label=_(u'开发者密码(AppSecret)'),
                    description=_(u'如：b1946ac92492d2347c6235b4d2611184<br>请查看您的公众号 “开发->基本设置”'),
                    validators=[Required(message=_(u'请填写开发者密码(AppSecret)'))])

    mp_verify = FileField(_(u'公众号校验文件'), 
                    description=_(u'如：MP_verify_zprDbONIS74q99hQ.txt<br>请前往您的公众号 “设置 -> 公众号设置 -> 功能设置 -> 业务域名” 下载校验文件'), 
                    validators=[
                        FileRequired(_(u'文件未上传')), 
                        FileAllowed(UploadSet('text', TEXT), message=_(u'只允许上传txt文本文件'))
                ])


class WeixinPayForm(Form):
    mch_id = StringField(label=_(u'微信支付商户号'),
                    description=_(u'如：1400590602，请查看您的商户平台 "帐户中心 -> 帐户设置 -> 商户信息 -> 基本帐户信息"'),
                    validators=[Required(message=_(u'请填写微信支付商户号'))])
    
    partner_key = StringField(label=_(u'微信支付商户密钥'),
                    description=_(u'请查看您的商户平台 "帐户中心 -> 帐户设置 -> API安全 -> API密钥"'),
                    validators=[Required(message=_(u'请填写微信支付商户密钥'))])
    



class SmsYunpianForm(Form):
    ak = StringField(_name='ak', 
                    label=_(u'APIKEY'),
                    validators=[Required(message=_(u'请填写APIKEY'))])
    app_name = StringField(_name='app_name', 
                    label=_(u'短信前辍'),
                    description=_(u'例如：【一店】，则填写 一店，不需填写方括号'),
                    validators=[Required(message=_(u'请填写前缀'))])


class SmsAlismsForm(Form):
    access_key_id = StringField(_name='access_key_id', 
                    label=_(u'AccessKey ID'),
                    description=_(u'<a target="_blank" href="https://help.aliyun.com/knowledge_detail/38738.html">AccessKey ID和AccessKey Secret 请见阿里云文档</a>'), 
                    validators=[Required(message=_(u'请填写ACCESSKEY'))])

    access_key_secret = StringField(_name='access_key_secret', 
                    label=_(u'AccessKey Secret'),
                    validators=[Required(message=_(u'请填写AccessKey Secret'))])

    app_name = StringField(_name='app_name', 
                    label=_(u'短信前辍'), 
                    description=_(u'例如：【一店】，则填写 一店，不需填写方括号'), 
                    validators=[Required(message=_(u'请填写短信前缀'))])


class StorageQiniuForm(Form):
    access_key = StringField('access_key', 
                    description=_(u'<a target="_blank" href="https://developer.qiniu.com/kodo/kb/1334/the-access-key-secret-key-encryption-key-safe-use-instructions">详情请见七牛文档</a>'), 
                    validators=[Required(message=_(u'请填写ACCESS KEY'))])

    secret_key = StringField('secret_key', 
                    validators=[Required(message=_(u'请填写SECRET KEY'))])

    bucket_name = StringField(_name='bucket_name', 
                    label=_(u'存储空间'), 
                    validators=[Required(message=_(u'请填写存储空间'))])

    cname = StringField(_name='cname', 
                    label=_(u'CDN加速域名'), 
                    description=_(u'<p>不需要填写https或者http开头，只需要填写域名</p><p>例如：static.theonestore.cn</p>'),
                    validators=[Required(message=_(u'请填写CDN加速域名'))])


class StorageAliossForm(Form):
    access_key_id = StringField(label=_('AccessKey ID'),
                    description=_(u'<a target="_blank" href="https://help.aliyun.com/knowledge_detail/38738.html">AccessKey ID和AccessKey Secret 请见阿里云文档</a>'), 
                    validators=[Required(message=_(u'请填写ACCESSKEY'))])

    access_key_secret = StringField(label=_('AccessKey Secret'),
                    validators=[Required(message=_(u'请填写AccessKey Secret'))])

    bucket_name = StringField(label=_(u'存储空间'), 
                    description=_(u'<a target="_blank" href="https://help.aliyun.com/document_detail/31883.html">存储空间 请见阿里云OSS文档</a>'),
                    validators=[Required(message=_(u'请填写存储空间'))])

    endpoint = StringField(label=_(u'EndPoint（地域节点）'), 
                    description=_(u'请登录你的阿里云OSS查看地域节点EndPoint'),
                    validators=[Required(message=_(u'请填写EndPoint（地域节点）'))])

    cname = StringField(label=_(u'CDN加速域名'), 
                    description=_(u'<p>不需要填写https或者http开头，只需要填写域名</p><p>例如：static.theonestore.cn</p>'),
                    validators=[Required(message=_(u'请填写CDN加速域名'))])
