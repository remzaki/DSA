from platform import system, release
import pytest
import logging
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.remote_connection import RemoteConnection

import lib.log
import lib.pre as pre
import lib.config as config
import lib.parser as parser
import lib.remote as remote

logger = lib.log.Logger()
logger.setup_logger('Automation.conftest', 'Automation.log', rotate=True)
log = logging.getLogger('Automation.conftest')
log.info('Automation log started')

browsers = remote.Remote.browsers


def pytest_addoption(parser):
    print "pytest_addoption()"
    parser.addoption("--path", action="store", default=None, help="run all combinations")


def pytest_generate_tests(metafunc):
    print "pytest_generate_tests()"

    # load up the settings
    config.setup_configs(metafunc.config.option.path)

    browser_list = browsers
    if pre.config['execution'] == 'local':
        browser_list = [{'browserName': pre.config['browser'], 'platform': "%s %s" % (system(), release())}]
    parse = parser.Parser(metafunc.config.option.path)
    test_cases = parse.get_datadict()
    tests = parser.proliferate(browser_list, test_cases)

    if 'driver' in metafunc.fixturenames:
        metafunc.parametrize('data',
                             tests,
                             ids=[value['TestName'] for value in tests],
                             scope='function')


@pytest.yield_fixture(scope='function')
def driver(request, data):
    """Driver Configuration"""
    # if the assignment below does not make sense to you please read up on object assignments.
    # The point is to make a copy and not mess with the original test spec.
    desired_caps = dict()
    test_name = request.node.name
    username = pre.config['username']
    access_key = pre.config['access_key']

    web_driver = None
    selenium_endpoint = "https://%s:%s@ondemand.saucelabs.com:443/wd/hub" % (username, access_key)
    if pre.config['execution'] == 'remote':
        desired_caps.update(data['browser'])
        desired_caps['tunnelIdentifier'] = pre.config['tunnel_id']
        desired_caps['name'] = test_name

        executor = RemoteConnection(selenium_endpoint, resolve_ip=False)
        web_driver = webdriver.Remote(
            command_executor=executor,
            desired_capabilities=desired_caps
        )
    else:
        if pre.config['browser'] == 'ie':
            web_driver = webdriver.Ie('.\drivers\IEDriverServer.exe')
        elif pre.config['browser'] == 'chrome':
            web_driver = webdriver.Chrome('.\drivers\chromedriver.exe')
        elif pre.config['browser'] == 'firefox':
            web_driver = webdriver.Firefox()
        elif pre.config['browser'] == 'mobile':
            mobile_emulation = {'deviceName': pre.config['device']}
            chrome_opts = webdriver.ChromeOptions()
            chrome_opts.add_experimental_option('mobileEmulation', mobile_emulation)
            web_driver = webdriver.Chrome(executable_path='.\drivers\chromedriver.exe', chrome_options=chrome_opts)

    # This is specifically for SauceLabs plugin.
    # In case test fails after selenium session creation having this here will help track it down.
    # creates one file per test non ideal but xdist is awful
    if web_driver is not None:
        if pre.config['execution'] == 'local':
            web_driver.maximize_window()
        web_driver.implicitly_wait(pre.config['timeout'])
        # with open("%s.testlog" % browser.session_id, 'w') as f:
        #     f.write("SauceOnDemandSessionID=%s job-name=%s\n" % (web_driver.session_id, test_name))
    else:
        raise WebDriverException("Never created!")

    yield web_driver
    # Teardown starts here
    # report results
    log.info("Teardown/Report")
    try:
        if pre.config['execution'] == 'remote':
            web_driver.execute_script("sauce:job-result=%s" % str(not request.node.rep_call.failed).lower())
        web_driver.quit()
    except WebDriverException, exc:
        log.warning('Warning: The driver failed to quit properly. Exception: %s', exc)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    print "pytest_runtest_makereport()"
    # this sets the result as a test attribute for SauceLabs reporting.
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # set an report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"
    setattr(item, "rep_" + rep.when, rep)
