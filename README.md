1Password Local Lookup Plugin
=========

This is a simple lookup plugin that search for secrets in a local 1Password database (B5.sqlite format). 
It uses the [onepassword-local-search](https://github.com/mickaelperrin/onepassword-local-search) python module that 
greatly improve performance over querying directly the 1Password servers.

Requirements
------------

You require:
- python 3.7
- onepassword-local-search module

```
pip3 install onepassword-local-search
```

Example Playbook
----------------

    - hosts: servers
      roles:
        - role: mickaelperrin.ansible-onepassword-local-lookup-plugin
      tasks
        - debug:
            msg: "{{ lookup('onepassword-local', 'p6iyvjqv4xdxw52hsacpkq4rgi', field='name') }}"
        - debug:
            msg: "{{ lookup('onepassword-local', 'p6iyvjqv4xdxw52hsacpkq4rgi', field='name', section='Section name') }}"

Tests
-----

Tests are managed by `pytest` for the python part and `molecule` for the ansible part with `docker` as driver.

```
mkvirtualenv3 ansible-onepassword-local-lookup-plugin
pip install -r requirements/dev.txt
```

### Pytest

```
pytest
``` 

### Molecule

Ensure that `docker` service is up and running

```
molecule test
``` 

License
-------

GPLv3

