
from serunner.log import  logger
import io
import os
import json
from serunner.excepetions import FileFormatError,CaseFileNotFound



def find_file(filePath,fileName):
    '''
    寻找文件
    '''
    file_abspath = None
    while file_abspath is None:
        if os.path.isfile(filePath):
            file_dir_path = os.path.dirname(filePath)

        elif os.path.isdir(filePath):
            file_dir_path = filePath
        else:
            err = "传入的路径有误"
            logger.error(err)
            raise FileNotFoundError(err)
        file_path = os.path.join(file_dir_path,fileName)

        if os.path.isfile(file_path):
            file_abspath = os.path.abspath(file_path)
        else:
            filePath = os.path.dirname(file_dir_path)

    return file_abspath

def find_extend_module(filePath):
    '''
    找拓展模块
    '''
    try:
        extend_py = find_file(filePath,"extend.py")
    except FileNotFoundError:
        return None
    return  extend_py

# def load_project_tests(filePath):
#     extend_py = find_extend_module(filePath)
#     if extend_py:
#         pro_work_dir = os.path.dirname(extend_py)
#         extend_method = parser.parse_extend_module()
#     else:
#         pro_work_dir = os.getcwd()
#         extend_method = {}


    # sys.path.insert(0, pro_work_dir)

def case_json_data(fileName):
    '''
    加载用例的json文件
    '''
    try:
        with io.open(fileName, encoding='utf8') as data:
            try:
                dict_data = json.load(data)
                # 对load成python 格式的内容进行基本判断
                if not dict_data:
                    err = "重载{file}文件的内容为空".format(file=fileName)
                    logger.error(err)
                    raise FileFormatError(err)
                elif not isinstance(dict_data, (list, dict)):
                    err = "{file}文件格式有误".format(file=fileName)
                    logger.error(err)
                    raise FileFormatError(err)

            except Exception as msg:
                logger.error("加载json文件有误：{err}".format(err=msg))
                raise FileFormatError(err)
            return dict_data
    except Exception as msg:
        logger.error(msg)
        raise FileNotFoundError(msg)

def case_folder_list(folderPath):
    '''
    用例文件夹，每一个测试文件以列表返回
    '''
    case_list = []
    for (dir_path, dir_names, file_names) in os.walk(folderPath):
        for file_name in file_names:
            if not file_name.endswith('.json'):
                continue
            case_path = os.path.join(dir_path, file_name)
            case_list.append(case_path)
    return case_list

def load_file(fileName):
    file_format = os.path.splitext(fileName)[1].lower()
    if file_format == '.json':
        return case_json_data(fileName)
    else:
        warn = "不支持当前{file}文件的后缀名格式，".format(file=fileName)
        logger.warning(warn)
        return []


def load_each_case_step(steps):
    case_steps = []
    if "step" in steps:
        pass
    if "suite" in steps:
        pass
    else:
        case_steps.append(steps)
    return case_steps


def load_each_testcase(caseData):
    content_testcase = {
        "global":{},
        "testcases":[]
    }

    if not isinstance(caseData,list):

        logger.warning("测试用例格式错误,你的测试用例类型为{type}，函数需要的是list类型".
                               format(type=type(caseData)))
    for case_data in caseData:
        if not isinstance(case_data, dict):
            raise FileFormatError("测试用例格式错误,用例类型{type}".format(type=type(case_data)))

        for  key,value in case_data.items():
            if key == "global":
                content_testcase["global"].update(value)
            elif key == "test":
                test_list = load_each_case_step(value)
                content_testcase["testcases"].extend(test_list)
            else:
                logger.warning("每一个用例格式中的标志键，入口应该是[test]或者[config]，而本用例用{key}".format(key=key))

    return  content_testcase


def load_each_file_case(path):
    try:
        case_data = load_file(path)
        test_case =  load_each_testcase(case_data)
        test_case['global']['path'] = path
        testcases_list = [test_case]
    except FileFormatError:
        testcases_list = []
    return testcases_list
def load_testcases(path):
    '''
    加载测试用例
    '''
    if isinstance(path, (list, set)):
        cases_list = []

        for case in set(path):
            test_case = load_testcases(case)
            if not test_case:
                continue
            cases_list.extend(test_case)

        return cases_list

    if not os.path.exists(path):
        err_msg = "测试用例的文件 {path}不存在".format(path=path)
        logger.error(err_msg)
        raise CaseFileNotFound(err_msg)

    if not os.path.isabs(path):
        path = os.path.join(os.getcwd(), path)

    if os.path.isdir(path):
        files_list = case_folder_list(path)
        testcases_list = load_testcases(files_list)
    elif os.path.isfile(path):
        testcases_list = load_each_file_case(path)

    return testcases_list








