import requests
import unittest


class Test200(unittest.TestCase):
    pass


fronts = []


def create_reques_callback(url):
    def callback(self):
        r = requests.head(request_format.format(url=url))
        self.assertEquals(r.status_code, 200)
    return callback


name_format = "test{name}"
request_format = "http://localhost:5000{url}"
for url in fronts:
    setattr(Test200, name_format.format(name=url.replace("/", "_")), create_reques_callback(url))
