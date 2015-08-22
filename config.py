import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    MONGODB_SETTINGS = {
        # if use MongoEngine, 'db' needs to be set
        # 'db': 'boleplusdb',
        'host': '127.0.0.1',
        'port': 27017
    }

    # UPLOAD CONFIG =
    UPLOAD_FOLDER = '/data/tmp/transactions/todo/'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx', 'dot', 'zip', 'eml', 'msg', 'htm', 'html', 'xls', 'xlsx'}

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
