import pytest
from os import path, environ
from lookup_plugins.onepassword_local import LookupModule
from ansible.errors import AnsibleError
from pytest_mock import mocker
if environ.get('USE_LOCAL'):
    import sys
    sys.path.insert(0, path.dirname(path.abspath(__file__)) + "/../../onepassword-local-search")
from onepassword_local_search.services.ConfigFileService import ConfigFileService
import json


def common_data(item):
    return dict(
        nl='\n',
        item_uuid='e25haqmocd5ifiymorfzwxnzry',
        login_uuid='zzfmhu2j7ajq55mmpm3ihs3oqy',
        login_custom_uuid='c3264cef-1e5e-4c96-a192-26729539f3f5',
        subdomain='onepassword_local_search',
        session_key='azuDId6PvlUtwsLQZD-4jzGpMxUxRNQOxEgcdbZhppI'
    ).get(item)


@pytest.fixture
def op_session(monkeypatch, mocker):
    monkeypatch.setenv('ONEPASSWORD_LOCAL_DATABASE_PATH', path.join(path.dirname(__file__), '..', 'molecule', 'default', 'tests', 'B5.sqlite'))
    monkeypatch.setenv('OP_SESSION_' + common_data('subdomain'), common_data('session_key'))
    monkeypatch.setenv('OP_SESSION_PRIVATE_KEY_FILE', path.join(path.dirname(__file__), '..', 'molecule', 'default', 'tests', '.Y_efcm4Gd_W4NnRTMeOuSEHPA5w'))
    mocker.patch.object( ConfigFileService, '_get_local_config')
    with open(path.join(path.dirname(__file__), '..', 'molecule', 'default', 'tests',  'config'), 'r') as f:
        config = f.read()
        f.close()
    ConfigFileService._get_local_config.return_value = json.loads(config)


@pytest.mark.usefixtures("op_session")
def test_get_login_title(capsys):
    result = LookupModule().run([common_data('login_uuid')], field='title')
    assert result == ['Connexion']


@pytest.mark.usefixtures("op_session")
def test_get_login_password(capsys):
    result = LookupModule().run([common_data('login_uuid')], field='password')
    assert result == ['password']


@pytest.mark.usefixtures("op_session")
def test_get_login_username(capsys):
    result = LookupModule().run([common_data('login_uuid')], field='username')
    assert result == ['username']


@pytest.mark.usefixtures("op_session")
def test_get_login_username(capsys):
    result = LookupModule().run([common_data('login_custom_uuid')], field='username', use_custom_uuid=True)
    assert result == ['username']


@pytest.mark.usefixtures("op_session")
def test_get_missing_uuid(capsys):
    with pytest.raises(AnsibleError) as e:
        LookupModule().run(['missing-uuid'], field='password')
    assert e.type == AnsibleError
    assert e.value.message == 'Unable to find item with uuid: missing-uuid'
