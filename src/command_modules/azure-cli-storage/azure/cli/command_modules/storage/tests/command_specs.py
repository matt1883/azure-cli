# AZURE CLI STORAGE TEST DEFINITIONS

import collections
import os
import sys
from time import sleep

from six import StringIO

from azure.cli.utils.command_test_script import CommandTestScript
from azure.common import AzureHttpError

RESOURCE_GROUP_NAME = 'travistestresourcegroup'
STORAGE_ACCOUNT_NAME = 'travistestresourcegr3014'
TEST_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), '..'))

ENV_VAR = {
    'AZURE_STORAGE_CONNECTION_STRING':('DefaultEndpointsProtocol=https;' +
                                        'AccountName={};' +
                                        'AccountKey=blahblah').format(STORAGE_ACCOUNT_NAME)
}

def _get_connection_string(runner):
    out = runner.run('storage account connection-string -g {} -n {}'
        .format(RESOURCE_GROUP_NAME, STORAGE_ACCOUNT_NAME))
    connection_string = out.replace('Connection String : ', '')
    runner.set_env('AZURE_STORAGE_CONNECTION_STRING', connection_string)

class StorageAccountScenarioTest(CommandTestScript):

    def test_body(self):
        account = STORAGE_ACCOUNT_NAME
        rg = RESOURCE_GROUP_NAME
        s = self
        s.test('storage account check-name --name teststorageomega', {'nameAvailable': True})
        s.test('storage account check-name --name {}'.format(account),
               {'nameAvailable': False, 'reason': 'AlreadyExists'})
        s.rec('storage account list -g {}'.format(rg))
        s.test('storage account show --resourcegroup {} --account-name {}'.format(rg, account),
               {'name': account, 'accountType': 'Standard_LRS', 'location': 'westus', 'resourceGroup': rg})
        s.rec('storage account usage')
        s.rec('storage account connection-string -g {} --account-name {} --use-http'.format(rg, account))
        s.rec('storage account keys list -g {} --account-name {}'.format(rg, account))
        s.rec('storage account keys renew -g {} --account-name {}'.format(rg, account))
        s.rec('storage account keys renew -g {} --account-name {} --key key2'.format(rg, account))
        s.test('storage account set -g {} -n {} --tags foo=bar;cat'.format(rg, account),
               {'tags': {'cat':'', 'foo':'bar'}})
        # TODO: This should work like other tag commands--no value to clear
        s.test('storage account set -g {} -n {} --tags none='.format(rg, account),
               {'tags': {'none': ''}})
        s.test('storage account set -g {} -n {} --type Standard_GRS'.format(rg, account),
               {'accountType': 'Standard_GRS'})
        s.run('storage account set -g {} -n {} --type Standard_LRS'.format(rg, account))

    def __init__(self):
        super(StorageAccountScenarioTest, self).__init__(None, self.test_body, None)

