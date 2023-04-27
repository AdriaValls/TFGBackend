class Config:

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STATIC_FOLDER = "frontend/dist/static"
    TEMPLATE_FOLDER = "/frontend/dist/templates"
    SECRET_KEY = "kdsfklsmfakfmafmadslvsdfasdf"

config = Config
