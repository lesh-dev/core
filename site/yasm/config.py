"""
General configuration file with lowest priority.

**__NEVER__ STORE IMPORTANT DATA HERE**

 * DEBUG - Mode must be set to False in production see `flask documentation <http://flask.pocoo.org/docs/1.0/config/>`_
 * SQLALCHEMY_TRACK_MODIFICATIONS - database URI see `sqlalchemy manual <https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/>`_
 * SQLALCHEMY_DATABASE_URI - database URI see `sqlalchemy manual <https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/>`_

"""


DEBUG = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = \
    "postgresql://user:password@url/database:port"
