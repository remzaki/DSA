from logging import getLogger

import lib.pre as pre
import lib.log
import lib.config
from lib.elements import Elements


class Actions(Elements):
    """Action Class contains all the action methods to test the Application"""

    def __init__(self, test_name, driver):
        Elements.__init__(self)
        self.test_name = test_name
        self.log = getLogger(test_name + ".Actions")
        self.driver = driver

    def click(self, step, data, spec):
        log = getLogger('%s.click.%i' % (self.test_name, step))
        log.debug("Param data: " + data)
        log.debug("Param spec: " + spec)

    def url(self, step, data, spec):
        log = getLogger('%s.url.%i' % (self.test_name, step))
        log.debug("Param data: " + data)
        log.debug("Param spec: " + spec)

        self.driver.get('https://gmail.com')
        Elements
