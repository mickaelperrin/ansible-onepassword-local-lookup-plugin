import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_hosts_file(host):
    f = host.file('/testfile.txt')
    assert f.exists
    assert f.contains('zzfmhu2j7ajq55mmpm3ihs3oqy::password::password')
