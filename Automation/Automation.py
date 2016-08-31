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
        def gen_test(datas):
            def test(self):
                log_name = '%s-%s' % (self.__name__, self.desired_capabilities['browserName'])
                logger.setup_logger(log_name, '%s.log' % log_name, level=logging.DEBUG)
                log = logging.getLogger(log_name)
                log.info('Executing Test: %s', self.__name__)

                self.assertTrue(datas is not None)
                actions = Actions()
                for step, d in enumerate(datas):
                    cmd = d[0].lower()
                    param1 = d[1].replace('"', '')
                    param2 = d[2]
                    p = [param1, param2]
                    if cmd != '':
                        do = getattr(actions, cmd)
                        do(step+1, self, p)
                    if step+1 == 93:
                        pass

            return test

        for i in data.items():
            name = i[0].replace('\'', '').strip().replace(' ', '_')
            test_name = name
            if name.split('_', 1)[0] != 'test':
                test_name = 'test_%s' % name
            a = i[1]
            # print(a)
            dict[test_name] = gen_test(a)
        return type.__new__(mcs, name, bases, dict)


@on_platforms(platforms)
class TestClass(BaseTest):
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
    # print config.parallel
    pytest.main(config.parallel)
