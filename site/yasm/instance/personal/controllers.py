from flask import Blueprint, render_template, jsonify
from ..menu import menu
from flask_login import login_required, current_user


module = Blueprint('personal', __name__, url_prefix='/personal')


@module.route('/', methods=['GET'])
@login_required
def index():
    return render_template(
        "personal/base.html",
        menu=menu,
        person=current_user,
    )


@module.route('/get_profile', methods=['GET'])
@login_required
def get_profile():
    user = current_user
    return jsonify(user.serialize())
