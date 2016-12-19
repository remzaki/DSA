import pytest
import logging
from lib.base import *
from lib.actions import Actions
from lib.log import Logger
from lib.parser import Parser
import os
import shutil
import datetime

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
                self.driver.implicitly_wait(config.timeout)
                for step, d in enumerate(testdatas):
                    cmd = d[0].lower()
                    param1 = d[1].replace('"', '')
                    param2 = d[2]
                    param3 = ''
                    if '#' in cmd:
                        continue
                    try:
                        param3 = d[3]
                    except IndexError:
                        pass
                    p = [param1, param2]
                    if cmd != '':
                        on_mobile = ('ios' in str(self.desired_capabilities).lower()) or\
                                    ('mobile' in str(self.desired_capabilities).lower()) or\
                                    ('android' in str(self.desired_capabilities).lower())
                        flag = True
                        if on_mobile and param3 == 'm-':
                            flag = False
                            log.info('Step %i will be SKIPPED in Mobile setup', step + 1)
                        elif on_mobile and param3 == 'm':
                            log.info('Step %i specific for Mobile setup', step + 1)
                        elif not on_mobile and param3 == 'm':
                            flag = False
                            log.info('Step %i will be SKIPPED since it is specific for Mobile setup', step + 1)

                        if flag:
                            do = getattr(actions, cmd)
                            do(step+1, self, p)

                    if step+1 == config.stop_at_step:
                        # breakpoint here below when debugging
                        pass

                    time.sleep(1)

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
    cwd = os.getcwd()
    tr_folder = "report"
    tr_dir = os.path.join(cwd, tr_folder)
    if os.path.exists(tr_dir):
        folder_name = datetime.datetime.now().strftime("%Y-%m-%d_%H")
        folder = os.path.join(tr_folder, folder_name)
        files = os.listdir(tr_dir)
        for f in files:
            if f.endswith(".xml") or f.endswith(".html"):
                if not os.path.exists(folder):
                    os.makedirs(folder)
                file_ = os.path.join(tr_dir, f)
                if os.path.exists(os.path.join(folder, f)):
                    os.remove(os.path.join(folder, f))
                shutil.move(file_, folder)
    else:
        os.makedirs(tr_dir)

    @classmethod
    def setup_class(cls):
        BaseTest.setup_class()

    __metaclass__ = TestSequenceMeta

if __name__ == '__main__':
    pytest.main(config.parallel)
