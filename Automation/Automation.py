import pytest
import logging
from lib.base import *
from lib.actions import Actions
from lib.log import Logger
from lib.parser import Parser
from lib.generateXml import *
from lib.generateHtml import *
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
                if 'platform' in self.desired_capabilities:
                    OS = self.desired_capabilities['platform']
                elif 'deviceName' in self.desired_capabilities:
                    OS = self.desired_capabilities['deviceName']
                else:
                    OS = platform.system() + " " + platform.release()
                if '.' in OS:
                    OS = OS.replace('.', ' ')
                log_name = '%s-%s-%s' % (self._testMethodName, OS, self.desired_capabilities['browserName'])
                logger.setup_logger(log_name, '%s.log' % log_name, level=logging.DEBUG)
                log = logging.getLogger(log_name)
                log.info('Executing Test: %s', self._testMethodName)
                
                self.assertTrue(testdatas is not None)
                actions = Actions()
                actions.log_name = log_name
                actions.platform = OS
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
            if f.endswith(".xml") or f.endswith(".html") or f.endswith(".txt") or f.endswith(".policy_num"):
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

    def teardown_class(cls):
        xresult = TestDict()
        hreport = HTMLClass()
        tg_dict = {}
        path_ = os.path.join(os.path.abspath("."), "report")
        files_ = os.listdir(path_)
        for file_ in files_:
            if file_.endswith('.txt'):
                fyl = os.path.join(path_, file_)
                f = open(fyl, "r")
                a = []
                for line in f:
                    a.append(line.replace('\n', ''))
                f.close()
                key = a[0]
                # check if key is already present in tg_dict
                if key not in tg_dict:
                    tg_dict[key] = []
                # append some value
                tg_dict[key].append(a)
        for key in tg_dict:
            for a in tg_dict[key]:
                values = {}
                passed = 0
                failed = 0
                # Legend:
                # a[0]=testsuite; a[1]=testcase; a[2]=status; a[3]=browser; a[4]=os; a[5]=screenshot; a[6]=log; a[7]=elog; a[8]=duration
                if a[2] == 'True':
                    passed = 1
                else:
                    failed = 1
                values["testsuite"] = key
                values["testcase"] = a[1]
                values["passed"] = str(passed)
                values["failed"] = str(failed)
                values["duration"] = a[8]
                values["browser"] = a[3]
                values["os"] = a[4]
                values["screenshot"] = a[5]
                values["log"] = a[6]
                values["elog"] = a[7]
                xresult.testDict = values
            xresult.create_xml(xresult.testDict)
        hreport.create_html(path_)
        # if os.path.exists(os.path.join(path_, 'report.html')):
        #     filelist = [f for f in files_ if f.endswith(".txt")]
        #     for f in filelist:
        #         os.remove(os.path.join(path_, f))

if __name__ == '__main__':
    pytest.main(config.parallel)