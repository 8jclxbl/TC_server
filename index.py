from app import app,server
from apps import total

app.layout = total.total_layout

if __name__ == "__main__":
    #在服务器上使用gunicorn需要这两句，开发环境下不需要
    #from werkzeug.contrib.fixers import ProxyFix
    #server.wsgi_app = ProxyFix(server.wsgi_app)
    app.run_server(debug = True)    
