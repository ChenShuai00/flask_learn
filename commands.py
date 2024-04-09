from model.post import BoardModel, PostModel
from model.user import PermissionModel, RoleModel, PermissionEnum, UserModel
import click
from exts import db
from faker import Faker
import random


# 创建权限
def create_permission():
    for permission_name in dir(PermissionEnum):
        if permission_name.startswith("__"):
            continue
        permission = PermissionModel(name=getattr(PermissionEnum, permission_name))
        db.session.add(permission)
    db.session.commit()
    click.echo("权限添加成功！")


# 创建角色
def create_role():
    # 稽查
    inspector = RoleModel(name="稽查", desc="负责审核帖子和评论是否合法合规")
    inspector.permissions = PermissionModel.query.filter(
        PermissionModel.name.in_([PermissionEnum.POST, PermissionEnum.COMMENT])).all()

    # 运营
    operator = RoleModel(name="运营", desc="负责网站持续正常运营")
    operator.permissions = PermissionModel.query.filter(PermissionModel.name.in_([PermissionEnum.POST, PermissionEnum.COMMENT, PermissionEnum.BOARD, PermissionEnum.FRONT_USER])).all()

    # 管理员
    administrator = RoleModel(name="管理员", desc="负责整个网站的所有工作")
    administrator.permissions = PermissionModel.query.all()

    db.session.add_all([inspector, operator, administrator])
    db.session.commit()
    click.echo("角色添加成功！")


# 创建测试用户

def create_test_user():
    admin_role = RoleModel.query.filter_by(name="管理员").first()
    zhangsan = UserModel(username="张三", email="zhangsan@zlkt.net", role=admin_role, password="111111", is_staff=True)

    operator_role = RoleModel.query.filter_by(name="运营").first()
    lisi = UserModel(username="李四", email="lisi@zlkt.net", role=operator_role, password="111111", is_staff=True)

    inspector_role = RoleModel.query.filter_by(name="稽查").first()
    wangwu = UserModel(username="王五", email="wangwu@zlkt.net", role=inspector_role, password="111111", is_staff=True)

    db.session.add_all([zhangsan, lisi, wangwu])
    db.session.commit()
    click.echo("测试用户添加成功!")


# 创建管理员命令

@click.option("--username", '-u')
@click.option("--email", '-e')
@click.option("--password", '-p')
def create_admin(username, email, password):
    admin_role = RoleModel.query.filter_by(name="管理员").first()
    admin_user = UserModel(username=username, email=email, password=password, role=admin_role, is_staff=True)
    db.session.add(admin_user)
    db.session.commit()
    click.echo("管理员创建成功！")


# 创建板块
def create_board():
    board_names = ["Python语法", 'web开发', '数据分析', '测试开发', '运维开发']
    for board_name in board_names:
        board = BoardModel(name=board_name)
        db.session.add(board)
    db.session.commit()
    click.echo("板块添加成功！")


# 创建帖子测试数据
def create_test_post():
    faker = Faker(locale="zh_CN")
    author = UserModel.query.first()
    boards = BoardModel.query.all()

    click.echo("开始生成测试帖子.....")
    for x in range(98):
        title = faker.sentence()
        content = faker.paragraph(nb_sentences=10)
        random_index = random.randint(0, 4)
        board = boards[random_index]
        post = PostModel(title=title, content=content, board=board, author=author)
        db.session.add(post)
    db.session.commit()
    click.echo("测试帖子生成成功！")