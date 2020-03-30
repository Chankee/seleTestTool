
# 工具特点

- 用例的编写采用json格式，测试用例，测试数据与代码实现分离，可观性舒适，可维护性强
- 采用关键字标识脚本，支持拓展关键字
- 命令行统一化脚本执行，多线程运行用例文件
- 基于unnitest类组件用例与多任务执行测试套件
- 拥有日志监控执行脚本的记录
- 支持数据参数化操作

# 用例文件执行

- 运行测试用例集

  ```python
  python script.py -p  ./test_cases
  ```

# json用例文件格式

```json
[
  {
    "global": {
      "name": "登录页面用例集",
      "action": {
        "start_chrome": "headless=True",
        "open": "$url",
        "click": "id|login-btn",
        "get_attribute": "css|#account-select > option:nth-child(2)|value",
        "end_chrome": ""
        },

      "variables": {
        "url": "https://devstore.01hour.com/login"
      }
    }

  },
      {
      "test":{
        "name": "用户登录界面",   
         "parameter": [
          {"username": ["13413413413","13513513515"]},
          {"password": ["qwerty123456","123.,.kjgy"]}
        ],
        "steps": [
          "${start_chrome()}",
          "${open()}",
          {"input_user_pwd": [
                  {"send_key": "id|login-username|$username"},
                  {"send_key": "id|login-password|$password"}
                 ]
          },
          "${click()}",
          {"result": ["${get_attribute()}"]},
          "${end_chrome()}"
        ],
        "fact_result": ["result"],
        "assert": [
          {"str_eq": ["$result", 0]},
          {"str_eq": ["$result", 0]}
        ]
       }
  }
   
]
```

# json 用例字段的解析

```json
 [
         {
          	  "global": {
                 "name": "",
				"action":{
                    
                  },
                  "variables":{
                      
                  }
       		   }
          },

          {
               "test": {...}
           },
           {
                "test": {...}
           }
]
```

- 一个json文件对应一个测试用例集

- 一个用例集里面包含多个测试用例

- 测试用例里面包含测试步骤，结果验证，数据参数化

- 以每个page的操作为例子，json中key值global对应是一个用例集中的全局变量，所有的test都可以使用global的value

| 键值   | 解析           | 是否必须 |
| ------ | -------------- | -------- |
| name   | 测试用例的名称 | True     |
| action | 定义页面的事件 | False    |
|        | 声明变量       | False    |

- key值为test的对应的value为每个测试用例的内容

| 键值        | 解析                                  | 是否必须 |
| ----------- | ------------------------------------- | -------- |
| name        | 测试用例的名称，或者操作步骤的名称    | False    |
| parameter   | 数据参数化，以列表的形式展示          | False    |
| steps       | 页面的操作步骤，采用关键字+参数的形式 | True     |
| fact_result | 提取需要验证的值                      | False    |
| assert      | 预期与实际结果进行验证                | False    |

### 后期计划
- 基于这个框架，用Django开发可视化平台
- 框架采用restful-framework格式