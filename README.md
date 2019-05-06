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
            msg: "{{ lookup('onepassword_local', 'p6iyvjqv4xdxw52hsacpkq4rgi', field='name') }}"
        - debug:
            msg: "{{ lookup('onepassword_local', 'c3264cef-1e5e-4c96-a192-26729539f3f5', field='your_custom_field') }}"
        - debug:
            msg: "{{ lookup('onepassword_local', '1234567890', field='password') }}"

Custom uuid feature
-------------------

uuid in 1Password changes when you move an item from one vault to another. To prevent this issue, a custom uuid mapping feature has been implemented.

You need to add on each item a field named `UUID` (in capitals).

Then run `op-local mapping update` to generate the mapping table relationship.

You can display UUID mapping by running `op-local mapping list`.

As we migrated from Lastpass to 1Password, we have also implemented a UUID mapping feature
related to a field named `LASTPASS_ID`. If the uuid given is 100% numeric, the search query will be performed over this field.


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

