import logging
import logging.handlers


class Logger(object):
    """description of class"""

    def setup_logger(self, logger_name, log_file, rotate=False, level=logging.INFO):
        l = logging.getLogger(logger_name)

        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%m/%d/%Y %I:%M:%S %p')

        if rotate:
            file_handler = logging.handlers.RotatingFileHandler(
                '.\logs\\' + log_file, mode='w', maxBytes=5*1024*1024, backupCount=2)
        else:
            file_handler = logging.FileHandler('.\logs\\' + log_file, 'w')
        file_handler.setFormatter(formatter)

        formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        l.setLevel(level)
        l.addHandler(file_handler)
        l.addHandler(stream_handler)