class StorageBlobScenarioTest(CommandTestScript):

    def set_up(self):
        self.container = 'testcontainer01'
        self.blob = 'testblob1'
        self.rg = RESOURCE_GROUP_NAME
        self.proposed_lease_id = 'abcdabcd-abcd-abcd-abcd-abcdabcdabcd'
        self.new_lease_id = 'dcbadcba-dcba-dcba-dcba-dcbadcbadcba'
        self.dest_file = os.path.join(TEST_DIR, 'download-blob.rst')
        self.date = '2016-04-08T12:00Z'
        _get_connection_string(self)
        # TODO: 'exists' does not seem to work with a SAS token.
        #sas_token = self.run('storage account generate-sas --services b --resource-types sco --permission rwdl --expiry 2017-01-01T00:00Z')
        #sas_token = self.run('storage container generate-sas --permission rwdl --expiry 2017-01-01T00:00Z -c {}'.format(container))
        #print('TOKEN: {}'.format(sas_token))
        #self.set_env('AZURE_SAS_TOKEN', sas_token)
        #self.set_env('AZURE_STORAGE_ACCOUNT', STORAGE_ACCOUNT_NAME)
        #self.pop_env('AZURE_STORAGE_CONNECTION_STRING')
        self.run('storage container delete --container-name {}'.format(self.container))
        if self.run('storage container exists --container-name {}'.format(self.container)) == 'True':
            raise RuntimeError('Failed to delete pre-existing container {}. Unable to continue test.'.format(self.container))

    def _storage_blob_scenario(self):
        s = self
        container = s.container
        blob = s.blob
        dest_file = s.dest_file
        s.run('storage blob upload-block-blob -b {} -c {} --upload-from {}'.format(blob, container, os.path.join(TEST_DIR, 'testfile.rst')))
        s.run('storage blob download -b {} -c {} --download-to {}'.format(blob, container, dest_file))
        if os.path.isfile(dest_file):
            os.remove(dest_file)
        else:
            raise RuntimeError('Download failed. Test failed!')
        s.test('storage blob exists -b {} -c {}'.format(blob, container), True)
        s.rec('storage blob list --container-name {}'.format(container))
        s.rec('storage blob properties get --container-name {} --blob-name {}'.format(container, blob))
        s.run('storage blob delete --container-name {} --blob-name {}'.format(container, blob))
        s.test('storage blob exists -b {} -c {}'.format(blob, container), False)

    def test_body(self):
        s = self
        container = s.container
        rg = s.rg
        proposed_lease_id = s.proposed_lease_id
        new_lease_id = s.new_lease_id
        date = s.date
        s.test('storage container create --container-name {} --fail-on-exist'.format(container), True)
        s.test('storage container exists --container-name {}'.format(container), True)
        s.test('storage container show --container-name {}'.format(container), {'name': container})
        s.rec('storage container list')
        s.run('storage container metadata set -c {} --metadata foo=bar;moo=bak;'.format(container))
        s.test('storage container metadata get -c {}'.format(container), {'foo': 'bar', 'moo': 'bak'})
        s.run('storage container metadata set -c {}'.format(container)) # reset metadata
        s.test('storage container metadata get -c {}'.format(container), None)
        s._storage_blob_scenario()
        
        # test lease operations
        s.run('storage container lease acquire --lease-duration 60 -c {} --if-modified-since {} --proposed-lease-id {}'.format(container, date, proposed_lease_id))
        s.test('storage container show --container-name {}'.format(container),
                {'properties': {'lease': {'duration': 'fixed', 'state': 'leased', 'status': 'locked'}}})
        s.run('storage container lease change --container-name {} --lease-id {} --proposed-lease-id {}'.format(container, proposed_lease_id, new_lease_id))
        s.run('storage container lease renew --container-name {} --lease-id {}'.format(container, new_lease_id))
        s.test('storage container show --container-name {}'.format(container),
                {'properties': {'lease': {'duration': 'fixed', 'state': 'leased', 'status': 'locked'}}})
        s.run('storage container lease break --container-name {} --lease-break-period 30'.format(container))
        s.test('storage container show --container-name {}'.format(container),
                {'properties': {'lease': {'duration': None, 'state': 'breaking', 'status': 'locked'}}})
        s.run('storage container lease release --container-name {} --lease-id {}'.format(container, new_lease_id))
        s.test('storage container show --container-name {}'.format(container),
                {'properties': {'lease': {'duration': None, 'state': 'available', 'status': 'unlocked'}}})
        
        # verify delete operation
        s.test('storage container delete --container-name {} --fail-not-exist'.format(container), True)
        s.test('storage container exists --container-name {}'.format(container), False)

    def tear_down(self):
        self.run('storage container delete --container-name {}'.format(self.container))

    def __init__(self):
        super(StorageBlobScenarioTest, self).__init__(self.set_up, self.test_body, self.tear_down)

