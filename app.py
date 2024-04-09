from flask import Flask
import config
import hooks
from exts import db, mail, cache, avatars
from blueprints.cms import bp as cms_bp
from blueprints.front import bp as front_bp
from blueprints.user import bp as user_bp
from flask_migrate import Migrate
import commands
from bbs_celery import make_celery
from flask_wtf import CSRFProtect
import filters

app = Flask(__name__)
app.config.from_object(config.DevelopmentConfig)
migrate = Migrate(app, db)
db.init_app(app)
mail.init_app(app)
cache.init_app(app)
avatars.init_app(app)

# 注册蓝图
app.register_blueprint(cms_bp)
app.register_blueprint(front_bp)
app.register_blueprint(user_bp)

# 添加命令
app.cli.command("create_permission")(commands.create_permission)
app.cli.command("create_role")(commands.create_role)
app.cli.command("create_test_user")(commands.create_test_user)
app.cli.command("create_admin")(commands.create_admin)
app.cli.command("create_board")(commands.create_board)
app.cli.command("create_test_post")(commands.create_test_post)

# 构建celery
celery = make_celery(app)

# CSRF保护
CSRFProtect(app)

# 添加钩子函数
app.before_request(hooks.bbs_before_request)
app.errorhandler(401)(hooks.bbs_401_error)
app.errorhandler(404)(hooks.bbs_404_error)
app.errorhandler(500)(hooks.bbs_500_error)

# 添加模板过滤器
app.template_filter("email_hash")(filters.email_hash)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
