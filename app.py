import re, os, random, string
from typing_extensions import Self
from flask import Flask, request, template_rendered, Blueprint, url_for, redirect, flash, render_template
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from datetime import datetime
from numpy import identity, product
from sqlalchemy import null
from api.api import *
from api.sql import *
from bookstore.views.store import *
from backstage.views.analysis import *
from backstage.views.manager import *
from link import *
from werkzeug.utils import secure_filename

## Flask-Login : 確保未登入者不能使用系統
app = Flask(__name__)
app.secret_key = 'Your Key' 

app.register_blueprint(api, url_prefix='/')                 ##登入、註冊頁面
app.register_blueprint(store, url_prefix='/bookstore')      ##使用者
app.register_blueprint(analysis, url_prefix='/backstage')   ##資料分析頁面
app.register_blueprint(manager, url_prefix='/backstage')    ##管理員

login_manager.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.debug = True
    app.secret_key = "Your Key"
    app.run()