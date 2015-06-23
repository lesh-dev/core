#!/usr/bin/env python

import datetime
import os

version_file = 'site/VERSION'

current_version = open(version_file).read().strip()
version_components = current_version.split('.')
version_components[2] = str(int(version_components[2]) + 1)
new_version = '.'.join(version_components)

print "New version is", new_version
with open(version_file, 'w') as vf:
    vf.write(new_version + '\n')
os.system('git commit -m "Version updated to {}" {}'.format(new_version, version_file))
os.system('git tag {}-prod-{}'.format(new_version, datetime.datetime.now().strftime("%Y.%m.%d")))
os.system('./push-prod.sh')
