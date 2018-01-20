import yasm.db as db
from flask import Flask

if __name__ == "__main__":
    app = Flask(__name__)
    db.connect(app)
    # testing if all objects are readable
    for i in (db.Notification,
              db.Department,
              db.Person,
              db.Course,
              db.CourseTeachers,
              db.Exam,
              db.School,
              db.PersonSchool,
              db.PersonComment,
              db.Submission,
              db.Contestants,
              db.Problems,
              db.Solutions):
        print(i.query.all())
    app.run()