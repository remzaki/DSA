import logging
from lib.config import config
from elements import Elements
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
import locale


class Actions(object):
    """
    Contains all the action method performed in a Test Case.
    """

    elements = Elements()
    log = None

    def logger(self, logger_name):
        self.log = logging.getLogger(logger_name)

    def trim_name(self, p):
        """General trimming helper purposes. Arguments:
        p = str(any string)
        """
        p = p.replace('<', '')
        p = p.replace('>', '')
        p = p.strip()

        return p

    def getset_elem(self, driver, elem):
        element = None
        try:
            element = driver.find_element_by_css_selector(elem)
        except Exception, e:
            self.log.error('Get WebElement Exception: %s', e)
            raise Exception
        finally:
            return element

    def wait_global(self, driver):

        # declaring global variable wait
        self.wait = WebDriverWait(driver, timeout=config.timeout)

    def testname(self, step, obj, l=None):
        self.logger(obj._testMethodName)
        self.log.info('Test Name: ' + l[0])
        self.wait_global(obj.driver)

    def description(self, step, obj, l=None):
        self.logger(obj._testMethodName)
        self.log.info('Description: ' + l[0])

    def url(self, step, obj, l=None):
        """Method for accessing the webpage URL"""
        self.logger('%s-%s.Actions.url.%s' % (obj._testMethodName, obj.desired_capabilities['browserName'], step))
        self.log.debug('Parameters: ' + l[0] + " | " + l[1])

        url = l[0]
        exp_title = l[1]

        # access the URL
        obj.driver.get(url)
        actual_title = obj.driver.title

        # try:
        #     actual_title = obj.driver.title
        #     element_present = ec.title_is(exp_title)
        #     element_present.t
        #     # WebDriverWait(obj.driver, timeout=5).until(element_present)
        #     self.wait.until(element_present)
        # except TimeoutException:
        #     self.log.error('Expected Page Title is "%s" but current Title is "%s"' % (exp_title, actual_title))

        if exp_title != actual_title:
            self.log.error('Expected Page Title is "%s" but current Title is "%s"' % (exp_title, actual_title))
            obj.assertEqual(exp_title, actual_title,
                            'Expected Page Title is "%s" but current Title is "%s"' % (exp_title, actual_title))

    def type(self, step, obj, l=None):
        pass
        # self.logger('%s-%s.Actions.type.%s' % (obj._testMethodName, obj.desired_capabilities['browserName'], step))
        # self.log.debug('Parameters: ' + l[0] + " | " + l[1])

    def wait(self, step, obj, l=None):
        self.logger('%s-%s.Actions.wait.%s' % (obj._testMethodName, obj.desired_capabilities['browserName'], step))
        self.log.debug('Parameters: ' + l[0] + " | " + l[1])

        driver = obj.driver
        edict = self.trim_name(l[1])

        got_data = self.elements.get_data(edict)
        if got_data:
            self.log.debug('Got element "%s" = %s', edict, got_data)
            element = got_data[0].strip()

            t = 3
            self.log.info('Implicit wait of %s seconds', t)
            driver.implicitly_wait(t)

            self.log.info('Get WebElement %s')
            e = self.getset_elem(driver, element)

            if e is not None:
                try:
                    print('-%s is displayed: %s' % (edict, e.is_displayed()))
                    print('-%s is enabled: %s' % (edict, e.is_enabled()))
                    presence_of = ec.visibility_of(e)
                    WebDriverWait(driver, 10).until_not(presence_of)
                except TimeoutException, exc:
                    print('wait(TimeoutException): %s' % exc)
                except StaleElementReferenceException, exc:
                    print(exc)
                except NoSuchElementException, exc:
                    print(exc)
                except Exception, exc:
                    print('wait(Exception): %s' % exc)
                print('-%s is displayed: %s' % (edict, e.is_displayed()))
                print('-%s is enabled: %s' % (edict, e.is_enabled()))
            else:
                print('element is none!!!')


        else:
            self.log.error('Element Dictionary "%s" is not found', edict)
            obj.assertTrue(got_data, 'Element Dictionary "%s" is not found' % edict)

    def enter(self, step, obj, l=None):
        self.logger('%s-%s.Actions.enter.%s' % (obj._testMethodName, obj.desired_capabilities['browserName'], step))
        self.log.debug('Parameters: ' + l[0] + " | " + l[1])

        driver = obj.driver
        data = l[0]
        edict = self.trim_name(l[1])

        got_data = self.elements.get_data(edict)
        if got_data:
            element = got_data[0].strip()
            e = self.getset_elem(driver, element)
            if e is not None:
                if e.is_enabled():
                    try:
                        e.clear()
                        e.send_keys(data)
                        e.send_keys(Keys.TAB)
                    except Exception:
                        raise Exception
                else:
                    self.log.error('Element %s is not enabled', edict)
                    obj.assertTrue(e.is_enabled(), 'Element %s is not enabled' % edict)
            else:
                print('element %s is %s' % (edict, e))
        else:
            self.log.error('Element Dictionary "%s" is not found', edict)
            obj.assertTrue(got_data, 'Element Dictionary "%s" is not found' % edict)

    def pause(self, step, obj, l=None):
        self.logger('%s-%s.Actions.pause.%s' % (obj._testMethodName, obj.desired_capabilities['browserName'], step))
        self.log.debug('Parameters: ' + l[0] + " | " + l[1])

    def verify(self, step, obj, l=None):
        self.logger('%s-%s.Actions.verify.%s' % (obj._testMethodName, obj.desired_capabilities['browserName'], step))
        self.log.debug('Parameters: ' + l[0] + " | " + l[1])

        driver = obj.driver
        data = l[0].split(':')
        way = data[0].strip()
        exp_value = data[1].strip()
        edict = self.trim_name(l[1])

        got_data = self.elements.get_data(edict)
        if got_data:
            element = got_data[0].strip()
            e = self.getset_elem(driver, element)

            if way.lower() == 'displayed':
                try:
                    presence_of = ec.presence_of_element_located((By.CSS_SELECTOR, element))
                    WebDriverWait(driver, 10).until(presence_of)
                    if not e.is_displayed:
                        self.log.error('Element not displayed %s[%s]', edict, element)
                        obj.assertTrue(False, 'Element not displayed %s[%s]' % (edict, element))
                except TimeoutException, exc:
                    print('verify() TimeoutException %s' % exc)
                except Exception, exc:
                    print('verify() %s' % exc)
            elif way.lower() == 'expected':
                act_value = e.text
                try:
                    presence_of = ec.presence_of_element_located((By.CSS_SELECTOR, element))
                    WebDriverWait(driver, 10).until(presence_of)
                    if act_value.strip() != exp_value:
                        self.log.error('Expected Value does not match with the Actual (%s)=(%s)', exp_value, act_value)
                        obj.assertTrue(False,
                                       'Expected Value does not match with the Actual (%s)=(%s)' % (exp_value, act_value))
                except TimeoutException, exc:
                    print('verify() TimeoutException %s' % exc)
                except Exception, exc:
                    print ('verify() %s' % exc)
            else:
                self.log.error('Verify command "%s" is not supported', way)
                obj.assertTrue(False, 'Verify command "%s" is not supported' % way)
        else:
            self.log.error('Element Dictionary "%s" is not found', edict)
            obj.assertTrue(got_data, 'Element Dictionary "%s" is not found' % edict)

    def click(self, step, obj, l=None):
        """Method for clicking an element in the webpage"""
        self.logger('%s-%s.Actions.click.%s' % (obj._testMethodName, obj.desired_capabilities['browserName'], step))
        self.log.debug('Parameters: ' + l[0] + " | " + l[1])

        driver = obj.driver
        edict = self.trim_name(l[1])
        print('-'*10 + edict + '-'*10)

        got_data = self.elements.get_data(edict)
        if got_data:
            self.log.debug('Element %s found with value %s', edict, got_data)
            element = got_data[0].strip()
            e = self.getset_elem(driver, element)

            # try to get the element display status
            # try:
            #     e_displayed = e.is_displayed()
            # except Exception, exc:
            #     print('-display exception: %s' % exc)
            # finally:
            #     print('%s is displayed %s' % (edict, e_displayed))

            # try to get the element enable status
            e_enabled = None
            try:
                enabled = ec.element_to_be_clickable((By.CSS_SELECTOR, element))
                WebDriverWait(driver, 10).until(enabled)
                e_enabled = e.is_enabled()
            except Exception, exc:
                print('-enable exception: %s' % exc)
            finally:
                print('%s is enabled %s' % (edict, e_enabled))

            if e_enabled:
                print('se used')
                e.click()
            else:
                print('js used')
                print(driver.execute_script("return document.querySelector('" + element + "')"))
                js = driver.execute_script(
                    "var a = document.querySelector('" + element + "');"
                                                                   "if(typeof(a) != null){"
                                                                   "a.click();"
                                                                   "console.log('hello world!')"
                                                                   "} else{"
                                                                   "return 'element typeof() is = ' + typeof(a)}")
                print('js log > %s' % js)

            # try:
            #     self.log.debug('Performing click @ %s', e)
            #     driver.implicitly_wait(1)
            #     try:
            #         e = self.getset_elem(driver, element)
            #         enabled = ec.element_to_be_clickable(e)
            #         WebDriverWait(driver, 5).until(enabled)
            #         print('se used')
            #         e.click()
            #     except TimeoutException, exc:
            #         print("Timeout exception %s" % exc)
            #     except Exception, exc:
            #         print('js used')
            #         driver.execute_script("document.querySelector('" + element + "').click()")
            #         print('- %s' % exc)
            #
            # except Exception, exc:
            #     print('-- %s' % exc)

        else:
            self.log.error('Element Dictionary "%s" is not found', edict)
            obj.assertTrue(got_data, 'Element Dictionary "%s" is not found' % edict)

    def select(self, step, obj, l=None):
        self.logger('%s-%s.Actions.select.%s' % (obj._testMethodName, obj.desired_capabilities['browserName'], step))
        self.log.debug('Parameters: ' + l[0] + " | " + l[1])

        driver = obj.driver
        arr = l[0].split(':')
        field = arr[0].strip()
        selection = arr[1].strip()
        edict = self.trim_name(l[1])

        got_data = self.elements.get_data(edict)
        if got_data:
            element = got_data[0].strip()
            if 'select' in element:
                self.log.info('Method is for <select> with <option>')
                e = self.getset_elem(driver, element)
                if e.is_enabled():
                    for opt in e.find_elements_by_tag_name('option'):
                        if opt.text == selection:
                            opt.click()
                            break
                else:
                    self.log.error('Element %s is not enabled', edict)
                    obj.assertTrue(e.is_enabled(), 'Element %s is not enabled' % edict)
            elif 'radio' in element:
                self.log.info('Method is for <input type="radio">')
                if 'questions' in field.lower():
                    self.log.info('Method for all Questions')
                    radio_btns = driver.find_elements_by_css_selector(element)
                    for i, radio_btn in enumerate(radio_btns):
                        e_id = radio_btn.get_attribute('id')
                        self.log.debug('Radio button id: %s', e_id)
                        try:
                            wait = WebDriverWait(driver, 5)
                            btn = wait.until(ec.element_to_be_clickable((By.ID, e_id)))
                            btn.click()
                        except Exception, exc:
                            self.log.warning('select(Exception): This ID is not clickable -> %s', e_id)
                elif 'question' in field.lower():
                    self.log.info('Method for a Question')
                else:
                    self.log.info('Method for normal Radio button')
                    try:
                        wait = WebDriverWait(driver, 5)
                        btn = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, element)))
                        btn.click()
                    except Exception, exc:
                        self.log.warning('select(Exception): This ID is not clickable -> %s', element)

        else:
            self.log.error('Element Dictionary "%s" is not found', edict)
            obj.assertTrue(got_data, 'Element Dictionary "%s" is not found' % edict)

    def choose(self, step, obj, l=None):
        self.logger('%s-%s.Actions.choose.%s' % (obj._testMethodName, obj.desired_capabilities['browserName'], step))
        self.log.debug('Parameters: ' + l[0] + " | " + l[1])

        driver = obj.driver
        arr_values = l[0].split('|')
        arr_keys = l[1].split('|')

        edict = self.trim_name(arr_keys[0])
        got_data = self.elements.get_data(edict)
        if got_data:
            element = got_data[0].strip()

            flag = False
            plan_list = driver.find_elements_by_css_selector(element)
            for plan in plan_list:
                score = 1
                for x in range(1, len(arr_keys)):
                    edict = self.trim_name(arr_keys[x])
                    got_data = self.elements.get_data(edict)
                    if got_data:
                        element = got_data[0].strip()

                        e = self.getset_elem(plan, element)
                        txt = e.text
                        val = arr_values[x].strip()

                        if "." in val:  # check if value has a decimal, if true then convert it as a currency
                            try:
                                val = '${:.2f}'.format(float(val))
                            except Exception, exc:
                                # print(exc)
                                pass
                        else:
                            try:    # try to convert it into a integer
                                val = '${:,d}'.format(int(val))
                            except Exception, exc:
                                # print(exc)
                                pass

                        if txt == val:
                            score += 1
                        # print('%d: %s <VS> %s' % (score, txt, val))
                    else:
                        self.log.error('Element Dictionary "%s" is not found', edict)
                        obj.assertTrue(got_data, 'Element Dictionary "%s" is not found' % edict)

                if score == len(arr_keys)-1:
                    try:
                        e.click()
                        flag = True
                        break
                    except Exception:
                        raise Exception

            if not flag:
                self.log.error('%s Plan was not found with details %s', score, arr_values)
                obj.assertTrue(False, '%s Plan was not found with details %s' % (score, arr_values))

        else:
            self.log.error('Element Dictionary "%s" is not found', edict)
            obj.assertTrue(got_data, 'Element Dictionary "%s" is not found' % edict)
