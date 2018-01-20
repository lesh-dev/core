from yasm.db import *
from flask import Flask
from yasm.test import Test
import yasm.config as cfg

if __name__ == "__main__":
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = cfg.db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    database.init_app(app)
    app.app_context().push()
    # testing if all objects are readable
    for i in (Notification,
              Department,
              Person,
              Course,
              CourseTeachers,
              Exam,
              School,
              PersonSchool,
              PersonComment,
              Submission,
              Contestants,
              Problems,
              Solutions):
        print(i.query.all())

    app.add_url_rule('/', view_func=Test.as_view('Greet'))
    app.run()