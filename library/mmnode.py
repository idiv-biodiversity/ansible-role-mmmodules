#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.mm import mmcmd


def main():

    # -------------------------------------------------------------------------
    # ansible module definition
    # -------------------------------------------------------------------------

    module = AnsibleModule(
        argument_spec=dict(
            node=dict(required=True, aliases=['name']),
        ),
        supports_check_mode=True,
    )

    # -------------------------------------------------------------------------
    # module variables
    # -------------------------------------------------------------------------

    node = module.params['node']

    # -------------------------------------------------------------------------
    # list node
    # -------------------------------------------------------------------------

    mmls = {}
    mmls['cmd'] = '/usr/lpp/mmfs/bin/mmlsnode'
    mmls['cmd'] = "%s -N %s" % (mmls['cmd'], node)

    mmcmd(module, mmls)

    changed = mmls['rc'] != 0

    # -------------------------------------------------------------------------
    # change if required and exit
    # -------------------------------------------------------------------------

    if changed and not module.check_mode:
        mmch = {}
        mmch['cmd'] = '/usr/lpp/mmfs/bin/mmaddnode'
        mmch['cmd'] = "%s -N %s" % (mmch['cmd'], node)

        mmcmd(module, mmch)

        if mmch['rc'] != 0:
            module.fail_json(
                msg="failure during mmaddnode",
                mmlsnode=mmls,
                mmaddnode=mmch,
            )
        else:
            module.exit_json(
                changed=changed,
                mmlsnode=mmls,
                mmaddnode=mmch,
            )
    else:
        module.exit_json(
            changed=changed,
            mmlsnode=mmls,
        )


if __name__ == '__main__':
    main()
