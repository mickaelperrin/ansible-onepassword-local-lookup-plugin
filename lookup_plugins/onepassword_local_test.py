import pytest
from os import path
from lookup_plugins.onepassword_local import LookupModule
from ansible.errors import AnsibleError
from pytest_mock import mocker
from onepassword_local_search.services.ConfigFileService import ConfigFileService
import json


def common_data(item):
    return dict(
        nl='\n',
        item_uuid='e25haqmocd5ifiymorfzwxnzry',
        login_uuid='zzfmhu2j7ajq55mmpm3ihs3oqy',
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
    LookupModule().run([common_data('login_uuid')], field='title')
    std = capsys.readouterr()
    assert std.out == 'Connexion'


@pytest.mark.usefixtures("op_session")
def test_get_login_password(capsys):
    LookupModule().run([common_data('login_uuid')], field='password')
    std = capsys.readouterr()
    assert std.out == 'password'


@pytest.mark.usefixtures("op_session")
def test_get_login_username(capsys):
    LookupModule().run([common_data('login_uuid')], field='username')
    std = capsys.readouterr()
    assert std.out == 'username'


@pytest.mark.usefixtures("op_session")
def test_get_missing_uuid(capsys):
    with pytest.raises(AnsibleError) as e:
        LookupModule().run(['missing-uuid'], field='password')
    assert e.type == AnsibleError
    assert e.value.message == 'Unable to find item with uuid: missing-uuid'
