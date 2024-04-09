from flask import Blueprint, render_template, g, redirect, request, flash, url_for
from decorators import permission_required
from forms.cms import AddStaffForm, EditStaffForm
from model.user import PermissionEnum, UserModel, RoleModel
from exts import db

bp = Blueprint("cms", __name__, url_prefix="/cms")


@bp.route("")
def index():
    return render_template("cms/index.html")


@bp.route("/staff/list")
@permission_required(PermissionEnum.CMS_USER)
def staff_list():
    users = UserModel.query.filter_by(is_staff=True).all()
    return render_template("cms/staff_list.html", users=users)


@bp.route("/staff/add", methods=["POST", "GET"])
@permission_required(PermissionEnum.CMS_USER)
def staff_add():
    if request.method == "GET":
        roles = RoleModel.query.all()
        return render_template("cms/add_staff.html", roles=roles)
    else:
        form = AddStaffForm(request.form)
        if form.validate():
            email = form.email.data
            role_id = form.role.data
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                flash("没有此用户")
                return redirect(url_for("cms.staff_add"))
            user.is_staff = True
            user.role = RoleModel.query.get(role_id)
            db.session.commit()
            return redirect(url_for("cms.staff_list"))


@bp.route("/staff/edit/<string:user_id>", methods=["POST", "GET"])
@permission_required(PermissionEnum.CMS_USER)
def staff_edit(user_id):
    user = UserModel.query.get(user_id)
    if request.method == "GET":
        roles = RoleModel.query.all()
        return render_template("cms/edit_staff.html", user=user, roles=roles)
    else:
        form = EditStaffForm(request.form)
        if form.validate():
            is_staff = form.is_staff.data
            role_id = form.role.data
            user.is_staff = is_staff
            if user.role.id != role_id:
                user.role = RoleModel.query.get(role_id)
            db.session.commit()
            return redirect(url_for("cms.staff_edit", user_id=user_id))
        else:
            for message in form.messages:
                flash(message)
            return redirect(url_for("cms.staff_edit", user_id=user_id))

@bp.before_request
def cms_before_request():
    if not hasattr(g, "user") or g.user.is_staff == False:
        return redirect("/")


@bp.context_processor
def cms_context_processor():
    return {"PermissionEnum": PermissionEnum}
