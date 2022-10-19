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
            license=dict(required=True),
        ),
        supports_check_mode=True,
    )

    # -------------------------------------------------------------------------
    # module variables
    # -------------------------------------------------------------------------

    node = module.params['node']
    lic = module.params['license']

    # -------------------------------------------------------------------------
    # list current licenses
    # -------------------------------------------------------------------------

    mmls = {}
    mmls['cmd'] = '/usr/lpp/mmfs/bin/mmlslicense'
    mmls['cmd'] = "%s -Y" % mmls['cmd']

    mmcmd(module, mmls)

    if mmls['rc'] != 0:
        module.fail_json(
            msg="failure during mmlslicense",
            mmlslicense=mmls,
        )

    current = {}

    mmls_xsv = csv.DictReader(mmls['stdout_lines'], delimiter=':')

    for row in mmls_xsv:
        if row['nodeName'] == node:
            current['required'] = row['requiredLicense']
            current['designated'] = row['designatedLicense']
            break

    if not current:
        module.fail_json(
            msg="node %s not known by mmlslicense" % node,
            mmlslicense=mmls,
        )

    if lic != current['required']:
        module.fail_json(
            msg="%s target %s license does not match required %s license" % (
                node,
                lic,
                current['required']
            ),
            mmlslicense=mmls,
        )

    changed = lic != current['designated']

    # -------------------------------------------------------------------------
    # change if required and exit
    # -------------------------------------------------------------------------

    if changed and not module.check_mode:
        mmch = {}
        mmch['cmd'] = '/usr/lpp/mmfs/bin/mmchlicense'
        mmch['cmd'] = "%s %s --accept -N %s" % (mmch['cmd'], lic, node)

        mmcmd(module, mmch)

        if mmch['rc'] != 0:
            module.fail_json(
                msg="failure during mmchlicense",
                mmchlicense=mmch,
            )
        else:
            module.exit_json(
                changed=changed,
                mmlslicense=mmls,
                mmchlicense=mmch,
                diff=dict(
                    before="%s\n" % current['designated'],
                    after="%s\n" % lic,
                )
            )
    else:
        module.exit_json(
            changed=changed,
            mmlslicense=mmls,
            diff=dict(
                before="%s\n" % current['designated'],
                after="%s\n" % lic,
            )
        )


if __name__ == '__main__':
    main()
