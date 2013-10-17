#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import urllib

import re

def grab_director(city, school_num, redir_url = None):
    if city:
        url = 'http://www.proshkolu.ru/org/' + city + '-' + school_num + '/'
    else:
        url = redir_url

    print url
    prog = re.compile("location.href='(.+?)&")
    dp = re.compile('boss/.>(.*?)<')
    f = urllib.urlopen(url)
    contents = f.read()
    if 'location.href' in contents:
        print 'GOT REDIRECT'
        res = prog.search(contents)
        if res:
            print res.group(1)
            return grab_director(city=None, school_num=None, redir_url=res.group(1))
        else:
            print "-------- NOT MATCHED"
            return None

    d = u'Директор'.encode('cp1251')
    boss = None
    res = dp.search(contents)
    if res:
        boss = res.group(0)
        print boss
        return boss
    else:
        print ' ### BOSS NOT FOUND'
        return None


with open('schools.csv', 'r') as f:
    for line in f:
        a = line.strip().split('\t')
        if len(a) < 3:
            print "BAD: ", line
            continue

        name = a[0].decode('utf-8')
        city = a[1].decode('utf-8')
        email = a[2].decode('utf-8')
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

        if city == u'Кострома':
            fio = grab_director(city='kostroma', school_num=name)

        print school_type, '|', name.encode('utf-8'), '|', city.encode('utf-8'), '|', email.encode('utf-8')

