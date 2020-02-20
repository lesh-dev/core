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

