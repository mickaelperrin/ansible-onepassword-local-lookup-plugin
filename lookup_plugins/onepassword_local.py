# python 3 headers, required if submitting to Ansible
from __future__ import (absolute_import, division, print_function)
from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.lookup import LookupBase
__metaclass__ = type
from os import path, environ
if environ.get('USE_LOCAL'):
    import sys
    sys.path.insert(0, path.dirname(path.abspath(__file__)) + "/../../onepassword-local-search")
from onepassword_local_search.OnePassword import OnePassword

DOCUMENTATION = """
    lookup: onepassword-local
    author: Mickaël Perrin <contact@mickaelperrin.fr>
    version_added: 1.0
    short_description: fast lookup of secrets stored in a local 1Password database (B5.sqlite)
    description: This plugin uses the onepassword-local-search python module that implements a faster way to retrieve
        secrets by using a local 1Password database in B5.sqlite format.
    requirements:
        - pip module onepassword-local-search
    options:
        _uuid:
          description: 'uuid of the item to retrieve.
            This may be:
              - a 1Password uuid
              - the value of a field named UUID in UUID v4 format
              - the value of a field named LASTPASS_ID with a lastpass uuid (digits only)
          Be sure to have run `op-local mapping update` to use custom uuid feature.'
          required: True
        field:
          description: 'the name of the field to be retrieven (name, username, password, notes, uri or any custom field).
            If not filled, the entire object is retrieven.'
          default: None
          required: False
"""

EXAMPLES = """
- name: get 'item'
  debug:
    msg: "{{ lookup('onepassword-local', 'e25haqmocd5ifiymorfzwxnzry' }}"
- name: get 'password'
  debug:
    msg: "{{ lookup('onepassword-local', 'e25haqmocd5ifiymorfzwxnzry', field='password' }}"
- name: get 'custom_field'
  debug:
    msg: "{{ lookup('onepassword-local', 'e25haqmocd5ifiymorfzwxnzry', field='custom_field' }}"
- name: get 'custom_field' with custom UUID field (the field is named UUID)
  debug:
    msg: "{{ lookup('onepassword-local', 'c3264cef-1e5e-4c96-a192-26729539f3f5', field='custom_field' }}"
- name: get 'custom_field' with custom lastpass field (the field is named LASTPASS_ID)
  debug:
    msg: "{{ lookup('onepassword-local', '1234567890', field='custom_field' }}"
"""

try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display
    display = Display()


class LookupModule(LookupBase):

    def run(self, uuids, **kwargs):
        ret = []
        field = kwargs.get('field')
        section = kwargs.get('section')
        for uuid in uuids:
            if field and section:
                display.debug("1Password lookup field: %s in section %s of uuid: %s" % (field, section, uuid))
            elif field:
                display.debug("1Password lookup first field: %s of uuid: %s" % (field, uuid))
            else:
                display.debug("1Password lookup full item with uuid: %s" % uuid)
            try:
                result = OnePassword().get(uuid, field=field, output=False)
                if result is not None:
                    ret.append(result.rstrip())
                else:
                    if field and section:
                        raise AnsibleError("could not find field: %s in section: %s" % (field, section))
                    elif field:
                        raise AnsibleError("could not find field: %s" % field)
                    else:
                        raise AnsibleError("Trouble when grabbing fields from item with uuid: %s" % uuid)
            except Exception as e:
                raise AnsibleError(e.args[0])
            except SystemExit as e:
                raise AnsibleError(e.code)
            except AnsibleParserError:
                raise AnsibleError("could not locate item with uuid: %s" % uuid)
        return ret
