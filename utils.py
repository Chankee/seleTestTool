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