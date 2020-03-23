from serunner.utils import deepcopy_dict

class DataTearDown(object):
    def __init__(self, variables=None):
        variable = deepcopy_dict(variables)
        self.VRRIABLE_TEAR_DOWN = variable

    def update_variable(self,newvaribales):
        # 更新变量
        for item in newvaribales:
            for key,value in item.items():
                self.VRRIABLE_TEAR_DOWN["variables"][key] = value
    def assert_result(self,asser_result):
        # 结果验证
        from serunner.parser import parse_assert
        assertor =  parse_assert(asser_result,self.VRRIABLE_TEAR_DOWN["variables"])
        for each in assertor:
            each[0](each[1][0],each[1][1])



