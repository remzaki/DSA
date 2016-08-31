import unittest
import sys
import new
from selenium import webdriver
from sauceclient import SauceClient
from lib.config import config
from lib.log import Logger
import logging

logger = Logger()
platforms = config.browser


def on_platforms(platforms):
    def decorator(base_class):
        module = sys.modules[base_class.__module__].__dict__
        for i, platform in enumerate(platforms):
            d = dict(base_class.__dict__)
            d['desired_capabilities'] = platform
            # TODO: name = "Test Suite Name"!
            name = "%s_%s" % (base_class.__name__, i + 1)
            module[name] = new.classobj(name, (base_class,), d)

    return decorator


class BaseTest(unittest.TestCase):
    username = None
    access_key = None
    selenium_port = None
    selenium_host = None
    upload = True
    tunnel_id = None
    build_tag = None

    # logger = logging.getLogger('Automation.Base.BaseTest')

    # setUp runs before each test case
    def setUp(self):

        # self.logger.info('execution mode is %s', config.exec_mode)
        # self.logger.info('TESTNAME IS: %s', self._testMethodName)
        # logger.setup_logger('log1', 'log1.txt')
        # log1 = logging.getLogger('log1')
        # log1.info('hi there from log1')

        if config.exec_mode == 'local':
            browser = config.browser[0]['browserName']
            if browser == 'ie':
                self.driver = webdriver.Ie('D:\Automation\Automation\drivers\IEDriverServer')
            elif browser == 'chrome':
                self.driver = webdriver.Chrome('.\drivers\chromedriver.exe')

            self.driver.maximize_window()

        elif config.exec_mode == 'remote':
            # self.desired_capabilities['name'] = self.id()   # Automation.testcase_7.test_testcase_7
            self.desired_capabilities['name'] = self._testMethodName

            if BaseTest.tunnel_id:
                self.desired_capabilities['tunnel-identifier'] = BaseTest.tunnel_id
            if BaseTest.build_tag:
                self.desired_capabilities['build'] = BaseTest.build_tag

            self.driver = webdriver.Remote(
                command_executor="http://%s:%s@%s:%s/wd/hub" %
                                 (BaseTest.username,
                                  BaseTest.access_key,
                                  BaseTest.selenium_host,
                                  BaseTest.selenium_port),
                desired_capabilities=self.desired_capabilities)

    # tearDown runs after each test case
    def tearDown(self):
        status = (sys.exc_info() == (None, None, None))

        if config.exec_mode == 'local':
            if not status:
                self.driver.save_screenshot('.\logs\%s.png' % self.__name__)
        elif config.exec_mode == 'remote':
            sauce_client = SauceClient(BaseTest.username, BaseTest.access_key)
            sauce_client.jobs.update_job(self.driver.session_id, passed=status)
            # test_name = "%s_%s" % (type(self).__name__, self.__name__)
            # with(open('logs\\' + test_name + '.txt', 'w')) as outfile:
            #    outfile.write("SauceOnDemandSessionID=%s job-name=%s\n" % (self.driver.session_id, test_name))

        self.driver.quit()

    @classmethod
    def setup_class(cls):
        cls.build_tag = config.build_tag
        cls.tunnel_id = config.tunnel_id
        cls.username = config.username
        cls.access_key = config.accesskey

        cls.selenium_port = config.selenium_port
        if (cls.selenium_port != '') and (cls.selenium_port is not None):
            cls.selenium_host = "localhost"
        else:
            cls.selenium_host = "ondemand.saucelabs.com"
            cls.selenium_port = "80"