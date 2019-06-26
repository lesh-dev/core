from flask import Blueprint, render_template, jsonify, request
from ..menu import menu
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash

module = Blueprint('internal', __name__, url_prefix='/internal')


@module.route('/', methods=['GET'])
@module.route('/<path>', methods=['GET'])
@login_required
def index(path):
    return render_template(
        "internal/base.html",
        menu=menu,
        person=current_user,
    )


@module.route('/get_profile', methods=['GET'])
@login_required
def get_profile():
    return jsonify(current_user.serialize())


@module.route('/update_password', methods=['POST'])
@login_required
def update_password():
    current_user.direct_login.update(
        values={
            'password_hash': generate_password_hash(password=request.values['new_password'])
        }
    )
    return jsonify('OK')


@module.route('/contact/add', methods=['POST'])
@login_required
def contacts_add():
    pass
    # name = request.values['name']
    # value = request.values['value']
