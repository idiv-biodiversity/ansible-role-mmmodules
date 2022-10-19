#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.mm import mmcmd


def main():

    # -------------------------------------------------------------------------
    # ansible module definition
    # -------------------------------------------------------------------------

    module = AnsibleModule(
        argument_spec=dict(
            node=dict(default=''),
            name=dict(required=True, aliases=['attribute', 'key']),
            value=dict(required=True),
        ),
        supports_check_mode=True,
    )

    # -------------------------------------------------------------------------
    # module variables
    # -------------------------------------------------------------------------

    node = module.params['node']
    name = module.params['name']
    value = module.params['value']

    if node == 'common':
        node = ''

    # -------------------------------------------------------------------------
    # list current config
    # -------------------------------------------------------------------------

    mmls = {}
    mmls['cmd'] = '/usr/lpp/mmfs/bin/mmlsconfig'
    mmls['cmd'] = "%s -Y %s" % (mmls['cmd'], name)

    mmcmd(module, mmls)

    if mmls['rc'] != 0:
        module.fail_json(
            msg="failure during mmlsconfig",
            mmlsconfig=mmls,
        )

    for line in mmls['stdout_lines']:
        if "(undefined)" in line:
            module.fail_json(
                msg="undefined attribute %s" % name,
                mmlsconfig=mmls,
            )

    mmls_xsv = csv.DictReader(mmls['stdout_lines'], delimiter=':')

    current = {}

    for row in mmls_xsv:
        nodelist = row['nodeList'].split(',')

        if len(nodelist) == 1 and not nodelist[0]:
            common = row['value']

        if not node and not nodelist or node in nodelist:
            current = row['value']
            break

    if current:
        changed = value != current
    elif common:
        changed = value != common
        current = common
    else:
        changed = True
        current = None

    # -------------------------------------------------------------------------
    # change if required and exit
    # -------------------------------------------------------------------------

    if changed and not module.check_mode:
        mmch = {}
        mmch['cmd'] = '/usr/lpp/mmfs/bin/mmchconfig'
        mmch['cmd'] = "%s %s=%s" % (mmch['cmd'], name, value)

        if node:
            mmch['cmd'] = "%s -N %s" % (mmch['cmd'], node)

        mmcmd(module, mmch)

        if mmch['rc'] != 0:
            module.fail_json(
                msg="failure during mmchconfig",
                mmchconfig=mmch,
            )

        else:
            module.exit_json(
                changed=changed,
                mmlsconfig=mmls,
                mmchconfig=mmch,
                diff=dict(
                    before="%s\n" % current,
                    after="%s\n" % value,
                )
            )

    else:
        module.exit_json(
            changed=changed,
            mmlsconfig=mmls,
            diff=dict(
                before="%s\n" % current,
                after="%s\n" % value,
            )
        )


if __name__ == '__main__':
    main()
