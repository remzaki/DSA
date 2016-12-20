import ConfigParser
from lib.remote import Remote


class config(object):
    """description of class"""

    # DEFAULTS
    config_file = '.\setup.cfg'
    exec_mode = 'local'
    browser = [{'browserName': 'ie'}]
    device = None
    build_tag = None  # get this somewhere
    tunnel_id = None
    selenium_port = None
    username = None
    accesskey = None
    parallelism = None
    parallel = ''
    timeout = 0
    stop_at_step = None

    config = ConfigParser.RawConfigParser()
    config.read(config_file)

    timeout = config.getfloat('setup', 'timeout')
    stop_at_step = config.getint('setup', 'debug_stop')
    server = config.get('setup', 'server_address')
    mode = config.get('setup', 'server_connection')
    release = config.get('setup', 'release')

    exec_mode = config.get('setup', 'execution')
    if exec_mode == 'local':
        browser = config.get('local', 'browser')
        browser = [{'browserName': browser}]
        device = config.get('local', 'device')

    elif exec_mode == 'remote':
        remote = Remote()
        browser = remote.browsers
        username = config.get(exec_mode, 'username')
        accesskey = config.get(exec_mode, 'accesskey')
        tunnel_id = config.get(exec_mode, 'tunnel_id')
        selenium_port = config.get(exec_mode, 'selenium_port')

        parallelism = config.getboolean(exec_mode, 'parallelism')
        if parallelism:
            parallel = config.get(exec_mode, 'parallel')
            parallel = '-n' + parallel
    mail = config.get('email', 'mail')
    m_version = config.get('email', 'm_version')
    email_add = config.get('email', 'email_add')
    SCOPES = config.get('email', 'SCOPES')
    storage_file = config.get('email', 'storage_file')
    client_secret = config.get('email', 'client_secret')
    q_from = config.get('email', 'q_from')
    q_sub_ssq = config.get('email', 'q_sub_ssq')
    q_sub_cq = config.get('email', 'q_sub_cq')
    q_sub_scq = config.get('email', 'q_sub_scq')
    q_sub_baa = config.get('email', 'q_sub_baa')
