import copy

import sys

py_version_2 = sys.version_info[:3][0]  == 2
py_version_3 = not py_version_2


def deepcopy_dict(data):
    try:
        return copy.deepcopy(data)
    except TypeError:
        copied_data = {}
        for key, value in data.items():
            if isinstance(value, dict):
                copied_data[key] = deepcopy_dict(value)
            else:
                try:
                    copied_data[key] = copy.deepcopy(value)
                except TypeError:
                    copied_data[key] = value

        return copied_data

def gen_para_list(*para):
    '''
    返回数据驱动的参数列表
    '''
    import itertools
    para_list = []
    for item_tuple in itertools.product(*para):
        item_dict = {}
        for item in item_tuple:
            item_dict.update(item)
        para_list.append(item_dict)
    return para_list

def update_deepcopy_data(deepData,notDeepData):

    data = {}
    list = [deepData,notDeepData]
    for new in list:
        data.update(new)
    return data

def get_uniform_comparator(comparator):
    """
    获取验证器
    """
    if comparator in ["eq", "equals", "==", "is"]:
        return "equals"
    elif comparator in ["lt", "less_than"]:
        return "less_than"
    elif comparator in ["le", "less_than_or_equals"]:
        return "less_than_or_equals"
    elif comparator in ["gt", "greater_than"]:
        return "greater_than"
    elif comparator in ["ge", "greater_than_or_equals"]:
        return "greater_than_or_equals"
    elif comparator in ["ne", "not_equals"]:
        return "not_equals"
    elif comparator in ["str_eq", "string_equals"]:
        return "string_equals"
    elif comparator in ["len_eq", "length_equals", "count_eq"]:
        return "length_equals"
    elif comparator in ["len_gt", "count_gt", "length_greater_than", "count_greater_than"]:
        return "length_greater_than"
    elif comparator in ["len_ge", "count_ge", "length_greater_than_or_equals", \
        "count_greater_than_or_equals"]:
        return "length_greater_than_or_equals"
    elif comparator in ["len_lt", "count_lt", "length_less_than", "count_less_than"]:
        return "length_less_than"
    elif comparator in ["len_le", "count_le", "length_less_than_or_equals", \
        "count_less_than_or_equals"]:
        return "length_less_than_or_equals"
    else:
        return comparator


VERSION = '1.0.0'
def get_version():
    import sys
    import platform
    version = '{tools_version} -- ({parse} {type} on {sys_pf} {sys_version})'.format(
                                       tools_version = VERSION,
                                       parse = platform.python_implementation(),
                                       type = sys.version.split()[0],
                                       sys_pf = sys.platform,
                                       sys_version = platform.platform()
                                        )

    return version.strip()

import re
class  Comparators(object):
    '''
    验证器 传入实际结果与预期结果，进行比对
    '''
    def equals(self,result,expect):
        assert  result == expect
    def less_than(self,result,expect):
        assert  result < expect

    def less_than_or_equals(self,result, expect):
        assert result <= expect

    def greater_than(self,result, expect):
        assert result > expect

    def greater_than_or_equals(self,result, expect):
        assert result >= expect

    def not_equals(self,result, expect):
        assert result != expect

    def string_equals(self,result, expect):
        assert str(result) == str(expect)

    def length_equals(self,result, expect):
        assert isinstance(expect, int)
        assert len(result) == expect

    def length_greater_than(self,result, expect):
        assert isinstance(expect, int)
        assert len(result) > expect

    def length_greater_than_or_equals(self,result, expect):
        assert isinstance(expect, int)
        assert len(result) >= expect

    def length_less_than(self,result, expect):
        assert isinstance(expect, int)
        assert len(result) < expect

    def length_less_than_or_equals(self,result, expect):
        assert isinstance(expect, int)
        assert len(result) <= expect

    def contains(self,result, expect):
        assert isinstance(result, (list, tuple, dict, str,bytes))
        assert expect in result

    def contained_by(self,result, expect):
        assert isinstance(expect, (list, tuple, dict, str,bytes))
        assert result in expect

    def regex_match(check_value, expect_value):
        assert isinstance(expect_value, str)
        assert isinstance(check_value, str)
        assert re.match(expect_value, check_value)

    def startswith(check_value, expect_value):
        assert str(check_value).startswith(str(expect_value))

    def endswith(check_value, expect_value):
        assert str(check_value).endswith(str(expect_value))
