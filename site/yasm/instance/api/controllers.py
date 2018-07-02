from flask import Blueprint, render_template, jsonify, request as f_request
from ..database import School

module = Blueprint('api', __name__, url_prefix='/api')


@module.route('/school', methods=['GET'])
def school_list():
    return jsonify(
        {
            'schools': School.query.with_entities(School.school_title, School.school_date_start).order_by(
                School.school_date_start.desc()).all()
        }
    )