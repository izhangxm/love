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
from helper import __initDjangoEnvironment
from LoveAPP.models import Friend
import codecs



def main():
    cc = 0
    results = Friend.objects.all()

    for ele in results[:]:
        userName = ele.userName
        try:
            # dbContactRemark_hex_str = "".join([hex(x) for x in ele.dbContactRemark[2:]]).replace('0x','')
            # contactRemark  = codecs.decode(dbContactRemark_hex_str, "hex").decode('utf-8')
            contactRemark  = ele.dbContactRemark[2:].decode('utf-8')
            print(userName,contactRemark)
        except Exception as e:
            pass
            cc += 1
    print(cc)
if __name__ == '__main__':
    main()


