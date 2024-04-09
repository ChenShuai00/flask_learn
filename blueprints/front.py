from flask import Blueprint, render_template, request, current_app, redirect, url_for, g, flash
from sqlalchemy.sql.functions import current_user

from model.post import BoardModel, PostModel, CommentModel
from decorators import login_required
from forms.post import PublicPostForm, PublicCommentForm
from exts import cache, db
from utils import restful
from flask_paginate import Pagination

bp = Blueprint("front", __name__, url_prefix="")


@bp.route("/")
def index():
    boards = BoardModel.query.all()
    # 获取页码参数
    page = request.args.get("page", type=int, default=1)
    # 获取板块参数
    board_id = request.args.get("board_id", type=int, default=0)
    # 当前page下的起始位置
    start = (page - 1) * current_app.config.get('PER_PAGE_COUNT')
    # 当前page下的结束位置
    end = start + current_app.config.get('PER_PAGE_COUNT')
    # 查询对象
    query_obj = PostModel.query.order_by(PostModel.created_time.desc())
    # 过滤帖子
    if board_id:
        query_obj = query_obj.filter_by(board_id=board_id)
    # 总共有多少帖子
    total = query_obj.count()
    # 当前page下的帖子列表
    posts = query_obj.slice(start, end)
    # 分页对象
    pagination = Pagination(bs_version=4, page=page, total=total, outer_window=0, inner_window=2, alignment="center")

    context = {
        "posts": posts,
        "boards": boards,
        "pagination": pagination,
        "current_board": board_id
    }
    return render_template("front/index.html", **context)


@bp.route("/post/public", methods=["GET", "POST"])
@login_required
def public_post():
    if request.method == "GET":
        boards = BoardModel.query.all()
        return render_template("front/public_post.html", boards=boards)
    else:
        form = PublicPostForm(request.form)
        if form.validate():
            title = form.title.data
            print(title)
            content = form.content.data
            board_id = form.board_id.data
            post = PostModel(title=title, content=content, board_id=board_id, author=g.user)
            db.session.add(post)
            db.session.commit()
            return restful.ok()
        else:
            message = form.messages[0]
            return restful.param_error(message=message)


@bp.route("/post/detail/<int:post_id>")
def post_detail(post_id):
    post = PostModel.query.get(post_id)
    post.read_count = post.read_count + 1
    db.session.commit()
    return render_template("front/post_detail.html", post=post)


@bp.route("/post/<int:post_id>/comment", methods=["GET", "POST"])
@login_required
def public_comment(post_id):
    form = PublicCommentForm(request.form)
    if form.validate():
        content = form.content.data
        comment = CommentModel(content=content, post_id=post_id, author=g.user)
        db.session.add(comment)
        db.session.commit()
    else:
        for message in form.messages:
            flash(message)
    return redirect(url_for("front.post_detail", post_id=post_id))
