from serunner.log  import logger
from serunner.utils  import  py_version_2
import inspect
from serunner.data import DataTearDown
class Runner():
    def __init__(self,each_test_global):
        self.test_global = DataTearDown(each_test_global)

    def _get_arg_msg(self,func):
        '''
        获取动态参数
        :param func:
        :return:
        '''
        if py_version_2:
            spec = inspect.getargspec(func)
            keywords = spec.keywords
        else:
            spec = inspect.getfullargspec(func)
            keywords = spec.varkw
        args = spec.args[1:] if inspect.ismethod(func) else spec.args  # 去除self 参数
        defaults = spec.defaults or ()
        nargs = len(args) - len(defaults)
        mandatory = args[:nargs]
        defaults = zip(args[nargs:], defaults)
        return mandatory, defaults, spec.varargs, keywords

    def get_dynamic_args(self,func):
        args, defaults, varargs, kwargs = self._get_arg_msg(func)
        args += ['{}={}'.format(name, value) for name, value in defaults]
        if varargs:
            args.append('*{}'.format(varargs))
        if kwargs:
            args.append('**{}'.format(kwargs))
        return args

    def _get_func_args(self,defaults,args,funcArgs):
        '''
        获取形参的实例
        :param defaults:
        :param args:
        :param funcArgs:
        :return:
        '''
        # func_args = [value for name, value in funcArgs.items()][0]

        kwargs,new_kwargs = {},{}
        for name, value in defaults:
            if name in args:
                args.remove(name)
                kwargs[name] = value

        for index, func_arg in enumerate(funcArgs):
            if func_arg:
                value = func_arg.split("=")
                if len(value) == 2:
                    kwargs[value[0]] = value[1]
                else:
                    new_kwargs[args[index]] = func_arg
        new_kwargs.update(kwargs)
        return new_kwargs
    def __get_static_args(self,func,funcArgs):
        '''
        :param func:
        :param funcArgs:
        :return:
        '''
        args, defaults, varargs, kwargs = self._get_arg_msg(func)
        args += ['{}={}'.format(name, value) for name, value in defaults]
        # print (defaults, args, funcArgs)  #<zip object at 0x0000017A59939C48> ['url'] ['https://baidu.com']
        kwargs = self._get_func_args(defaults,args,funcArgs)
        return  kwargs

    def __run_keyword(self,func,funcArgs):
        '''
        运行关键词函数
        :param func:
        :param funcArgs:
        :return:
        '''
        kwargs = self.__get_static_args(func,funcArgs)
        result = func(**kwargs)
        return result


    def  run_test(self,test_case_dict):
        '''
        运行用例
        '''
        # 提取用例信息
        run_step = test_case_dict.get("steps",[])
        fact_result = test_case_dict.get("fact_result",[])
        assert_assert = test_case_dict.get("assert",[])

        def run_method(value):
            # 运行关键字
            if len(value) == 1:
                result = self.__run_keyword(value[0][0], value[0][1])
            else:
                for index in range(len(value)):
                    result = self.__run_keyword(value[index][0], value[index][1])

            return result

        # 运行测试步骤
        fact_result_list,each_result = [],{}
        for step in run_step:
            for key,value in step.items():
                # 提取结果
                if key in fact_result:
                    result = run_method(value)
                    each_result[key] = result
                else:
                    run_method(value)
        logger.info("步骤运行成功")
        fact_result_list.append(each_result)

        # 更新全局变量
        self.test_global.update_variable(fact_result_list)

        # 结果验证
        self.test_global.assert_result(assert_assert)





