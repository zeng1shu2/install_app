# coding:utf-8

import logging
import os

if os.path.exists('./Log'):
    pass
else:
    os.mkdir('./Log')
path = os.path.abspath('./Log')
check = 'Check_Sys.log'
check_path = os.path.join(path, check)


def check_logs():
    c_log = logging
    c_log.basicConfig(level=logging.DEBUG,
                      format="%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s",
                      filename=check_path,
                      filemode='a+'
                      )
    return c_log
