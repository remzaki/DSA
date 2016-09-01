import pytest
import logging
from lib.base import *
from lib.actions import Actions
from lib.log import Logger
from lib.parser import Parser

# from lib.elements import Elements
# awww = Elements()
# aww = awww.dict
# e = 'applicant_dob_fld'
# aw = aww[e]
# for dat in aw:
#     print dat


logger = Logger()
data = Parser().get_datadict()
# data = {}


class TestSequenceMeta(type):
    """ The dynamic test generator
    The quick brown fox jumps over the lazy dog
    """

    def __new__(mcs, name, bases, dict):
        def gen_test(testdatas):
            def gen(self):
                log_name = '%s-%s' % (self.__name__, self.desired_capabilities['browserName'])
                logger.setup_logger(log_name, '%s.log' % log_name, level=logging.DEBUG)
                log = logging.getLogger(log_name)
                log.info('Executing Test: %s', self.__name__)

                self.assertTrue(testdatas is not None)
                actions = Actions()
                for step, d in enumerate(testdatas):
                    cmd = d[0].lower()
                    param1 = d[1].replace('"', '')
                    param2 = d[2]
                    p = [param1, param2]
                    if cmd != '':
                        do = getattr(actions, cmd)
                        do(step+1, self, p)
                    if step+1 == 93:
                        pass

            return gen

        for s, tests in data.items():
            suite = s.replace('\'', '').strip().replace(' ', '_')
            name = suite
            # print '-'+suite
            for n, test in tests.items():
                test_name = n.replace('\'', '').strip().replace(' ', '_')
                # print '--'+test_name
                # print('---%s' % test)
                if test_name.split('_', 1)[0] != 'test':
                    test_name = 'test_%s' % test_name
                dict[test_name] = gen_test(test)

        return type.__new__(mcs, name, bases, dict)


@on_platforms(platforms)
class TestClass(BaseTest):
    for s, tests in data.items():
        suite = s.replace('\'', '').strip().replace(' ', '_')

    @classmethod
    def setup_class(cls):
        BaseTest.setup_class()

    __metaclass__ = TestSequenceMeta

    def est_abc(self):
        pass
        # from selenium.common.exceptions import TimeoutException
        # from selenium.webdriver.support.ui import WebDriverWait
        # from selenium.webdriver.support import expected_conditions as EC
        # from selenium.webdriver.common.by import By
        #
        # self.driver.get('https://model.uhone.com/Quote/QuoteCensus')
        # try:
        #     element_present = EC.presence_of_element_located((By.CSS_SELECTOR, 'title'))
        #     WebDriverWait(self.driver, timeout=5).until(element_present)
        #     actual_title = "UHOne"
        # except TimeoutException:
        #     pass
        # a = self.driver.find_element_by_css_selector('#a')
        # a.send_keys()
        # self.driver.implicitly_wait()
        # print self.driver.title
        # self.assertEqual(self.driver.title, actual_title,
        #                  'Title does not match with expected: %s with %s' % (self.driver.title, actual_title))


if __name__ == '__main__':
    pytest.main(config.parallel)
