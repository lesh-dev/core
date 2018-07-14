from flask import Blueprint, render_template, redirect, request as rq, Response, jsonify
from ..menu import menu
from .side import side
from ..database import db, School, Contact

module = Blueprint('admin', __name__, url_prefix='/admin')


def resp(code, data):
    return Response(
        status=code,
        mimetype="application/json",
        response=jsonify(data)
    )


@module.route('/', methods=['GET'])
def index():
    return render_template(
        "admin/base.html",
        menu=menu,
        side=side
    )


@module.route('/gui/', methods=['GET'])
@module.route('/gui/<path:path>', methods=['GET'])
def admin(path='path'):  # resolved by reactJS
    return render_template(
        "admin/base.html",
        menu=menu,
        side=side
    )


@module.route('/api/schools/add', methods=['GET'])
def school_add():
    args = rq.args
    title = args['title']
    start = args['start']
    end = args['end']
    tp = args['type']
    location = args['location']
    s = School(
        school_title=title,
        school_type=tp,
        school_date_start=start,
        school_date_end=end,
        school_location=location,
        school_created='now',
        school_modified='now',
        school_changedby='me'
    )
    db.session.add(s)
    db.session.commit()
    return resp(200, [])


@module.route('/api/contact/del/<int:id>', methods=['POST'])
def api_contact_del(id):
    Contact.query.filter(Contact.id == id).delete()
    db.session.commit()
    return jsonify('OK')


@module.route('/api/contact/add/<int:person_id>', methods=['POST'])
def api_contact_add(person_id):
    name = rq.values['name']
    url = rq.values['url']
    add = Contact(
        person_id=person_id,
        name=name,
        value=url
    )
    db.session.add(add)
    db.session.commit()
    return jsonify('OK')
