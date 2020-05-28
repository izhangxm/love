#! /usr/bin/python
# -*- coding: utf-8 -*-
# @author izhangxm
# Copyright 2017 izhangxm@gmail.com. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
import os
from datetime import datetime
from sys import stdout

# 获得标准时间
def getFTime():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class Logger(object):
    def __init__(self, fp_locker, file_path, screen_locker):
        self.screen_locker = screen_locker
        self.fp_locker = fp_locker
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))
        self.fp = open(file_path, 'a+',encoding='utf-8')

    def log(self, tag, user, info, screen=True):
        '''
        日志记录和屏幕输出
        :param user:
        :param tag:
        :param info:
        :return:
        '''
        output_str = "%s, %s, %s, %s" % (getFTime(), tag, user, info)
        try:
            self.fp_locker.acquire()
            self.fp.write(output_str + '\n')
        finally:
            self.fp.flush()
            self.fp_locker.release()

        if screen:
            try:
                self.screen_locker.acquire()
                output_str = "\033[0;31m%s %s %s %s\033[0m" % (getFTime(), tag, user, info)
                if tag == 'INFO':
                    output_str = '\033[0;32m%s %s %s %s\033[0m'% (getFTime(), tag, user, info)
                print(output_str)
            finally:
                stdout.flush()
                self.screen_locker.release()