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
            node=dict(required=True),
            nodeclass=dict(required=True),
        ),
        supports_check_mode=True,
    )

    # -------------------------------------------------------------------------
    # module variables
    # -------------------------------------------------------------------------

    node = module.params['node']
    nodeclass = module.params['nodeclass']

    # -------------------------------------------------------------------------
    # list node class
    # -------------------------------------------------------------------------

    mmls = {}
    mmls['cmd'] = '/usr/lpp/mmfs/bin/mmlsnodeclass'
    mmls['cmd'] = "%s %s -Y" % (mmls['cmd'], nodeclass)

    mmcmd(module, mmls)

    if mmls['rc'] != 0:
        module.fail_json(
            msg="failure during mmlsnodeclass",
            mmlsnodeclass=mmls,
        )

    mmls_xsv = csv.DictReader(mmls['stdout_lines'], delimiter=':')
    changed = True

    for row in mmls_xsv:
        if row['nodeClass'] == nodeclass:
            if node in row['memberNodes'].split(','):
                changed = False

            break

    # -------------------------------------------------------------------------
    # change if required and exit
    # -------------------------------------------------------------------------

    if changed and not module.check_mode:
        mmch = {}
        mmch['cmd'] = '/usr/lpp/mmfs/bin/mmchnodeclass'
        mmch['cmd'] = "%s %s add -N %s" % (mmch['cmd'], nodeclass, node)

        mmcmd(module, mmch)

        if mmch['rc'] != 0:
            module.fail_json(
                msg="failure during mmchnodeclass",
                mmlsnodeclass=mmls,
                mmchnodeclass=mmch,
            )
        else:
            module.exit_json(
                changed=changed,
                mmlsnodeclass=mmls,
                mmchnodeclass=mmch,
            )

    else:
        module.exit_json(
            changed=changed,
            mmlsnodeclass=mmls,
        )


if __name__ == '__main__':
    main()
