import os

class Config:
    UPLOAD_FOLDER = 'uploads'

    @staticmethod
    def init_app(app):
        if not os.path.exists(Config.UPLOAD_FOLDER):
            os.makedirs(Config.UPLOAD_FOLDER)
        app.config['UPLOAD_FOLDER'] = Config.UPLOAD_FOLDER
