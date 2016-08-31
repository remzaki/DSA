import logging
import logging.handlers


class Logger(object):
    """description of class"""

    def setup_logger(self, logger_name, log_file, level=logging.INFO):
        l = logging.getLogger(logger_name)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%m/%d/%Y %I:%M:%S %p')
        file_handler = logging.FileHandler('.\logs\\' + log_file, 'w')
        # file_handler = logging.handlers.RotatingFileHandler(
        #     'D:\\Automation\\Automation\\logs\\' + log_file, mode='w', maxBytes=5*1024*1024, backupCount=1)
        file_handler.setFormatter(formatter)
        # streamHandler = logging.StreamHandler()
        # streamHandler.setFormatter(formatter)

        l.setLevel(level)
        l.addHandler(file_handler)
        # l.addHandler(streamHandler)
