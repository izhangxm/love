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
from django.db import models
class Friend(models.Model):
    certificationFlag = models.IntegerField(db_column=u'certificationFlag', primary_key=False)
    dbContactBrand = models.BinaryField(db_column=u'dbContactBrand', primary_key=False)
    dbContactChatRoom = models.BinaryField(db_column=u'dbContactChatRoom', primary_key=False)
    dbContactHeadImage = models.BinaryField(db_column=u'dbContactHeadImage', primary_key=False)
    dbContactLocal = models.BinaryField(db_column=u'dbContactLocal', primary_key=False)
    dbContactOpenIM = models.BinaryField(db_column=u'dbContactOpenIM', primary_key=False)
    dbContactOther = models.BinaryField(db_column=u'dbContactOther', primary_key=False)
    dbContactProfile = models.BinaryField(db_column=u'dbContactProfile', primary_key=False)
    dbContactRemark = models.BinaryField(db_column=u'dbContactRemark', primary_key=False)
    dbContactSocial = models.BinaryField(db_column=u'dbContactSocial', primary_key=False)

    encodeUserName = models.TextField(db_column=u'encodeUserName', primary_key=False)
    extFlag = models.IntegerField(db_column=u'extFlag', primary_key=False)
    imgStatus = models.IntegerField(db_column=u'imgStatus', primary_key=False)
    openIMAppid = models.TextField(db_column=u'openIMAppid', primary_key=False)
    type = models.IntegerField(db_column=u'type', primary_key=False)
    userName = models.TextField(db_column=u'userName', primary_key=True)

    class Meta:
        db_table = 'Friend'