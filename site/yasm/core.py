import db
from flask import Flask
from test import Test
import config as cfg
from unstable.api.rest_api_example import PersonList, PersonDetail
from unstable.api.custom_api_example import School2Persons
from flask_rest_jsonapi import Api

if __name__ == "__main__":
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = cfg.db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.database.init_app(app)
    app.app_context().push()
    # testing if all objects are readable
    db.db_read_test()
    app.add_url_rule('/', view_func=Test.as_view('Greet'))
    app.add_url_rule('/school_2_persons/<int:school_id>', view_func=School2Persons.as_view('S2P'))
    # app.add_url_rule('/api', view_func=api.Api.as_view('Api'))
    # app.add_url_rule('/api/persons_get', view_func=api.PersonsGet.as_view('PersonsGet'))

    api = Api(app)
    api.route(PersonList, 'person_list', '/persons')
    api.route(PersonDetail, 'person_detail', '/persons/<int:id>')

    @app.route('/test')
    def test():
        return open('/home/yaroslav/Projects/PyCharm/lesh/core/site/yasm/fb_test.html').read()

    @app.route('/testT')
    def testT():
        return open('/home/yaroslav/Projects/PyCharm/lesh/core/site/yasm/fb_testT.html').read()


    app.run(debug=True)