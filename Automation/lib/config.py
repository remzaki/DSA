import ConfigParser
import logging

import pre
import lib.log


logger = lib.log.Logger()
logger.setup_logger('Automation.config', 'Automation.log', rotate=True)
log = logging.getLogger('Automation.config')
log.info('config.py logging here..')


def setup_configs(path=None):
    cfg_file = 'setup.cfg'
    if path is not None:
        path += '\%s' % cfg_file
    else:
        path = cfg_file

    config = ConfigParser.RawConfigParser()
    config.read(path)

    pre.config['execution'] = config.get('setup', 'execution')
    pre.config['timeout'] = config.getfloat('setup', 'timeout')
    pre.config['debug_stop'] = config.getint('setup', 'debug_stop')
    pre.config['server_connection'] = config.get('setup', 'server_connection')
    pre.config['server_address'] = config.get('setup', 'server_address')
    pre.config['release'] = config.get('setup', 'release')
    pre.config['browser'] = config.get('local', 'browser')
    pre.config['device'] = config.get('local', 'device')
    pre.config['mail'] = config.get('email', 'mail')
    pre.config['m_version'] = config.get('email', 'm_version')
    pre.config['email_add'] = config.get('email', 'email_add')
    pre.config['SCOPES'] = config.get('email', 'SCOPES')
    pre.config['storage_file'] = config.get('email', 'storage_file')
    pre.config['client_secret'] = config.get('email', 'client_secret')
    pre.config['q_from'] = config.get('email', 'q_from')
    pre.config['q_sub_ssq'] = config.get('email', 'q_sub_ssq')
    pre.config['q_sub_cq'] = config.get('email', 'q_sub_cq')
    pre.config['q_sub_scq'] = config.get('email', 'q_sub_scq')
    pre.config['q_sub_baa'] = config.get('email', 'q_sub_baa')
    pre.config['q_ghi_hcc_sub'] = config.get('email', 'q_ghi_hcc_sub')
    pre.config['q_ghi_from'] = config.get('email', 'q_ghi_from')
    pre.config['username'] = config.get('remote', 'username')
    pre.config['access_key'] = config.get('remote', 'access_key')
    pre.config['tunnel_id'] = config.get('remote', 'tunnel_id')
    pre.config['selenium_port'] = config.get('remote', 'selenium_port')
