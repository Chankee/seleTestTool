
from serunner.log import logger
from serunner.sekey import KeyWord,_get_global
from serunner.excepetions import KeyNameError
import importlib
import re


def parse_dynamic_args(arg,variable):
    '''
    获取动态变量
    e.g $url/index/$page
    '''
    variable_regexp = r"\$([\w_]+)"
    try:
        args = re.findall(variable_regexp,arg)
        new_arg = arg
        if args:
            for arg_v in args:
                if  arg_v in variable.keys():
                    dynamic_arg_value = variable[arg_v]
                    new_arg = new_arg.replace("${}".format(arg_v),dynamic_arg_value,1)
                else:
                    err = "该变量[{}]还没定义，请重新定义".format(arg)
                    logger.error(err)
                    raise  NameError(err)
            return new_arg
    except TypeError:
        return None


def parse_after_value(value, variable=None):
    '''
    对变量的解析
    e.g  value = "$url"  variable={"url":"https://www.baidu.com"}

    '''
    if not variable:
        return value
    new_value = parse_dynamic_args(value,variable)
    if not new_value:
        return value
    else:
        return new_value

def parse_extend_module():
    '''
    动态加载拓展的关键词
    :return: extend.对象
    '''
    try:
        handler_class = getattr(
            importlib.import_module("extend"),
            "Extend")
        return handler_class
    except:
        err = "拓展关键字模块加载失败"
        logger.error(err)
        raise  NotImplementedError(err)

def convert_func_list(action,args,varibales=None):
    '''
    这个转换返回                            需要修改
    将关键词 转为 method  e.g
        {"open": "id|kw"}
    返回
        [kw.method,[args]]
    '''
    kw =KeyWord()
    extend_key = parse_extend_module()
    ek = extend_key(_get_global().driver)
    action_list = []

    if hasattr(kw, action):
        action_key = getattr(kw, action)
        new_args = __get_args(args,varibales)
        action_list = [action_key, new_args]

    if hasattr(ek,action):
        action_key = getattr(ek, action)
        new_args = __get_args(args,varibales)
        action_list = [action_key, new_args]

    if not action_list:
        err = "{key}关键字并不存在，请自行添加或者查询关键字添加方法".format(key=action)
        logger.error(err)
        raise KeyNameError(err)
    return action_list

def __get_args(args,varibale=None):
    '''
     拆分action参数 e.g
         "id|login_username"
    返回列表类型
        ["id","login_username"]
    '''
    values = parse_after_value(args,varibale)
    if isinstance(values,str):
        value = values.split("|")
    return value

def __parse_each_action(action,variables=None):
    '''
    将每一个action拆分为字典格式，支持如下两种格式:
    1.{"key_word":"args_1|args_2"} ==>
                    {"关键词":
                        [函数,[参数1，参数2...]]
                    }
    2.{"dynamic":[{"key_word_1":"args_1|args_2"},{"key_word_2":"args_1|args_2"}]} ==>
                    {"动态名":[
                        {"key_word_1":[函数1,[参数1，参数2, ...]]},
                        {"key_word_2":[函数2，[参数1，参数2，...]]},
                    ]}
    两种格式都可以出现在action中
    '''
    new_action_dict = {}
    for key, value in action.items():
        if isinstance(value, str):
            new_action_dict[key] = convert_func_list(key, value,variables)
        elif isinstance(value, (list,)):
            new_actions = []
            for action in value:
                new_action = __parse_each_action(action,variables)
                new_actions.append(new_action)
            new_action_dict[key] = new_actions

    return new_action_dict
def __parse_return_action_format(dict_step,key):
    '''
    解析返回的关键词格式
    '''
    result = []
    if isinstance(dict_step[key][0],dict):
        for step in dict_step[key]:
            for k,value in step.items():
                if not isinstance(value[0],(list,dict)):
                    result.append(value)
                else:
                    result = value

    if not isinstance(dict_step[key][0],(list,dict)):
        result.append(dict_step[key])

    dict_step[key] = result
    return dict_step

def get_format_action(action,varibales=None):
    '''
    得到解析后的action
    e.g
    1.{"key_word":"args_1|args_2"} ==>
                    {"关键词":[
                        [函数,[参数1，参数2...]]
                    ]}
    2.{"dynamic":[{"key_word_1":"args_1|args_2"},{"key_word_2":"args_1|args_2"}]} ==>
                    {"动态名":[
                        [函数1,[参数1，参数2, ...]],
                        [函数2，[参数1，参数2，...]],
                    ]}
    '''
    dict_action = __parse_each_action(action,varibales)
    formact_action = {}
    for key,value in dict_action.items():
        formact_action.update(__parse_return_action_format(dict_action,key))
    return formact_action


def get_dynamic_keywords(actions):
    '''
    根据action 得到关键词
    :param actions:
    :return:
    '''
    dynamic_action_list = []
    if isinstance(actions,list):
        for action in actions:
            for key,value in action.items():
                dynamic_action_list.append(key)
    elif isinstance(actions,dict):
        for key, value in actions.items():
            dynamic_action_list.append(key)
    return  dynamic_action_list

