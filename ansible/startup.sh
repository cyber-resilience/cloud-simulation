#!/bin/bash

if [ -f ~/.bash_profile ]; then . ~/.bash_profile; fi

if [ "type -t setaws" = "function" ]; then setaws default; fi
export ANSIBLE_HOST_KEY_CHECKING=False

ansible-playbook --private-key=~/MM.pem -u ec2-user -f 20 -i localhost, aws.yaml
ansible-playbook --private-key=~/MM.pem -u ec2-user -f 20 -i playbooks/inventory/ec2.py setup.yaml
