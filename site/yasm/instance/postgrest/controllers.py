from flask import Blueprint, request
from flask_login import login_required
from instance.rights_decorator import has_rights
import urllib3

module = Blueprint('postgrest', __name__, url_prefix='/postgrest')


@module.route('/<s>', methods=['GET', 'POST', 'PUT', 'PUTCH'])
@login_required
@has_rights('admin')
def index(s):
    http = urllib3.PoolManager()
    copy_headers = [
        'prefer',
        'content-type',
        'content_type',
        'content-Type',
        'content_Type',
        'Content-type',
        'Content_type',
        'Content-Type',
        'Content_Type',
        'Accept',
    ]
    headers = {}
    for h in copy_headers:
        if h in request.headers.keys():
            headers[h] = request.headers[h]
    return http.request('GET', 'localhost:3000{}'.format(request.full_path.split('postgrest')[1]), headers=headers).data
