import pytest
import logging

import lib.pre as pre
import lib.config as config
import lib.log
from lib.actions import Actions


@pytest.mark.usefixtures('driver', 'data')
class TestClass(object):
    logger = lib.log.Logger()

    def test(self, driver, data):
        self.logger.setup_logger(data['TestName'], '%s.log' % data['TestName'])
        log = logging.getLogger(data['TestName'])
        log.info('test case logging')

        actions = Actions(data['TestName'], driver)
        actions.url()
        actions.click()

        for i, spec in enumerate(data['steps']):
            print i
            print spec
