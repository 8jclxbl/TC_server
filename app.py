import dash
from flask import Flask
#master分支是初赛提交的代码，数据开始是存储在mysql中，使用flask的sqlalchemy插件实现基于orm的数据读取
#后来测试发现使用数据库，在总体域中由于需要频繁的sql查询，导致速度过慢。鉴于数据的大小，成绩相关的部分均使用csv存储，在服务启动时加载如内存中

#pure-csv分支，实现了彻底的将mysql数据库剥离

server = Flask(__name__)

#网页的css
external_stylesheets = ['./static/total.css'] 

#此js文件是dash绘图所必须的，但是由于其服务器在国外，此js成了网站访问速度的瓶颈
#这里直接修改了dash库的源代码，dash/__init__.py,注释掉了默认的地址，使得可以从服务器获取文件
external_scripts = ['./static/plotly-1.47.0.min.js','./static/draw_background.js']
app = dash.Dash(server = server,external_stylesheets=external_stylesheets,external_scripts=external_scripts)
#dash的多页面程序所必须的
app.config.suppress_callback_exceptions = True
#配置文件中原本存放了数据库的路径
#删除数据库相关模块后，现在只剩了csrp的secret
server.config.from_object('config')