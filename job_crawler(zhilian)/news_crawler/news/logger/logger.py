#coding:utf-8
import time
import logging
from colorlog import ColoredFormatter

class logger:

    @property
    def setup_log(self):
        """Return a log with a default ColoredFormatter."""
        if not hasattr(self, '_log'):
            formatter = ColoredFormatter(
                "%(log_color)s%(levelname)-8s%(reset)s %(log_color)s%(message)s",
                datefmt=None,
                reset=True,
                log_colors={
                    'DEBUG':    'cyan',
                    'INFO':     'green',
                    'WARNING':  'yellow',
                    'ERROR':    'red',
                    'CRITICAL': 'red',
                }
            )
            
            # 创建一个输出logger 
            log = logging.getLogger('example')
            handler = logging.StreamHandler()
            handler.setFormatter(formatter)
            log.addHandler(handler)
            log.setLevel(logging.DEBUG)

            # 创建一个写入日志文件logger 
            log_write = logging.getLogger('example')
            handler_write = logging.FileHandler('logs/' + self.filename)  
            log_write.addHandler(handler_write)
            self._log =  log
        # 返回输出logger
        return self._log

    def __init__(self, filename = ''): 
        if filename:
            filename =  filename + '-'
        self.filename = filename + time.strftime("%Y-%m-%d", time.localtime()) + '.log'  

    def write_log(self, content, method = "error"):
        """Create and use a logger."""
        log = self.setup_log
        try:
            methods = {'debug':log.debug,'info':log.info,'warning':log.warning,'error':log.error,'critical':log.critical}
            methods.get(method)(content) 
        except Exception, e:
            self.log.error(content)
            

