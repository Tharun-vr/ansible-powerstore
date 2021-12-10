# Copyright: (c) 2021, DellEMC

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Unit Tests for Security Config module on PowerStore"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type
ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'
                    }

import pytest
from mock.mock import MagicMock
from ansible_collections.dellemc.powerstore.tests.unit.plugins.module_utils.mock_security_config_api import MockSecurityConfigApi
from ansible_collections.dellemc.powerstore.tests.unit.plugins.module_utils.mock_sdk_response \
    import MockSDKResponse
from ansible_collections.dellemc.powerstore.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException
from ansible_collections.dellemc.powerstore.plugins.module_utils.storage.dell \
    import dellemc_ansible_powerstore_utils as utils

utils.get_logger = MagicMock()
utils.get_powerstore_connection = MagicMock()
utils.PowerStoreException = MagicMock()
from ansible.module_utils import basic
basic.AnsibleModule = MagicMock()
from ansible_collections.dellemc.powerstore.plugins.modules.security_config import PowerStoreSecurityConfig


class TestPowerstoreSecurityConfig():

    get_module_args = MockSecurityConfigApi.SECURITY_CONFIG_COMMON_ARGS

    @pytest.fixture
    def security_config_module_mock(self, mocker):
        mocker.patch(MockSecurityConfigApi.MODULE_UTILS_PATH + '.PowerStoreException', new=MockApiException)
        security_config_module_mock = PowerStoreSecurityConfig()
        return security_config_module_mock

    def test_get_security_config_response(self, security_config_module_mock):
        MockSecurityConfigApi.get_security_config_response('api')
        self.get_module_args.update({
            'security_config_id': "1",
            'state': "present"
        })
        security_config_module_mock.module.params = self.get_module_args
        security_config_module_mock.perform_module_operation()
        security_config_module_mock.configuration.get_security_config_details.assert_called()

    def test_modify_security_config_response(self, security_config_module_mock):
        MockSecurityConfigApi.modify_security_config_response('module')
        self.get_module_args.update({
            'security_config_id': "1",
            'protocol_mode': "TLSv1_1",
            'state': "present"
        })
        security_config_module_mock.module.params = self.get_module_args
        security_config_module_mock.perform_module_operation()
        security_config_module_mock.configuration.modify_security_config.assert_called()

    def test_modify_security_config_invalid_protocol_mode_response(self, security_config_module_mock):
        MockSecurityConfigApi.modify_security_config_response('module')
        self.get_module_args.update({
            'security_config_id': "1",
            'protocol_mode': "TLSv1_3",
            'state': "present"
        })
        security_config_module_mock.module.params = self.get_module_args
        security_config_module_mock.perform_module_operation()
        security_config_module_mock.configuration.modify_security_config.assert_called()
