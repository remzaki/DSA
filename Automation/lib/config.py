import ConfigParser


class config(object):
    """description of class"""

    # DEFAULTS
    # config_file = '.\setup.cfg'
    config_file = 'D:\\Automation\\Automation\\setup.cfg'
    exec_mode = 'local'
    browser = [{'browserName': 'ie'}]
    build_tag = None  # get this somewhere
    tunnel_id = None
    selenium_port = None
    username = None
    accesskey = None
    parallelism = None
    parallel = ''
    timeout = 0

    config = ConfigParser.RawConfigParser()
    config.read(config_file)

    timeout = config.getfloat('setup', 'timeout')

    exec_mode = config.get('setup', 'execution')
    if exec_mode == 'local':
        browser = config.get('local', 'browser')
        browser = [{'browserName': browser}]

    elif exec_mode == 'remote':
        browser = [
            {
                'platform': 'Windows 10',
                'browserName': 'chrome',
                'version': '51.0'
            }
            ,
            {
                'platform': 'Windows 7',
                'browserName': 'internet explorer',
                'version': '11.0'
            }
            ,
            {
               'platform': 'Linux',
               'browserName': 'android',
               'version': '4.3',
               'deviceName': 'Android Emulator',
               'deviceOrientation': 'portrait'
            },
            {
               'platform': 'OS X 10.11',
               'browserName': 'safari',
               'version': '9',
            }
        ]  # get browsers on script
        username = config.get(exec_mode, 'username')
        accesskey = config.get(exec_mode, 'accesskey')
        tunnel_id = config.get(exec_mode, 'tunnel_id')
        selenium_port = config.get(exec_mode, 'selenium_port')

        parallelism = config.getboolean(exec_mode, 'parallelism')
        if parallelism:
            parallel = config.get(exec_mode, 'parallel')
            parallel = '-n' + parallel
