"""
.. _admin_controllers:

Url dispatching file of :ref:`admin <admin>` module

|contains|
 * module - :ref:`nestable blueprint <nestable_blueprint>` which represents admin module of YaSM
"""
from instance.NestableBlueprint import NestableBlueprint
from instance.admin.gui import module as gui
from instance.admin.api import module as api

module = NestableBlueprint('admin', __name__, url_prefix='/admin')
module.register_blueprint(gui)
module.register_blueprint(api)
