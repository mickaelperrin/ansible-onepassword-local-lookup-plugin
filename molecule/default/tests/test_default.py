import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_hosts_file(host):
    f = host.file('/testfile.txt')
    assert f.exists
    assert f.contains('zzfmhu2j7ajq55mmpm3ihs3oqy::password::password')


def test_custom_uuid(host):
    f = host.file('/testfile.txt')
    assert f.exists
    assert f.contains('c3264cef-1e5e-4c96-a192-26729539f3f5::password::password')


def test_lastpass_uuid(host):
    f = host.file('/testfile.txt')
    assert f.exists
    assert f.contains('1234567890::password::password')