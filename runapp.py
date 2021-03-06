# -*- coding: utf-8 -*-
"""
    theonestore
    https://github.com/kapokcloud-inc/theonestore
    ~~~~~~~~~~~
    :copyright: © 2018 by the Kapokcloud Inc.
    :license: BSD, see LICENSE for more details.
"""

from json import loads as json_loads

from flask_babel import Babel
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
import flask_excel as excel

from app import configure_before

from app.database import db

from app.helpers import (
    create_app, 
    enable_logging,
    register_blueprint,
    configure_uploads,
    static_uri,
    toint,
    toamount,
    get_file_uploadtype,
    request_args_to_query_string
)
from app.helpers.date_time import (
    timestamp2str,
    before_after_timestamp
)

from app.helpers.data_format import(
    format_amount,
    format_avatar
)

from app.routes.admin import ADMIN_ROUTES
from app.routes.mobile import MOBILE_ROUTES
from app.routes.api import API_ROUTES
from app.routes.pc import PC_ROUTES


# 创建App
app = create_app()

# 打开日志记录
enable_logging(app)

# 多国语言i18n支持
babel = Babel()
babel.init_app(app)

# 注册路由
register_blueprint(app, ADMIN_ROUTES)
register_blueprint(app, MOBILE_ROUTES)
register_blueprint(app, API_ROUTES)
register_blueprint(app, PC_ROUTES)

# 数据库初始化
db.init_app(app)

# 上传文件存储
configure_uploads(app)

# 启动form表单csr保护
csrf = CSRFProtect(app)
csrf.exempt('app.views.admin.upload.ueditor')
csrf.exempt('app.views.api.pay.notify')

# flask session
Session(app)

excel.init_excel(app)

# 注册jinja模板过滤器
jinja_filters = {
    'timestamp2str':timestamp2str,
    'before_after_timestamp':before_after_timestamp,
    'json_loads':json_loads,
    'static_uri':static_uri,
    'toint':toint,
    'toamount':toamount,
    'get_file_uploadtype':get_file_uploadtype,
    'request_args_to_query_string':request_args_to_query_string,
    'format_amount':format_amount,
    'format_avatar':format_avatar
}
app.jinja_env.filters.update(jinja_filters)
app.jinja_env.cache_size = 0

configure_before(app)


if __name__ == '__main__':
    app.config.from_pyfile('config/config.dev.cfg')
    babel.init_app(app)

    # 上传文件存储
    configure_uploads(app)

    app.jinja_env.auto_reload = True
    app.jinja_env.cache_size = 0
    app.run(host='0.0.0.0', debug=True, port=5000)
    # app.run(
    #     host='0.0.0.0',
    #     debug=True,
    #     port=443,
    #     ssl_context=(
    #         'C:\workspace\ssl\kapokcloud.com.pem',
    #         'C:\workspace\ssl\kapokcloud.com.key'))
