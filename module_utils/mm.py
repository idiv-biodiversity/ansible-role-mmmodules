#!/usr/bin/python
# -*- coding: utf-8 -*-


def mmcmd(module, values):
    (rc, out, err) = module.run_command(values['cmd'])

    values['rc'] = rc

    values['stdout'] = out
    values['stderr'] = err

    values['stdout_lines'] = []
    values['stderr_lines'] = []

    values['stdout_lines'] = values['stdout'].splitlines()
    values['stderr_lines'] = values['stderr'].splitlines()
