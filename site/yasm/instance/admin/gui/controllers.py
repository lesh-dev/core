"""
.. _admin_gui_controllers:

Url dispatching file of :ref:`admin.gui <admin_gui>` module

|contains|
 * module - :ref:`nestable blueprint <nestable_blueprint>` which represents admin.gui module of YaSM
"""
from flask import render_template, redirect, request as rq, Response, jsonify
from flask_login import login_required, current_user
from instance.menu import menu
from instance.admin.side import side
from instance.database import db, School, Contact, Person
from instance.rights_decorator import has_rights
from instance.NestableBlueprint import NestableBlueprint

module = NestableBlueprint('admin_gui', __name__, url_prefix='')


@module.route('/', methods=['GET'])
@module.route('/<path:path>', methods=['GET'])
@login_required
@has_rights('admin')
def index(path='path'):
    """
    Main page of admin module


    |rights|
     * ``admin``

    :return: html
    """
    return render_template(
        "admin/base.html",
        menu=menu,
        person=current_user,
        side=side
    )
