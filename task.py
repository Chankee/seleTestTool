import unittest
from serunner.log import  logger
from serunner import loader,parser,runner
from threading import  Thread
class SeRunner(object):
    def __init__(self,**kwargs):
        self.unittest_runner = unittest.TextTestRunner(**kwargs)
        self.test_loader = unittest.TestLoader()
        self.summary = []
        self.test_result = []

    def timeit(func):
        '''
        线程运行时间监测
        :return:  装饰器
        '''
        import time
        def wrapper(*args, **kwargs):
            start_time = time.time()
            res = func(*args, **kwargs)
            end_time = time.time()
            logger.info("%s函数运行时间为：%.2f" % (func.__name__, end_time - start_time))
            return res

        return wrapper
    def run_thread(self, testcase):
        '''
        多线程运行
        '''
        import time
        start_time = time.time()
        result = self.unittest_runner.run(testcase)
        end_time = time.time()
        logger.info("用例集运行时间为：%.2f" % (end_time - start_time))
        self.test_result.append((result,end_time - start_time))

    @timeit
    def run_suite(self, test_suite):
        # 多线程执行用例
        tests_thread = []

        for testcase in test_suite:
            case_thread = Thread(target=self.run_thread, args=(testcase,))
            tests_thread.append(case_thread)
        for case in tests_thread:

            case.setDaemon(True)
            case.start()
        for  case in tests_thread:
            case.join()

    def run(self, path_or_testcases):
        '''
        运行测试套件
        '''

        test_cases = loader.load_testcases(path_or_testcases)

        test_cases = parser.parse_tests(test_cases)

        test_suite = self.add_test(test_cases)

        self.run_suite(test_suite)
        self.summary_result(self.test_result)

        return self.summary
    def add_test(self,testCases):
        '''
        添加测试套件
        '''
        test_cations = []
        def  _add_run_step(runner,test_global,test_case_dict):
            def test(self):
                try:
                    runner.run_test(test_case_dict)
                except Exception as err:
                    self.fail(str(err))

            test.__doc__ = test_case_dict["name"]
            return test
        test_suite = unittest.TestSuite()

        for testcase in testCases:

            test_global = testcase.get("global", {})

            run = runner.Runner(test_global)
            TestFunc = type('TestSequense', (unittest.TestCase,), {})

            test_cases = testcase.get("testcases", [])
            for index, test_case_dict in enumerate(test_cases):
                for times_index in range(int(test_case_dict.get("times", 1))):
                    test_method_name = 'test_{:02}_{:02}'.format(index, times_index)
                    test_method = _add_run_step(run,test_global,test_case_dict)

                    setattr(TestFunc,test_method_name,test_method)
                loaded_testcase = self.test_loader.loadTestsFromTestCase(TestFunc)

                for item in test_case_dict["steps"]:
                    for key,value in item.items():
                        test_cations.append(key)
            setattr(loaded_testcase, "test_global", test_global)

            setattr(loaded_testcase, "step_action", test_cations)

            test_suite.addTest(loaded_testcase)

        return test_suite

    def summary_result(self,results):
        '''
        基于测试运行下的测试报告汇总
        '''
        for each_result,time in results:
            summary = {
                "success": each_result.wasSuccessful(),
                "spend_time": time,
                "stat": {
                    'testsRun': each_result.testsRun,
                    'failures': len(each_result.failures),
                    'errors': len(each_result.errors),
                    'skipped': len(each_result.skipped),
                    'expectedFailures': len(each_result.expectedFailures),
                    'unexpectedSuccesses': len(each_result.unexpectedSuccesses)
                }
            }

            summary["stat"]["successes"] = summary["stat"]["testsRun"] - summary["stat"]["failures"] \
                                           - summary["stat"]["errors"] - summary["stat"]["skipped"] \
                                           - summary["stat"]["expectedFailures"] - summary["stat"]["unexpectedSuccesses"]
            self.summary.append(summary)



