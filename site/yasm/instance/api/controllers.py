# from .generated import module, jsonify
from flask import Blueprint, jsonify
from instance.database import School, PersonSchool, Person

module = Blueprint('api', __name__, url_prefix='/api')


@module.route("/uninvited/<int:school_id>", methods=['GET'])
def uninvited(school_id):
    sch = School.query.get(school_id)
    if sch:
        invited = [x[0] for x in (sch
                                  .person_schools
                                  .order_by(PersonSchool.member_person_id)
                                  .with_entities(PersonSchool.member_person_id).all())
                   ]
        all = Person.query.ordered_by(Person.person_id).all()
        i = 0
        j = 0
        ans = []
        while i < len(invited) and j < len(all):
            if (all[j].person_id < invited[i]):
                ans.append(all[j])
                j += 1
            elif (all[j].person_id > invited[i]):
                i += 1
            else:
                i += 1
                j += 1
        while j < len(all):
            ans.append(all[j])
        return jsonify({
            'length': len(ans),
            'values': ans
        })
    return jsonify({
        'length': 0,
        'values': []
    })


@module.route('school_dates/<int:school_id>', methods=['GET'])
def school_dates(school_id):
    sch = School.query.get(school_id)
    start = sch.school_date_start
    end = sch.school_date_end  # TODO
    return jsonify([start, end])
