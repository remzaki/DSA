import os
import unittest
import sys
import new
import time
import platform
from selenium import webdriver
from sauceclient import SauceClient
from lib.config import config
from lib.log import Logger
import logging
from lib.platformCount import *
from lib.generateXml import *
from lib.generateHtml import *
from lib.checkEmail import CheckEmail

logger = Logger()
platforms = config.browser
pc = PlatformCount()
checkEmail = CheckEmail()


def on_platforms(platforms):
    def decorator(base_class):
        module = sys.modules[base_class.__module__].__dict__
        for i, platform in enumerate(platforms):
            d = dict(base_class.__dict__)
            d['desired_capabilities'] = platform
            # TODO: name = "Test Suite Name"!
            name = "%s_%s" % (base_class.__name__, i + 1)
            pc.pfCount = i + 1
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
        self.startTime = time.time()
        if config.exec_mode == 'local':
            self.browser = config.browser[0]['browserName']
            if self.browser == 'ie':
                self.driver = webdriver.Ie('.\drivers\IEDriverServer.exe')
            elif self.browser == 'chrome':
                self.driver = webdriver.Chrome('.\drivers\chromedriver.exe')
            elif self.browser == 'firefox':
                self.driver = webdriver.Firefox()
            elif self.browser == 'mobile':
                mobile_emulation = {"deviceName": config.device}
                chrome_options = webdriver.ChromeOptions()
                chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
                self.driver = webdriver.Chrome(executable_path='.\drivers\chromedriver.exe',
                                               chrome_options=chrome_options)

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
        id_ = self.id()
        id_ = id_.split(".")
        tg_name = id_[1]
        tg_name = tg_name + "_" + str(pc.pfCount)
        tc_name = id_[2]
        screenshot = ''

        if config.exec_mode == 'local':
            OS = platform.system() + " " + platform.release()
            browser = self.browser
            if not status:
                self.driver.save_screenshot('.\logs\%s-%s-%s.png' % (self._testMethodName, OS, browser))
                screenshot = os.path.join(os.path.join(os.path.abspath("."), "logs"),
                                          self._testMethodName + '-' + OS + '-' + browser + ".png")
            self.endTime = time.time()
            duration = (self.endTime - self.startTime) + 3

        elif config.exec_mode == 'remote':
            sauce_client = SauceClient(BaseTest.username, BaseTest.access_key)
            sauce_client.jobs.update_job(self.driver.session_id, passed=status)
            # test_name = "%s_%s" % (type(self).__name__, self.__name__)
            # with(open('logs\\' + test_name + '.txt', 'w')) as outfile:
            #    outfile.write("SauceOnDemandSessionID=%s job-name=%s\n" % (self.driver.session_id, test_name))
            self.test_attrib = sauce_client.jobs.get_job_attributes(self.driver.session_id)
            # browser = self.test_attrib["browser"]
            # OS = self.test_attrib["os"]
            if 'platform' in self.desired_capabilities:
                OS = self.desired_capabilities['platform']
            elif 'deviceName' in self.desired_capabilities:
                OS = self.desired_capabilities['deviceName']
            browser = self.desired_capabilities['browserName']
            # logfile = os.path.join(os.path.join(os.path.abspath("."), "logs"),
            #                        self.__name__ + '-' + self.desired_capabilities['browserName'] + ".log")

            sauce_labs_path = 'https://saucelabs.com/beta/tests/'
            screenshot = sauce_labs_path + self.test_attrib["id"]
            duration = self.test_attrib["modification_time"] - self.test_attrib["creation_time"]
        if OS == 'Windows 2008':
            OS = 'Windows 7'
        elif OS == 'Windows 2012':
            OS = 'Windows 8'
        elif OS == 'Windows 2012 R2':
            OS = 'Windows 8 1'

        if '.' in OS:
            OS = OS.replace('.', ' ')
        elog = ''
        logfile = os.path.join(os.path.join(os.path.abspath("."), "logs"),
                               self._testMethodName + '-' + OS + '-' + browser + ".log")
        if not status:
            try:
                with open(logfile) as f:
                    for line in f:
                        if '- ERROR -' in line and not ('.Actions.wait.' in line):
                            if len(line) > 250:
                                elog = line[:250]
                            else:
                                elog = line
                            if '\n' in elog:
                                elog = elog.replace('\n', '')
                            break
                    # log = f.readlines()
            except IOError, exc:
                print exc

        if config.parallelism and config.exec_mode == 'remote':
            tg_name = id_[1] + '-' + OS + '-' + browser

        text_file = os.path.join(os.path.join(os.path.abspath("."), "report"), tg_name + '-' + tc_name + ".txt")
        file_ = open(text_file, "w")
        file_.write(tg_name + '\n')
        file_.write(tc_name + '\n')
        file_.write(str(status) + '\n')
        file_.write(browser + '\n')
        file_.write(OS + '\n')
        file_.write(screenshot + '\n')
        file_.write(logfile + '\n')
        file_.write(elog + '\n')
        file_.write(str(duration))
        file_.close()

        checkEmail.clear_emails()
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

    @classmethod
    def teardown_class(cls):
        pc.pfCount -= 1