# coding:utf-8

import logging
import os

if os.path.exists('./Log'):
    pass
else:
    os.mkdir('./Log')
path = os.path.abspath('./Log')
file = 'system.log'
new_path = os.path.join(path, file)


def logs():
    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s",
                        filename=new_path,
                        filemode='a'
                        )
    return logging

