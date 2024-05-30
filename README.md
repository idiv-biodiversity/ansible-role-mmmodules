Ansible Role: mmmodules
=======================

Ansible modules for [IBM Spectrum Scale][] (formerly GPFS) file systems.


Table of Contents
-----------------

<!-- toc -->

- [Requirements](#requirements)
- [Module Usage](#module-usage)
- [Dependencies](#dependencies)
- [Example Playbook](#example-playbook)
  * [Top-Level Playbook](#top-level-playbook)
  * [Role Dependency](#role-dependency)
- [License](#license)
- [Author Information](#author-information)

<!-- tocstop -->

Requirements
------------

- Ansible 2.4

Module Usage
------------

There's a bit of a chicken and egg situation going on, because some commands
can only be run if everything is set up. So, assuming that one `filer` is
already up and running, we can use one as delegate:

```yml
- name: find our delegate
  set_fact:
    mmdelegate: '{{ groups.filer | random }}'
```

This can then be used with the modules if required:

```yml
- name: add node
  mmnode:
    name: node007
  delegate_to: '{{ mmdelegate }}'

- name: add to nodeclass
  mmnodeclass:
    node: node007
    nodeclass: compute
  delegate_to: '{{ mmdelegate }}'

- name: set license
  mmlicense:
    node: node007
    license: client
  delegate_to: '{{ mmdelegate }}'
```

Configuration can be done for node classes:

```yml
- name: small pagepool for compute
  mmconfig:
    node: compute
    key: pagepool
    value: 4G
  run_once: yes

- name: fat pagepool for filer
  mmconfig:
    node: filer
    key: pagepool
    value: 256G
  run_once: yes
```

Dependencies
------------

```yml
---

# requirements.yml

roles:

  - name: idiv_biodiversity.mmmodules
    src: https://github.com/idiv-biodiversity/ansible-role-mmmodules
    version: vX.Y.Z

...
```

Example Playbook
----------------

### Top-Level Playbook

Write a top-level playbook:

```yml
---

- name: file server
  hosts: filer

  roles:
    - role: idiv_biodiversity.mmmodules

...
```

### Role Dependency

Define the role dependency in `meta/main.yml`:

```yml
---

dependencies:

  - role: idiv_biodiversity.mmmodules

...
```

License
-------

MIT

Author Information
------------------

This role was created in 2022 by [Christian Krause][author] aka [wookietreiber
at GitHub][wookietreiber], HPC cluster systems administrator at the [German
Centre for Integrative Biodiversity Research (iDiv)][idiv].


[IBM Spectrum Scale]: https://www.ibm.com/products/spectrum-scale
[author]: https://www.idiv.de/en/groups_and_people/employees/details/61.html
[idiv]: https://www.idiv.de/
[wookietreiber]: https://github.com/wookietreiber
