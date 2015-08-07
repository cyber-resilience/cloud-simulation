#!/bin/bash
#ansible -i playbooks/inventory/ec2.py tag_AnsibleCreated_True -u ec2-user --private-key=~/MM.pem -m shell -a 'df -h'
ansible -i playbooks/inventory/ec2.py tag_AnsibleCreated_True -u ec2-user --private-key=~/MM.pem "$@"
