from app import app
from apps import total

app.layout = total.total_layout

if __name__ == "__main__":
    app.run_server(debug=True)    