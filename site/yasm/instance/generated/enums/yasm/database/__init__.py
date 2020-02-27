import enum


class AnketaStatus(enum.Enum):
    progress = 'progress'
    nextyear = 'nextyear'
    duplicate = 'duplicate'
    reserved = 'reserved'
    cont = 'cont'
    old = 'old'
    new = 'new'
    processed = 'processed'
    declined = 'declined'
    taken = 'taken'
    duplicated = 'duplicated'
    spam = 'spam'
    discuss = 'discuss'
    less = 'less'
    verify = 'verify'

class Curatorship(enum.Enum):
    empty = 'empty'
    none = 'none'
    assist = 'assist'
    cur = 'cur'

class SchoolType(enum.Enum):
    lesh = 'lesh'
    vesh = 'vesh'
    zesh = 'zesh'
    summer = 'summer'
    summmer = 'summmer'
    winter = 'winter'
    spring = 'spring'

class CourseType(enum.Enum):
    generic = 'generic'
    other = 'other'
    facult = 'facult'
    prac = 'prac'
    single = 'single'

class CourseArea(enum.Enum):
    cs = 'cs'
    unknown = 'unknown'
    nature = 'nature'
    precise = 'precise'
    other = 'other'
    human = 'human'

