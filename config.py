import os.path
from datetime import timedelta


class BaseConfig(object):
    SECRET_KEY = '123456'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = timedelta(days=31)
    PER_PAGE_COUNT = 10
    UPLOAD_IMAGE_PATH = "static/front"



class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/flasklearn?charset=utf8mb4'
    # 邮箱配置
    MAIL_SERVER = 'smtp.163.com'
    MAIL_USE_SSL = True
    MAIL_PORT = 465
    MAIL_USERNAME = 'jizh332804@163.com'
    MAIL_PASSWORD = 'TNJWVDIEJXSUHTUG'
    MAIL_DEFAULT_SENDER = 'jizh332804@163.com'

    # 缓存设置
    CACHE_TYPE = 'RedisCache'
    CACHE_REDIS_HOST = '127.0.0.1'
    CACHE_REDIS_PORT = 6379

    # Celery配置
    CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
    CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'

    # 个人头像
    AVATARS_SAVE_PATH = os.path.join(BaseConfig.UPLOAD_IMAGE_PATH, "avatars")


class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = ('mysql+pymysql://[测试服务器MySQL用户名]:[测试服务器MySQl密码]@[测试服务器MySQL域名]:['
                               '测试服务器MySQL端口]/flasklearn?charset=utf8mb4')


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = ('mysql+pymysql://[生产环境服务器MySQL用户名]:[生产环境服务器MySQl密码]@[生产环境服务器MySQL域名]:['
                               '生产环境服务器MySQL端口]/flasklearn?charset=utf8mb4')
