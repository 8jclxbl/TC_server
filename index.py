from app import app,server
from apps import total

app.layout = total.total_layout

if __name__ == "__main__":
    from werkzeug.contrib.fixers import ProxyFix
    server.wsgi_app = ProxyFix(server.wsgi_app)
    app.run_server()    
