# coding:utf-8

import logging
import os

path = os.path.abspath('../../Log')
file = 'system.log'
new_path = os.path.join(path, file)

print(new_path)