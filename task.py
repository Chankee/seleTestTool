import unittest
from serunner.log import  logger
from serunner import  loader,parser,excepetions,runner
class SeRunner(object):
    def __init__(self,**kwargs):
        self.unittest_runner = unittest.TextTestRunner(**kwargs)
        self.test_loader = unittest.TestLoader()
        self.summary = None

    def run(self, path_or_testcases):

        test_cases = loader.load_testcases(path_or_testcases)

        test_suite = parser.parse_tests(test_cases)

        self.add_test(test_suite)
    def add_test(self,testCases):
        '''
        添加测试套件
        '''
        test_suite = unittest.TestSuite()

        for testcase in testCases:
            test_global = testcase.get("global", {})

            run = runner.Runner()
            TestSequense = type('TestSequense', (unittest.TestCase,), {})

            test_cases = testcase.get("testcases", [])
            for index, test_case_dict in enumerate(test_cases):
                run.run_test(test_case_dict.get("steps"))
                for times_index in range(int(test_case_dict.get("times", 1))):
                    test_method_name = 'test_{:02}_{:02}'.format(index, times_index)