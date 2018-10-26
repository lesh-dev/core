import json
import contextvars


result = contextvars.ContextVar("result")


class Loader(object):
    def __init__(self, test_case):
        self.test_case = test_case

    def __enter__(self):
        with open("tests/results", "r") as results_file:
            self.results = json.load(results_file)
            result.set(self.results[self.test_case] if self.test_case in self.results.keys() else None)

    def __exit__(self, exc_type, exc_val, exc_tb):
        with open("tests/results", "w") as results_file:
            if (not self.test_case in self.results.keys() and result.get() != None) or result.get() != self.results[self.test_case]:
                self.results[self.test_case] = result.get()
            results_file.write(json.dumps(self.results, indent=4, sort_keys=True))
            if exc_val:
                raise exc_val


def load_result(f):
    def decorated(*args, **kwargs):
        test_case = args[0].id()
        with Loader(test_case):
                f(*args, **kwargs)
    return decorated