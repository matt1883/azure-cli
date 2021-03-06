#---------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#---------------------------------------------------------------------------------------------
#pylint: skip-file
# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator 0.16.0.0
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class RegistryProperties(Model):
    """RegistryProperties

    :param storage_account:
    :type storage_account: :class:`StorageAccountBaseProperties
     <containerregistry.models.StorageAccountBaseProperties>`
    :param login_server:
    :type login_server: str
    :param creation_date:
    :type creation_date: datetime
    :param admin_user_enabled:
    :type admin_user_enabled: bool
    """ 

    _attribute_map = {
        'storage_account': {'key': 'storageAccount', 'type': 'StorageAccountBaseProperties'},
        'login_server': {'key': 'loginServer', 'type': 'str'},
        'creation_date': {'key': 'creationDate', 'type': 'iso-8601'},
        'admin_user_enabled': {'key': 'adminUserEnabled', 'type': 'bool'},
    }

    def __init__(self, storage_account=None, login_server=None, creation_date=None, admin_user_enabled=None):
        self.storage_account = storage_account
        self.login_server = login_server
        self.creation_date = creation_date
        self.admin_user_enabled = admin_user_enabled
