from flask import Blueprint, render_template
from ..menu import menu
from ..database import School

module = Blueprint('admin', __name__, url_prefix='/admin')


@module.route('/', methods=['GET'])
def index():
    return render_template(
        "admin/base.html",
        menu=menu,
        side=[]
    )


@module.route('/school', methods=['GET'])
def school_dashboard():
    schools = School.query.with_entities(School.school_title, School.school_date_start).order_by(School.school_date_start).all()[::-1]
    return render_template(
        "admin/school_dashboard.html",
        menu=menu,
    )
