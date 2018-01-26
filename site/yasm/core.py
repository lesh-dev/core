from yasm import db
from flask import Flask
from yasm.test import Test
import yasm.config as cfg

if __name__ == "__main__":
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = cfg.db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.database.init_app(app)
    app.app_context().push()
    # testing if all objects are readable
    db.db_read_test()

    app.add_url_rule('/', view_func=Test.as_view('Greet'))
    app.run(debug=True)