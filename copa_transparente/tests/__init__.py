import json
import unittest


class JSONTestRunner:
    def run(self, test):
        result = JSONTestResult(self)
        test(result)
        print(json.dumps(result.infos, sort_keys=True, indent=4))
        return result


class JSONTestResult(unittest.TestResult):
    def __init__(self, runner):
        unittest.TestResult.__init__(self)
        self.runner = runner
        self.infos = []
        self.current = {}

    def newTest(self):
        self.infos.append(self.current)
        self.current = {}

    def startTest(self, test):
        self.current['id'] = test.id()

    def addSuccess(self, test):
        self.current['result'] = 'ok'
        self.newTest()

    def addError(self, test, err):
        self.current['result'] = 'error'
        print(err)
        self.newTest()

    def addFailure(self, test, err):
        self.current['result'] = 'fail'
        self.newTest()

    def addSkip(self, test, err):
        self.current['result'] = 'skipped'
        self.current['reason'] = err
        self.newTest()


