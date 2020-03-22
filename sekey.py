from  serunner.kselenium import  KSelenium

_KW = None
def _get_global():
	global _KW
	if _KW is None:
		_KW = KSelenium()
	return _KW

class KeyWord():

    def start_chrome(self,url=None,headless=None):
        '''
        初始化浏览器
        定义actions e.g
        format_1
        {"start_chrome":"url=https://devstore.01hour.com"|headless=True"}
            headless  True不开启桌面模式 ，默认开启桌面模式
        format_2
        {"start_chrome":"url=https://devstore.01hour.com"}
        or
        {"start_chrome":"headless=True"}
        format_3
        {"start_chrome":""}
        '''
        return _get_global().chrome_init(url,headless)
    def end_chrome(self):
        '''
        关闭浏览器
        定义actions e.g
        {"end_chrome":""}
        '''
        _get_global().kill_browser()
    def open(self,url):
        '''
        打开链接
        定义actions e.g
        {"open":"url=https://devstore.01hour.com"}
        '''
        _get_global().open_url(url)

    def click(self,type,value):
        '''
        元素点击
        定义actions e.g
        {"click":"type=id|value=login-btn"}
        '''
        _get_global().click(type,value)
    def js_click(self,css):
        '''

        定义actions e.g
        {"click":""}
        '''
        _get_global().js_click(css)

    def click_wait(self,type=None,value=None,time=5):
        '''
        元素点击
        定义actions e.g
        {"click_wait":"type=id|value=login-btn|time=10"}
        '''

        element = _get_global().find_wait(type,value,time)
        element.click()

    def get_attribute(self,type,value,attribute):
        '''
        获取元素属性
        定义actions e.g
        {"get_attribute":"type=id|value=login-btn|attribute=src"}
        '''

        return _get_global().get_attribute(type,value,attribute)

    def send_key(self,type,value,text):
        '''
        获取元素属性
        定义actions e.g
        {"send_key":"type=id|value=login-btn|text=13131313131"}
        {"send_key":"id|login-btn|13131313131"}
        '''
        _get_global().send_key(type,value,text)

    def is_visible(self,type,value):
        '''
        元素是否可见
        定义actions e.g
        '''

        return _get_global().is_visible(type,value)


    def switch_iframe(self,type,value):
        '''
        切换iframe

        '''
        _get_global().switch_to_frame(type,value)

    def js(self,script):
        return  _get_global().js(script)

    def select_option(self,type,value,option_by,option):

        _get_global().select_option(type,value,option_by,option)

    def max_window(self):
        _get_global().maximize_window()