class StorageFileScenarioTest(CommandTestScript):

    def set_up(self):
        self.share1 = 'testshare01'
        self.share2 = 'testshare02'
        _get_connection_string(self)
        self.run('storage share delete --share-name {}'.format(self.share1))
        self.run('storage share delete --share-name {}'.format(self.share2))

    def _storage_directory_scenario(self, share):
        s = self
        dir = 'testdir01'
        s.test('storage directory create --share-name {} --directory-name {} --fail-on-exist'.format(share, dir), True)
        s.test('storage directory exists --share-name {} --directory-name {}'.format(share, dir), True)
        s.run('storage directory metadata set --share-name {} --directory-name {} --metadata a=b;c=d'.format(share, dir))
        s.test('storage directory metadata get --share-name {} --directory-name {}'.format(share, dir),
               {'a': 'b', 'c': 'd'})
        s.run('storage directory metadata set --share-name {} --directory-name {}'.format(share, dir))
        s.test('storage directory metadata get --share-name {} --directory-name {}'.format(share, dir), None)
        s._storage_file_in_subdir_scenario(share, dir)
        s.test('storage directory delete --share-name {} --directory-name {} --fail-not-exist'.format(share, dir), True)
        s.test('storage directory exists --share-name {} --directory-name {}'.format(share, dir), False)

        # verify a directory can be created with metadata and then delete
        dir = 'testdir02'
        s.test('storage directory create --share-name {} --directory-name {} --fail-on-exist --metadata foo=bar;cat=hat'.format(share, dir), True)
        s.test('storage directory metadata get --share-name {} --directory-name {}'.format(share, dir),
               {'cat': 'hat', 'foo': 'bar'})
        s.test('storage directory delete --share-name {} --directory-name {} --fail-not-exist'.format(share, dir), True)

    def _storage_file_scenario(self, share):
        source_file = os.path.join(TEST_DIR, 'testfile.rst')
        dest_file = os.path.join(TEST_DIR, 'download_test.rst')
        filename = 'testfile.rst'
        s = self
        s.run('storage file upload --share-name {} --local-file-name {} --file-name {}'.format(share, source_file, filename))
        s.test('storage file exists --share-name {} --file-name {}'.format(share, filename), True)
        if os.path.isfile(dest_file):
            os.remove(dest_file)
        s.run('storage file download --share-name {} --file-name {} --local-file-name {}'.format(share, filename, dest_file))
        if os.path.isfile(dest_file):
            os.remove(dest_file)
        else:
            s.print_('\nDownload failed. Test failed!')
        s.rec('storage share contents --share-name {}'.format(share))
        s.run('storage file delete --share-name {} --file-name {}'.format(share, filename))
        s.test('storage file exists --share-name {} --file-name {}'.format(share, filename), False)

    def _storage_file_in_subdir_scenario(self, share, dir):
        source_file = os.path.join(TEST_DIR, 'testfile.rst')
        dest_file = os.path.join(TEST_DIR, 'download_test.rst')
        filename = 'testfile.rst'
        s = self
        s.run('storage file upload --share-name {} --directory-name {} --local-file-name {} --file-name {}'.format(share, dir, source_file, filename))
        s.test('storage file exists --share-name {} --directory-name {} --file-name {}'.format(share, dir, filename), True)
        if os.path.isfile(dest_file):    
            os.remove(dest_file)
        s.run('storage file download --share-name {} --directory-name {} --file-name {} --local-file-name {}'.format(share, dir, filename, dest_file))
        if os.path.isfile(dest_file):
            os.remove(dest_file)
        else:
            io.print_('\nDownload failed. Test failed!')
        s.rec('storage share contents --share-name {} --directory-name {}'.format(share, dir))
        s.run('storage file delete --share-name {} --directory-name {} --file-name {}'.format(share, dir, filename))
        s.test('storage file exists --share-name {} --file-name {}'.format(share, filename), False)

    def test_body(self):
        s = self
        share1 = s.share1
        share2 = s.share2
        s.test('storage share create --share-name {} --fail-on-exist'.format(share1), True)
        s.test('storage share create --share-name {} --fail-on-exist --metadata foo=bar;cat=hat'.format(share2), True)
        s.test('storage share exists --share-name {}'.format(share1), True)
        s.test('storage share metadata get --share-name {}'.format(share2), {'cat': 'hat', 'foo': 'bar'})
        # TODO: Would need to enable behavior if a dictionary contains a list...
        s.rec('storage share list')

        # verify metadata can be set, queried, and cleared
        s.run('storage share metadata set --share-name {} --metadata a=b;c=d'.format(share1))
        s.test('storage share metadata get --share-name {}'.format(share1), {'a': 'b', 'c': 'd'})
        s.run('storage share metadata set --share-name {}'.format(share1))
        s.test('storage share metadata get --share-name {}'.format(share1), None)

        self._storage_file_scenario(share1)
        self._storage_directory_scenario(share1)

    def tear_down(self):
        self.run('storage share delete --share-name {} --fail-not-exist'.format(self.share1))
        self.run('storage share delete --share-name {} --fail-not-exist'.format(self.share2))

    def __init__(self):
        super(StorageFileScenarioTest, self).__init__(self.set_up, self.test_body, self.tear_down)

TEST_DEF = [
    # STORAGE ACCOUNT TESTS
    {
        'test_name': 'storage_account',
        'script': StorageAccountScenarioTest()
    },
    # TODO: Enable when item #117262541 is complete
    #{
    #    'test_name': 'storage_account_create',
    #    'command': 'storage account create --type Standard_LRS -l westus -g travistestresourcegroup --account-name teststorageaccount04'
    #},
    {
        'test_name': 'storage_account_delete',
        'command': 'storage account delete -g travistestresourcegroup --account-name teststorageaccount04'
    },
    # STORAGE CONTAINER TESTS
    {
        'test_name': 'storage_blob',
        'script': StorageBlobScenarioTest()
    },
    # STORAGE SHARE TESTS
    {
        'test_name': 'storage_file',
        'script': StorageFileScenarioTest()
    },
]