from flask import Flask
from flask_cors import CORS
from components.config import Config
import components.routes as routes

class DashboardApp:
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app, expose_headers=['Content-Disposition'])
        Config.init_app(self.app)
        routes.register_routes(self.app)

    def run(self):
        self.app.run(debug=True)

if __name__ == "__main__":
    app = DashboardApp()
    app.run()