def  __parse_step_string(steps,staticActions,key=None,variables=None):
    '''
    解析步骤中的字符串
    e.g
        "${open()},${click()}",
        "${open()}",
        "${chrome_open()}",
    '''

    dict_step = {}
    dynamic_func = get_dynamic_name(steps)

    if not key:
        dynamic_list = __parse_dynamic_action(dynamic_func, staticActions)
        keys = '_'.join([str(i) for i in dynamic_func])
        dict_step[keys] = dynamic_list

    if  not dynamic_func:
        static_method_list = []
        static_method = convert_func_list(key,steps,variables)
        static_method_list.append(static_method)
        dict_step[key] = static_method_list
    if dynamic_func and key :

        dynamic_list = __parse_dynamic_action(dynamic_func,staticActions)
        dict_step[key] = dynamic_list

    return dict_step

def __parse_dynamic_action(dynamic,action):
    '''
    解析动态action
    :param dynamic:  ['open', 'add']
    :param actions:  已经解析好的action(关键词)
    :return:
    '''

    new_value_list = []
    for index in range(len(dynamic)):
        if  dynamic[index] in action.keys():
            method_list = action[dynamic[index]]
            if len(method_list) == 1:
                new_value_list.append(method_list[0])
            if len(method_list) > 1:
                for method in method_list:
                    new_value_list.append(method)
        else:
            err = "{key}关键字并不存在，请自行添加或者查询关键字添加方法".format(key=dynamic[index])
            logger.error(err)
            raise NameError(err)

    return new_value_list

def get_dynamic_name(func):

    '''
    动态获取关键词的方法
    :param func:   {"click":"${open()},${add()}"}
    :return:
    '''
    function_regexp =  r"\$\{([\w_]+\([\$\w\.\-/_ =,]*\))\}"
    try:
        value = re.findall(function_regexp,func)
        value_list = []
        for v in value:
            new_value = v.split("()")
            value_list.append(new_value[0])
        return value_list
    except TypeError:
        return None

def __parse_step_dict(step,staticActions,variables=None):
    '''
    解析步骤中的字典类型
    e.g
        {
            "open": "${open()},${click()}",
            "click": "id|btn"
        },
    '''

    for key,value in step.items():
        if isinstance(value,str):
            new_dict = __parse_step_string(value,staticActions,key,variables)
    return new_dict

def __parse_step_list(steps,staticActions,key,variables=None):
    '''
    [
        {"click": "id|btn"},
        "${open()},${click()}",
        {"click":"${open()}"}
    ]
    '''
    return_dict ,dict_step,list_step  ={}, {},[]
    for step in steps:
        if isinstance(step,str):
            dict_step = __parse_step_string(step,staticActions,variables=variables)
        if isinstance(step,dict):
            dict_step = __parse_step_dict(step,staticActions,variables)

        for k,value in dict_step.items():
            for v in value:
                list_step.append(v)
    return_dict[key] = list_step
    return return_dict

def parse_step(steps,staticActions,variables=None):
    '''
    "case_step": [
                {"open_click":"${open()},${click()}"},
                {"open":"https://www.xinlang.com"},
                "${open()},${click()}",
                {"my_action":[{"click": "id|btn"},{"click":"${open()}"}]}
            ]
    '''
    new_step = []
    for step in steps:

        if isinstance(step, str):
            dict_step = __parse_step_string(step, staticActions,variables=variables)
        if isinstance(step, dict):
            for k, v in step.items():
                if isinstance(v, (list,)):
                    dict_step = __parse_step_list(v, staticActions,k,variables)
                if isinstance(v,str):
                    dict_step = __parse_step_string(v,staticActions,k,variables)

        new_step.append(dict_step)
    return new_step


def parse_para(parameters):
    '''
    "parameter": [
        {"username": ["123","456"]},
        {"password": ["abc","edf"]},
      ],
    '''
    para_list = []
    for item in parameters:
        for key,value in item.items():
            para,list_p = {},[]
            for v in value:

                para[key] = v
                list_p.append(para)
                para = {}
            para_list.append(list_p)
    from serunner.utils import gen_para_list
    final_para = gen_para_list(*para_list)

    return final_para

def parse_tests(testcases):
    '''
    解析testcases
    '''

    parsed_testcases_list = []
    for test_case in testcases:
        testcase_global = test_case.setdefault("global", {})

        test_suite_each_case = test_case["testcases"]
        new_suite_each_case = []
        for each_case in test_suite_each_case:
            # 获取用例中的可变参数
            config_parameters = each_case.pop("parameter", [])
            final_para = parse_para(config_parameters)
            for para in final_para:
                from serunner.utils import deepcopy_dict,update_deepcopy_data

                new_variable = update_deepcopy_data(testcase_global.get("variables", {}),para)
                #获取全局变量中的actions
                override_actions = deepcopy_dict(testcase_global.get("action", {}))

                # 获取全局变量中的actions
                static_actions = get_format_action(override_actions,new_variable)



                ovrerider_case = deepcopy_dict(each_case)


                parse_after_step = parse_step(ovrerider_case['steps'],static_actions,new_variable)


                ovrerider_case["parameter"] = para

                ovrerider_case["steps"] = parse_after_step

                new_suite_each_case.append(ovrerider_case)

        testcase_global.pop("action")
        test_case["testcases"] = new_suite_each_case
        parsed_testcases_list.append(test_case)
    return parsed_testcases_list










