import db
from flask import Flask
from test import Test
import config as cfg
import unstable.api.api_views as api

if __name__ == "__main__":
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = cfg.db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.database.init_app(app)
    api.json.init_app(app)
    app.app_context().push()
    # testing if all objects are readable
    db.db_read_test()

    app.add_url_rule('/', view_func=Test.as_view('Greet'))
    app.add_url_rule('/api', view_func=api.Api.as_view('Api'))

    @app.route('/test')
    def test():
        return open('/home/yaroslav/Projects/PyCharm/lesh/core/site/yasm/fb_test.html').read()

    @app.route('/testT')
    def testT():
        return open('/home/yaroslav/Projects/PyCharm/lesh/core/site/yasm/fb_testT.html').read()


    app.run(debug=True)