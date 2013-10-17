#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Parse CSV file with emails
and extract personal data about school heads
"""

import urllib

import re

def grab_director(city, school_num, redir_url = None):
    """
    Extract school head name by given data
    Supports proshkolu.ru domain only
    """
    if school_num and not re.match('[0-9]+', school_num):
        return None

    if city:
        url = 'http://www.proshkolu.ru/org/' + city + '-' + school_num + '/'
    else:
        url = redir_url

    #print url
    prog = re.compile("location.href='(.+?)&")
    boss_re = re.compile('boss/.>(.*?)<')
    page = urllib.urlopen(url)
    contents = page.read()
    if 'location.href' in contents:
        #print 'GOT REDIRECT'
        res = prog.search(contents)
        if res:
            #print res.group(1)
            return grab_director(
                city=None,
                school_num=None,
                redir_url=res.group(1))
        else:
            #print "-------- NOT MATCHED"
            return None

    #d = u'Директор'.encode('cp1251')
    boss = None
    res = boss_re.search(contents)
    if res:
        boss = res.group(1).decode('cp1251')
        #print boss
        return boss
    else:
        #print ' ### BOSS NOT FOUND'
        return None


def process_line(arr):
    """
    Process one line of the input TSV file
    """

    name = arr[0].decode('utf-8')
    city = arr[1].decode('utf-8')
    email = arr[2].decode('utf-8')
    school_type = 'sosh'
    name = name.replace(u'СОШ №', '').strip()
    city = city.replace(u'г.', '').strip()
    if u'Лицей' in name:
        school_type = 'lic'
        name = name.replace(u'Лицей', '').strip()

    if u'Гимназия' in name:
        school_type = 'gimn'
        name = name.replace(u'Гимназия', '').strip()

    name = name.replace(u'№', '').strip()
    name = name.replace(u'СОШ', '').strip()
    email = email.lower().strip()

    fio = 'D'
    if city == u'Кострома':
        fio = grab_director(city='kostroma', school_num=name) or 'N'
    elif city == u'Саратов':
        fio = grab_director(city='saratov', school_num=name) or 'N'
    elif city == u'Ижевск':
        fio = grab_director(city='izhevsk', school_num=name) or 'N'
    elif city == u'Киров':
        fio = grab_director(city='kirov', school_num=name) or 'N'

    print school_type, '|', name.encode('utf-8'), '|', \
        city.encode('utf-8'), '|', \
        fio.encode('utf-8') + ' <' + email.encode('utf-8') + '>'


def main():
    """
    Gravicappa
    """
    csv = open('schools.csv', 'r')
    for line in csv:
        arr = line.strip().split('\t')
        if len(arr) < 3:
            print "BAD: ", line
            continue
        process_line(arr)


if __name__ == '__main__':
    main()
