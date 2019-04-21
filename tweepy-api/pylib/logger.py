import logging as log

keys = ['debug','warn','info','error']
values = [log.DEBUG,log.WARN, log.INFO,log.ERROR]
log_level = dict(zip(keys,values))


def set_logger(log_mode='warn',pid=''):
    log_format = '%(levelname)s: %(message)s'
    log.basicConfig(filename="logger_"+pid+".log",format=log_format, level=log_level[log_mode],filemode='w')
    return log
