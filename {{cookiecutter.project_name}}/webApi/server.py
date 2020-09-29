import os
from waitress import serve
from app import app

if __name__ == "__main__":
    app.debug = False
    server = os.getenv("SERVER")
    port = os.getenv("PORT")
    serve(app, host=server, port=port)
