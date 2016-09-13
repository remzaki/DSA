import pytest
import logging
from lib.base import *
from lib.actions import Actions
from lib.log import Logger
from lib.parser import Parser

logger = Logger()
data = Parser().get_datadict()
# data = {}


class TestSequenceMeta(type):
    """ The dynamic test generator
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

                    if step+1 == config.stop_at_step:
                        # breakpoint here below when debugging
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

    @classmethod
    def setup_class(cls):
        BaseTest.setup_class()

    __metaclass__ = TestSequenceMeta

if __name__ == '__main__':
    pytest.main(config.parallel)
