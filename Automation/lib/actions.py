from __future__ import print_function
import logging
from lib.config import config
from lib.checkEmail import CheckEmail
from elements import Elements
from selenium.common.exceptions import TimeoutException, \
    StaleElementReferenceException, \
    NoSuchElementException, \
    WebDriverException, \
    UnexpectedAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import os
import locale


class Actions(object):
    """
    Contains all the action method performed in a Test Case.
    """

    def __init__(self):
        # some class variables
        self.elements = Elements()
        self.log = None
        self.w8 = None
        self.asset = None
        self.driver = None
        self.typ = None

    def logger(self, logger_name):
        self.log = logging.getLogger(logger_name)

    def trim_name(self, p):
        """General trimming helper purposes. Arguments:
        p = str(any string)
        """
        if '<' in p:
            p = p.replace('<', '')
            p = p.replace('>', '')
            p = p.strip()
        else:
            p = False

        return p

    def getset_elem(self, driver, elem):
        element = None
        try:
            element = driver.find_element_by_css_selector(elem)
        except Exception, e:
            self.log.error('Get WebElement Exception: %s', e)
            self.asset.assertTrue(False, 'Get WebElement Exception: %s' % e)
        finally:
            return element

    def setup_global(self, obj):
        # declaring global stuffs
        self.asset = obj
        self.driver = self.asset.driver
        self.w8 = WebDriverWait(obj.driver, timeout=config.timeout)

    def testname(self, step, obj, l=None):
        self.logger(obj._testMethodName)
        self.log.info('Test Name: %s', l[0])
        self.setup_global(obj)

    def description(self, step, obj, l=None):
        self.logger(obj._testMethodName)
        self.log.info('Description: ' + l[0])

    def url(self, step, obj, l=None):
        """Method for accessing the webpage URL"""
        self.logger('%s-%s.Actions.url.%s' % (obj._testMethodName, obj.desired_capabilities['browserName'], step))
        self.log.debug('Parameters: ' + l[0] + " | " + l[1])

        driver = obj.driver
        url = l[0]
        exp_title = l[1]

        # access the URL
        # try:
        driver.get(url)
        # except UnexpectedAlertPresentException:
        #     driver.switch_to.alert.accept()
        # driver.implicitly_wait(config.timeout)
        # actual_title = obj.driver.title

        # try:
        #     actual_title = obj.driver.title
        #     element_present = ec.title_is(exp_title)
        #     # WebDriverWait(obj.driver, timeout=5).until(element_present)
        #     self.w8.until(element_present)
        # except TimeoutException:
        #     self.log.error('Expected Page Title is "%s" but current Title is "%s"' % (exp_title, actual_title))

        # if exp_title != actual_title:
        #     self.log.error('Expected Page Title is "%s" but current Title is "%s"' % (exp_title, actual_title))
        #     obj.assertEqual(exp_title, actual_title,
        #                     'Expected Page Title is "%s" but current Title is "%s"' % (exp_title, actual_title))

        try:
            self.w8.until(lambda driver: obj.driver.title.startswith(exp_title))
        except TimeoutException:
            self.log.error('Expected Page Title is "%s" but current Title is "%s"' % (exp_title, obj.driver.title))
            obj.assertEqual(exp_title, obj.driver.title,
                            'Expected Page Title is "%s" but current Title is "%s"' % (exp_title, obj.driver.title))

    def type(self, step, obj, l=None):
        self.typ = l[0].strip()
        pass
        # self.logger('%s-%s.Actions.type.%s' % (obj._testMethodName, obj.desired_capabilities['browserName'], step))
        # self.log.debug('Parameters: ' + l[0] + " | " + l[1])

    def wait(self, step, obj, l=None):
        self.logger('%s-%s.Actions.wait.%s' % (obj._testMethodName, obj.desired_capabilities['browserName'], step))
        self.log.debug('Parameters: ' + l[0] + " | " + l[1])

        driver = obj.driver

        edict = self.trim_name(l[1])
        if edict:
            got_data = self.elements.get_data(edict)
        else:
            edict = got_data = l[1]

        if got_data:
            self.log.debug('Got element "%s" = %s', edict, got_data)
            element = got_data.strip()

            self.log.info('Get WebElement %s', element)
            e = self.getset_elem(driver, element)

            if e is not None:
                try:
                    self.log.debug('Waiting until the element is not displayed')
                    # print('-%s is displayed: %s' % (edict, e.is_displayed()))
                    # print('-%s is enabled: %s' % (edict, e.is_enabled()))
                    presence_of = ec.visibility_of(e)
                    # WebDriverWait(driver, 10).until_not(presence_of)
                    self.w8.until_not(presence_of)
                except TimeoutException, exc:
                    # print('wait(TimeoutException): %s' % exc)
                    self.log.warning('TimeoutExcepion: %s', exc)
                except StaleElementReferenceException, exc:
                    self.log.warning('StaleElementReferenceException: %s', exc)
                except NoSuchElementException, exc:
                    self.log.warning('NoSuchElementException: %s', exc)
                except Exception, exc:
                    # print('wait(Exception): %s' % exc)
                    self.log.warning('Exception: %s', exc)
                    # print('-%s is displayed: %s' % (edict, e.is_displayed()))
                    # print('-%s is enabled: %s' % (edict, e.is_enabled()))
            else:
                self.log.warning('Unable to process element %s = %s', element, e)

        else:
            self.log.error('Element Dictionary "%s" is not found', edict)
            obj.assertTrue(got_data, 'Element Dictionary "%s" is not found' % edict)

    def enter(self, step, obj, l=None):
        self.logger('%s-%s.Actions.enter.%s' % (obj._testMethodName, obj.desired_capabilities['browserName'], step))
        self.log.debug('Parameters: ' + l[0] + " | " + l[1])

        driver = obj.driver
        data = l[0]
        if '$' in data:
            import uuid
            uid = str(uuid.uuid4()).split('-')
            data = data.replace('$', uid[1])
            self.log.info("USERNAME IS %s", data)

        edict = self.trim_name(l[1])
        if edict:
            got_data = self.elements.get_data(edict)
        else:
            edict = got_data = l[1]

        if got_data:
            element = got_data.strip()

            self.log.info('Get WebElement %s', element)
            e = self.getset_elem(driver, element)
            if e is not None:
                # try to know if element field is enabled
                self.log.debug('Check if Element "%s" is Enabled', element)
                enabled = False
                try:
                    enabled = e.is_enabled()
                except Exception, exc:
                    self.log.error('Exception: %s', exc)

                if enabled:  # if its enabled
                    self.log.debug('Clear text then input data "%s"', data)
                    try:
                        e.clear()
                        e.send_keys(data)
                        # self.driver.send_keys(Keys.TAB)
                    except Exception, exc:
                        self.log.error('Exception: %s', exc)
                        obj.assertTrue(False, 'Exception: %s' % exc)

                        # try:
                        #     the_txt = e.text
                        #     if the_txt == '':
                        #         the_txt = e.get_attribute('value')
                        # except StaleElementReferenceException:
                        #     e = self.getset_elem(driver, element)
                        #     the_txt = e.text
                        #     if the_txt == '':
                        #         the_txt = e.get_attribute('value')
                        #
                        # if data not in the_txt:
                        #     self.log.error('Data "%s" was not entered successfully in %s', data, edict)
                        #     obj.assertTrue('Data "%s" was not entered successfully in %s' % (data, edict))
                else:
                    self.log.error('Element %s is not enabled', edict)
                    obj.assertTrue(e.is_enabled(), 'Element %s is not enabled' % edict)
            else:
                # print('element %s is %s' % (edict, e))
                self.log.warning('Unable to process element %s = %s', element, e)

        else:
            self.log.error('Element Dictionary "%s" is not found', edict)
            obj.assertTrue(got_data, 'Element Dictionary "%s" is not found' % edict)

    def pause(self, step, obj, l=None):
        self.logger('%s-%s.Actions.pause.%s' % (obj._testMethodName, obj.desired_capabilities['browserName'], step))
        self.log.debug('Parameters: ' + l[0] + " | " + l[1])

        msg = l[0]
        timer = int(l[1])

        mins, secs = divmod(int(l[1]), 60)
        time_format = '{:02d}:{:02d}'.format(mins, secs)
        self.log.info("%s %s", msg, time_format)

        try:
            while timer:
                mins, secs = divmod(timer, 60)
                time_format = '{:02d}:{:02d}'.format(mins, secs)
                print("%s - %s" % (msg, time_format), end='\r')
                time.sleep(1)
                timer -= 1
        except KeyboardInterrupt:
            self.log.debug("Pause timer interruption")

        self.log.info("Pause timer finish")

    def verify(self, step, obj, l=None):
        self.logger('%s-%s.Actions.verify.%s' % (obj._testMethodName, obj.desired_capabilities['browserName'], step))
        self.log.debug('Parameters: ' + l[0] + " | " + l[1])

        if ':' in l[0]:
            data = l[0].split(':')
        else:
            self.log.error('Method was called but with no proper Instruction on argument')
            obj.assertTrue(False, 'Method was called but with no proper Instruction on argument')

        driver = obj.driver
        way = data[0].strip()
        exp_value = data[1].strip()

        edict = self.trim_name(l[1])
        if edict:
            got_data = self.elements.get_data(edict)
        else:
            edict = got_data = l[1]

        if got_data:
            element = got_data.strip()

            self.log.info('Get WebElement %s', element)
            e = self.getset_elem(driver, element)

            if way.lower() == 'displayed':
                try:
                    presence_of = ec.presence_of_element_located((By.CSS_SELECTOR, element))
                    # WebDriverWait(driver, 10).until(presence_of)
                    self.w8.until(presence_of)
                except TimeoutException, exc:
                    # print('verify() TimeoutException %s' % exc)
                    self.log.warning('TimeoutException: %s', exc)
                except Exception, exc:
                    # print('verify() %s' % exc)
                    self.log.warning('Exception: %s', exc)

                displayed = False
                try:
                    displayed = e.is_displayed()
                except Exception, exc:
                    self.log.error('Checking if Element is Displayed Exception: %s', exc)

                if not displayed:
                    self.log.error('Element not displayed %s[%s]', edict, element)
                    obj.assertTrue(False, 'Element not displayed %s[%s]' % (edict, element))

            elif way.lower() == 'expected':
                act_value = ''
                try:
                    presence_of = ec.presence_of_element_located((By.CSS_SELECTOR, element))
                    e = self.w8.until(presence_of)
                    act_value = e.text
                except TimeoutException, exc:
                    self.log.warning('TimeoutException: %s', exc)
                except Exception, exc:
                    self.log.warning('Exception: %s', exc)

                if act_value.strip() != exp_value:
                    self.log.error('Expected Value does not match with the Actual "%s"!="%s"', exp_value, act_value)
                    obj.assertTrue(False,
                                   'Expected Value does not match with the Actual "%s"!="%s"' % (exp_value, act_value))

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
        if edict:
            got_data = self.elements.get_data(edict)
        else:
            edict = got_data = l[1]

        if got_data:
            self.log.debug('Element %s found with value %s', edict, got_data)
            element = got_data.strip()
            e_enabled = None
            try:
                self.log.debug('Wait until the Element is Clickable')
                enabled = ec.element_to_be_clickable((By.CSS_SELECTOR, element))
                btn = self.w8.until(enabled)
                e_enabled = True
                # self.log.debug('Get Element is_enabled() value')
                # e_enabled = e.is_enabled()
            except TimeoutException, exc:
                self.log.warning('TimeoutException: %s', exc)
            except Exception, exc:
                self.log.warning('Exception: %s', exc)
            finally:
                self.log.debug('Element is_enabled() = %s', e_enabled)

            if e_enabled:
                try:
                    location = btn.location
                    self.log.debug('"%s" location: %s', element, location)
                    driver.execute_script("return arguments[0].scrollIntoView();", btn)
                    driver.execute_script("window.scrollBy(0, -200);")

                    self.log.info('Performing the click on %s', edict)
                    btn.click()
                except Exception, exc:
                    self.log.error('Exception: %s', exc)
                    obj.assertTrue(False, 'Exception: %s' % exc)
            else:
                self.log.warning('PERHAPS WE SHOULD USE JAVASCRIPT CLICK EXECUTION!?')
                obj.assertTrue(False, 'PERHAPS WE SHOULD USE JAVASCRIPT CLICK EXECUTION!?')
                # print('js used')
                # print(driver.execute_script("return document.querySelector('" + element + "')"))
                # js = driver.execute_script(
                #     "var a = document.querySelector('" + element + "');"
                #                                                    "if(typeof(a) != null){"
                #                                                    "a.click();"
                #                                                    "console.log('hello world!')"
                #                                                    "} else{"
                #                                                    "return 'element typeof() is = ' + typeof(a)}")
                # print('js log > %s' % js)

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
        if edict:
            got_data = self.elements.get_data(edict)
        else:
            edict = got_data = l[1]

        if got_data:
            element = got_data.strip()
            if 'select' in element:
                self.log.info('Method is for <select> with <option>')
                e = self.getset_elem(driver, element)

                # try to know if element field is enabled
                self.log.debug('Check if Element "%s" is Enabled', element)
                e_enabled = False
                try:
                    e_enabled = e.is_enabled()
                except Exception, exc:
                    self.log.error('Exception: %s', exc)

                if e_enabled:
                    self.log.info('Loop thru the options and click the right one')
                    try:
                        for opt in e.find_elements_by_tag_name('option'):
                            if opt.text == selection:
                                opt.click()
                                break
                    except Exception, exc:
                        self.log.error('Exception: %s', exc)
                else:
                    self.log.error('Element %s is not enabled', edict)
                    obj.assertTrue(e.is_enabled(), 'Element %s is not enabled' % edict)

            elif 'radio' in element:
                self.log.info('Method is for <input type="radio">')
                if 'questions' in field.lower():
                    self.log.info('Method for all Questions')
                    radio_btns = driver.find_elements_by_css_selector(element)
                    if radio_btns:
                        for i, radio_btn in enumerate(radio_btns):
                            e_id = radio_btn.get_attribute('id')
                            # self.log.debug('Radio button id: %s', e_id)

                            try:
                                # e_enabled = ec.element_to_be_clickable((By.ID, e_id))
                                e_enabled = radio_btn.is_displayed()
                            finally:
                                self.log.debug('Visibility of Element "%s" is %s', e_id, e_enabled)

                            if e_enabled:
                                try:
                                    # wait = WebDriverWait(driver, 3)
                                    btn = self.w8.until(ec.element_to_be_clickable((By.ID, e_id)))
                                    # self.log.debug('Click %s', btn)
                                    btn.click()
                                except TimeoutException, exc:
                                    self.log.warning('TimeoutException: %s', exc)
                                except Exception, exc:
                                    self.log.warning('Exception: %s', e_id)
                    else:
                        self.log.error('Unable to process Element "%s" = %s', element, radio_btns)
                        obj.assertTrue(False, 'Unable to process Element "%s" = %s' % (element, radio_btns))

                elif 'question' in field.lower():
                    self.log.info('Method for a Question')
                    self.log.error('Not yet implemented!')
                    obj.assertTrue(False, 'Not yet implemented!')

                else:
                    self.log.info('Method for normal Radio button')
                    try:
                        # wait = WebDriverWait(driver, 5)
                        btn = self.w8.until(ec.element_to_be_clickable((By.CSS_SELECTOR, element)))
                        self.log.debug('Click %s', btn)
                        btn.click()
                    except TimeoutException, exc:
                        self.log.warning('TimeoutException: %s', exc)
                    except Exception, exc:
                        self.log.warning('Exception: %s', element)

        else:
            self.log.error('Element Dictionary "%s" is not found', edict)
            obj.assertTrue(got_data, 'Element Dictionary "%s" is not found' % edict)

    def choose(self, step, obj, l=None):
        self.logger('%s-%s.Actions.choose.%s' % (obj._testMethodName, obj.desired_capabilities['browserName'], step))
        self.log.debug('Parameters: ' + l[0] + " | " + l[1])

        driver = obj.driver
        arr_values = l[0].split('|')
        arr_keys = l[1].split('|')

        if "ghi_plan" in arr_keys[0]:
            """Get the number of GetHealthInsurance plans found."""
            plan_numbers = "ghi_plan_count"
            got_data = self.elements.get_data(plan_numbers)
            element = got_data.strip()
            plan_found = None
            while plan_found is None:
                try:
                    presence_of = ec.presence_of_element_located((By.CSS_SELECTOR, element))
                    e = self.w8.until(presence_of)
                    plan_found = e.text
                except TimeoutException, exc:
                    self.log.warning('TimeoutException: %s', exc)
                except Exception, exc:
                    self.log.error('Exception: %s', exc)
                    obj.assertTrue(False, 'Exception: %s' % exc)
            scroll_x = int(plan_found) / 10
            if scroll_x > 1:
                """Scrolls down the plan page."""
                x = 0
                while x <= scroll_x:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    x += 1
        edict = self.trim_name(arr_keys[0])
        if edict:
            got_data = self.elements.get_data(edict)
        else:
            got_data = arr_keys[0]

        if got_data:
            element = got_data.strip()

            self.log.info('Retrieve List of Plans')
            flag = False
            plan_list = driver.find_elements_by_css_selector(element)
            if plan_list:
                self.log.info('Check if there is a match')
                for plan in plan_list:  # for each plan
                    score = 0
                    top_score = len(arr_keys) - 1

                    self.log.info('Check if plan "%s" matches', plan)
                    for x in range(1, len(arr_keys)):   # for each details in the plan
                        edict = self.trim_name(arr_keys[x])
                        if edict:
                            got_data = self.elements.get_data(edict)
                        else:
                            edict = got_data = arr_keys[x]

                        if got_data:
                            element = got_data.strip()

                            e = self.getset_elem(plan, element)
                            try:
                                txt = e.text
                                if txt == '':
                                    txt = e.get_attribute('value')
                            except Exception, exc:
                                self.log.error('Exception: %s', exc)
                                obj.assertTrue(False, 'Exception: %s' % exc)

                            val = arr_values[x].strip()

                            if "." in val:  # check if value has a decimal, if true then convert it as a currency
                                try:
                                    val = '${:.2f}'.format(float(val))
                                except Exception, exc:
                                    self.log.error('Float Format Exception: %s', exc)
                                    obj.assertTrue(False, 'Float Format Exception: %s' % exc)
                            else:
                                try:  # try to convert it into a integer
                                    val = '${:,d}'.format(int(val))
                                except Exception, exc:
                                    # ignore Exceptions
                                    self.log.warning('Int Format Exception: %s', exc)

                            if txt == val:
                                score += 1
                                self.log.debug('Point score %d/%d from %s', score, top_score, txt)
                        else:
                            self.log.error('Element Dictionary "%s" is not found', edict)
                            obj.assertTrue(got_data, 'Element Dictionary "%s" is not found' % edict)

                    if score == top_score:
                        self.log.debug('Found a match %d/%d', score, top_score)
                        try:
                            location = e.location
                            self.log.debug('"%s" location: %s', element, location)
                            driver.execute_script("return arguments[0].scrollIntoView();", e)
                            driver.execute_script("window.scrollBy(0, -200);")

                            self.log.debug('Click Element "%s"', element)
                            e.click()
                            flag = True
                            break
                        except Exception, exc:
                            self.log.error('Exception: %s', exc)
                            obj.assertTrue(False, 'Exception: %s' % exc)
            else:
                self.log.error('Unable to process Element "%s" = %s', element, plan_list)
                obj.assertTrue(False, 'Unable to process Element "%s" = %s' % (element, plan_list))

            if not flag:
                self.log.error('%s Plan was not found with details %s', score, arr_values)
                obj.assertTrue(False, '%s Plan was not found with details %s' % (score, arr_values))

        else:
            self.log.error('Element Dictionary "%s" is not found', edict)
            obj.assertTrue(got_data, 'Element Dictionary "%s" is not found' % edict)

    def check(self, step, obj, l=None):
        """Method for accessing the sent email"""
        self.logger('%s-%s.Actions.check.%s' % (obj._testMethodName, obj.desired_capabilities['browserName'], step))
        self.log.debug('Parameters: ' + l[0] + " | " + l[1])
        checkEmail = CheckEmail()

        if ':' in l[0]:
            data = l[0].split(':')
        else:
            self.log.error('Method was called but with no proper Instruction on argument')
            obj.assertTrue(False, 'Method was called but with no proper Instruction on argument')

        check = data[0].strip()
        exp_value = data[1].strip()

        if check.lower() == 'email':
            url = None
            while not url:
                url = checkEmail.get_link(self.typ)
            exp_title = l[1]
            list_ = [url, exp_title]
            step += .5
            self.url(step, obj, list_)
        else:
            self.log.error('Check command "%s" is not supported', check)
            obj.assertTrue(False, 'Check command "%s" is not supported' % check)
