from flask import Blueprint, send_file
from flask_login import current_user
import os

module = Blueprint('secure_static', __name__, url_prefix='/secure_static')
secure_static_root = 'secure_static'


def check_existance(p):
    return os.path.isfile(os.path.join('instance', p))


def send_if_eixsts(p, *, fallback):
    if check_existance(p):
        return send_file(p)
    else:
        return fallback


def get_incognito_ava():
    return send_file(os.path.join(secure_static_root, 'avas/incognito.svg'))


@module.route('/get_ava/<int:person_id>', methods=['GET'])
def get_person_ava(person_id):
    fallback = get_incognito_ava()
    if current_user.is_authenticated:
        p = os.path.join(secure_static_root, 'avas/{id}.jpg'.format(id=person_id))
        return send_if_eixsts(
            p,
            fallback=fallback
        )
    else:
        return fallback
