import db


def get_display(cl):
    if db.Notification == cl:
        entryes = cl.query.with_entities(
            cl.mail_group
        )
    elif db.Department == cl:
        entryes = cl.query.with_entities(
            cl.department_title
        )
    elif db.Person == cl:
        entryes = cl.query.with_entities(
            cl.first_name,
            cl.last_name,
            cl.nick_name
        )
    elif db.Course == cl:
        entryes = cl.query.with_entities(
            cl.course_title,
            cl.school_id
        )
    elif db.CourseTeachers == cl:
        entryes = cl.query.with_entities(
            cl.course_id,
            cl.course_teachers_id
        )
    elif db.Exam == cl:
        entryes = cl.query.with_entities(
            cl.course_id,
            cl.student_person_id
        )
    elif db.School == cl:
        entryes = cl.query.with_entities(
            cl.school_title
        )
    elif db.PersonSchool == cl:
        entryes = cl.query.with_entities(
            cl.member_person_id,
            cl.member_department_id,
            cl.school_id
        )
    elif db.PersonComment == cl:
        entryes = cl.query.with_entities(
            cl.blamed_person_id,
            cl.person_comment_created
        )
    elif db.Submission == cl:
        entryes = cl.query.with_entities(
            cl.sender,
            cl.submission_timestamp
        )
    elif db.Contestants == cl:
        entryes = cl.query.with_entities(
            cl.name,
            cl.contest_year
        )
    elif db.Problems == cl:
        entryes = cl.query.with_entities(
            cl.problem_name,
            cl.contest_year
        )
    elif db.Solutions == cl:
        entryes = cl.query.with_entities(
            cl.problem_id,
            cl.contestant_id,
            cl.resolution_mark
        )
    else:
        return []
    entryes = entryes.all()
    if len(entryes) == 0:
        return []
    lengths = [0] * len(entryes[0])
    for elem in entryes:  # TODO: vectorize?
        for j in range(len(lengths)):
            if elem[j] is not None:
                lengths[j] = max(lengths[j], len(str(elem[j])))
    results = []
    for elem in entryes:
        current = ''
        for j in range(len(lengths)):
            if elem[j] is not None:
                current += str(elem[j]) + '&nbsp' * (lengths[j] + 1 - len(str(elem[j])))
            else:
                current += '&nbsp' * (lengths[j] + 1)
        results.append(current)

    return results