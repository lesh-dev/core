from flask import jsonify, request
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash

from instance.NestableBlueprint import NestableBlueprint


module = NestableBlueprint('internal-api', __name__, url_prefix='/api')


@module.route('/get_profile', methods=['POST'])
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


@module.route('/courses', methods=['POST'])
@login_required
def courses():
    return jsonify(
        [ct.course.serialize() for ct in current_user.course_teachers]
    )
