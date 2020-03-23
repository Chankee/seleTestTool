from serunner.log import logger
from serunner.excepetions import DriverNotFound,IncorrectSelectorType,ElementNotFound,JsScriptFailed
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from serunner.kselenium.setting import MAXTIME,MINITIME,DEFAULT_SHOW_MODE_TIMEOUT
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.remote.errorhandler import ElementNotVisibleException
from selenium.webdriver.remote.errorhandler import NoAlertPresentException
from selenium.webdriver.remote.errorhandler import NoSuchWindowException
import time
class Magic:
    def __init__(self, target):
        self.target = target

    def __getattr__(self, item):
        return getattr(self.target, item)

    def magic(self):
        return self.target

class WebDriverMagic(Magic):
    def __init__(self, target):
        super().__init__(target)

class KSelenium(object):
    def __init__(self):
        self.driver = None

    def _get_chrome_options(self,headless):
        '''
        浏览器options参数设置
        :param headlese:
        :return: 设置的option
        '''
        options = ChromeOptions()
        # 设置为开发者模式，防止被各大网站识别出来使用了Selenium
        options.add_experimental_option('excludeSwitches', ['enable-logging'])  # 禁止打印日志
        if str(headless) == "True":
            # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
            options.add_argument('--headless')
        return options
    def _chrome_driver(self,headless):
        '''
        驱动初始化
        :param headless:
        :return: 浏览器驱动
        '''
        chrome_options = self._get_chrome_options(headless)
        driver = Chrome(chrome_options=chrome_options)
        return driver

    def set_driver(self,driver):
        '''
        设置浏览器驱动
        :param driver:
        :return:
        '''
        self.driver = WebDriverMagic(driver)
        logger.info("浏览器驱动设置成功")
    def get_driver(self):
        '''
        获取浏览器驱动
        :return:
        '''
        if self.driver:
            logger.info("浏览器驱动获取成功")
            return self.driver.magic()
    def require_driver(self):
        '''
        获取当前类的驱动
        :return:
        '''
        if not self.driver:
            raise DriverNotFound("请先初始化浏览器")
        return self.driver
    def open_url(self,url):
        self.require_driver().get(url)
    def _start_plan(self,browser,url=None):
        self.set_driver(browser)
        if url is not None:
            self.open_url(url)
        self.get_driver()
    def chrome_init(self,url=None, headless=False):
        '''
        谷歌驱动初始化
        :param url:
        :param headless:
        :return:
        '''
        driver = self._chrome_driver(headless)
        return self._start_plan(driver,url)

    def kill_browser(self):
        '''
        关闭浏览器
        :return:
        '''
        time.sleep(DEFAULT_SHOW_MODE_TIMEOUT)
        self.require_driver().quit()
        self.driver = None
    def _find_element(self,type,value,timeout=MAXTIME):
        '''
        寻找页面元素(默认5秒时间)
        :param type:  选择器
        :param value: 选择器值
        :param timeout:  设置等待时间
        :param waitDisplay: 是否设置 元素等待显示
        :return:  返回页面元素
        '''
        selector_list = ["id", "name", "link_text", "partial_link_text", "css", "xpath", "tag_name","class"]
        if type not  in selector_list:
            raise IncorrectSelectorType('选择器{type}有误'.format(type=type))
        element = None
        start_time = time.time()
        wait_time = lambda : timeout - (time.time()-start_time)
        while element is None:
            try:
                if type == 'id':
                    element = self.require_driver().find_element_by_id(value)
                elif type == 'css':
                      element = self.require_driver().find_element_by_css_selector(value)
                elif type == 'link_text':
                    element = self.require_driver().find_element_by_link_text(value)
                elif type == 'partial_link_text':
                    element = self.require_driver().find_element_by_partial_link_text(value)
                elif type == 'name':
                    element = self.require_driver().find_element_by_name(value)
                elif type == 'xpath':
                    element = self.require_driver().find_element_by_xpath(value)
                elif type == 'tag_name':
                    element = self.require_driver().find_element_by_tag_name(value)
                elif type == 'class':
                    element = self.require_driver().find_element_by_class_name(value)
                else:
                    err = "选择器{type}类型有误".format(type=type)
                    logger.error(err)
                    raise  IncorrectSelectorType(err)
                logger.debug('找到页面元素:  {type}{value}'.format(type=type,value=value))
            except:
                if wait_time() < 0:
                    # 触发跳出循环条件
                    break
                else:
                    time.sleep(1)
                    logger.error("页面元素还没有找到，剩余查找时间{:.2f}".format(wait_time()))
        if  not element:
            # raise ElementNotFound("页面元素没有找到，使用{type}选择器".format(type=type))
            return None
        else:
            return element
    def _find_elements(self,type,value):
        '''
        查找一组元素
        :param type:
        :param value:
        :return:  返回列表的elements
        '''
        selector_list = ["id", "name", "link_text", "partial_link_text", "css", "xpath", "tag_name","class"]

        if type not in selector_list:
            raise IncorrectSelectorType('选择器{type}有误'.format(type=type))

        if type == "id":
            webelements = self.require_driver().find_elements_by_id(value)
        elif type == "css":
            webelements = self.require_driver().find_elements_by_css_selector(value)
        elif type == "link_text":
            webelements = self.require_driver().find_elements_by_link_text(value)
        elif type == "partial_link_text":
            webelements = self.require_driver().find_elements_by_partial_link_text(value)
        elif type == "name":
            webelements = self.require_driver().find_elements_by_name(value)
        elif type == "xpath":
            webelements = self.require_driver().find_elements_by_xpath(value)
        elif type == "tag_name":
            webelements = self.require_driver().find_elements_by_tag_name(value)
        elif type == "class":
            webelements = self.require_driver().find_elements_by_class_name(value)
        else:
            err = '选择器类型不存在'
            logger.error(err)
            raise IncorrectSelectorType(err)
        return  webelements
    def _find_wait(self, type,value,time):
        '''

        :param locator:
        :return:
        '''
        locator = None
        if type == "id":
            locator = (By.ID, value)
        elif type == 'name':
            locator = (By.NAME, value)
        elif type == "class":
            locator = (By.CLASS_NAME, value)
        elif type== "link_text":
            locator = (By.LINK_TEXT, value)
        elif type == "xpath":
            locator = (By.XPATH, value)
        elif type == "css":
            locator = (By.CSS_SELECTOR, value)
        else:
            raise IncorrectSelectorType(
                "请输入正确的elements：id','name','class','link_text','xpath','css'."
            )
        element = WebDriverWait(self.require_driver(), time, 1).until(EC.presence_of_element_located(locator))
        return element

    def wait_for_element_visible(self,type,value,timeout=MAXTIME):
        """
        等待元素，如果该元素在页面上存在且可见。返回element

        """
        element = None
        start_time = time.time()
        wait_time = lambda: timeout - (time.time() - start_time)
        while element is None:
            try:
                element = self._find_element(type,value)
                if element.is_displayed():
                    return element
                else:
                    element = None
            except:
                if wait_time() < 0:
                    # 触发跳出循环条件
                    break
                else:
                    time.sleep(0.5)
                    logger.error("元素还没有找到，剩余查找时间{:.2f}".format(wait_time()))
        if not element:
                raise  ElementNotVisibleException("元素等待{time}秒后，依然无法可见".format(time=time))

    def maximize_window(self):
        self.driver.maximize_window()
        time.sleep(DEFAULT_SHOW_MODE_TIMEOUT)

    def get_url(self):
        '''
        得到浏览器的url
        :return:
        '''
        return self.require_driver().current_url

    def get_title(self):
        '''
        得到浏览器的标题
        :return:
        '''
        return self.require_driver().title


    def js(self,script):
        '''
        执行js脚本
        :param script:
        :return:
        '''
        try:
            return self.require_driver().execute_script(script)
        except:
            err = "使用js脚本点击失败"
            logger.error(err)
            raise JsScriptFailed(err)

    def js_click(self, css):
        """
        采用js点击
        e.g
        driver.js_click('#buttonid')
        """
        t1 = time.time()
        js_str = "$('{0}').click()".format(css)
        self.js(js_str)



    def send_key(self, type, value, text):
        '''

        '''
        element = self._find_element(type,value)
        element.send_keys(text)

    def click(self,type,value):
        '''
        元素点击
        '''
        result = None
        start_time = time.time()
        wait_time = lambda : MAXTIME- (time.time()-start_time)
        print (wait_time())
        while result is None:
            try:
                if self.is_element_visible(type,value):
                    element =self._find_element(type,value)
                    element.click()
                    result = True
                if wait_time() < 0:
                    # 触发跳出循环条件
                    break
                else:
                    time.sleep(0.5)
                    logger.error("click元素没有可见，剩余查找时间{:.2f}".format(wait_time()))
            except:
                if wait_time() < 0:
                    # 触发跳出循环条件
                    break
                else:
                    time.sleep(0.5)
                    logger.error("click元素还没有找到，剩余查找时间{:.2f}".format(wait_time()))
        if result is None:
            raise  Exception("元素还没有找到,执行点击失败")


    def get_attribute(self,type,value,attribute):


        element = self._find_element(type,value)
        time.sleep(DEFAULT_SHOW_MODE_TIMEOUT)
        if element:
            return element.get_attribute(attribute)
        return  None


    def is_element_present(self,type, value):
        """
        判断 指定的元素选择器是否出现在页面上。
        """
        try:
            self._find_element(type,value)
            return True
        except Exception:
            return False

    def is_element_visible(self,type,value):
        '''
        判断元素是否可见
        '''
        try:
            element = self._find_element(type,value)
            result = element.is_displayed()
            return result
        except Exception:
            return False

    def is_text_visible(self,type,value,text):
        '''
        指定的选择器中文本是否可见。
        '''
        try:
            element = self._find_element(type,value)
            result = element.is_displayed() and text in element.text
            return result
        except Exception:
            return False

    def find_visible_elements(self,type,value):
        """
        寻找一组可见的elements
        """
        elements = self._find_elements(type,value)
        try:
            new_elements = [element for element in elements if element.is_displayed()]
            return new_elements
        except (StaleElementReferenceException, ElementNotVisibleException):
            return []

    def wait_switch_to_alert(self,timeout=MAXTIME):
        '''
        等待切换到弹框
        :return:
        '''
        alert = None
        start_time = time.time()
        wait_time = lambda : timeout - (time.time()-start_time)
        while alert is None:
            try:
                alert = self.require_driver().switch_to.alert
            except NoAlertPresentException:
                if wait_time() < 0:
                    # 触发跳出循环条件
                    break
                else:
                    time.sleep(0.5)
                    logger.error("弹框还没有找到，剩余查找时间{:.2f}".format(wait_time()))

        if not alert:
            raise Exception(" %s 秒后,弹框没有找到 after %s seconds!" % time)
        else:
            return alert

    def wait_accept_alert_text(self,time=MAXTIME):
        """
        从弹框中获取文本
        """
        alert = self.wait_switch_to_alert(time)
        alert_text = alert.text
        alert.accept()
        return alert_text

    def wait_for_and_dismiss_alert(self, time=MAXTIME):
        """
        弹框消息并且获取弹框文本
        """
        alert = self.wait_switch_to_alert(time)
        alert_text = alert.text
        alert.dismiss()
        return alert_text

    def switch_to_frame(self,type,value):
        """
        等待iframe出现
        """
        result = self.is_element_visible(type,value)
        if result:
            element = self._find_element(type,value)
            self.require_driver().switch_to.frame(element)
            return True
        else:
            raise Exception("ifame 不存在")

    def switch_to_default_content(self):
        '''
        退出iframe
        :return:
        '''
        self.require_driver().switch_to.default_content()

    def switch_to_window(self, window, timeout=MINITIME):
        """
        切换窗口
        """
        result = None
        start_time = time.time()
        wait_time = lambda : timeout - (time.time()-start_time)
        if isinstance(window, int):
            while result is None:
                try:
                    window_handle = self.require_driver().window_handles[window]
                    self.require_driver().switch_to.window(window_handle)
                    result = True
                    return True
                except :
                    if wait_time() < 0:
                        # 触发跳出循环条件
                        break
                    else:
                        time.sleep(0.1)
            raise Exception(" %s 后窗口没有找到!" % time)
        else:
            window_handle = window
            while result is None:

                try:
                    self.require_driver().switch_to.window(window_handle)
                    result = True
                    return True
                except NoSuchWindowException:
                    if wait_time() < 0:
                        # 触发跳出循环条件
                        break
                    time.sleep(0.1)
            raise Exception(" %s 后窗口没有找到!" % time)

    def select_option(self,type,value,option_by,option):
            element = self.wait_for_element_visible(type,value)
            try:
                if option_by == "index":
                    Select(element).select_by_index(option)
                elif option_by == "value":
                    Select(element).select_by_value(option)
                else:
                    Select(element).select_by_visible_text(option)
            except (StaleElementReferenceException, ElementNotVisibleException):
                time.sleep(0.05)





