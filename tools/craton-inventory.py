#!/usr/bin/env python

"""
Craton Inventory Helper: A sample client script to use with Craton api
to drive Ansible playbooks.

Description:
    Generate Inventory that Ansible can understand by querying Craton Inventory
    API. Craton will provide a fully formatted inventory json back that can
    simply be used to drive ansible playbooks.
Configuration:
    CRATON_INVENTORY_URL : should be the url pointing to your installation of
                           Craton Inventory service.
    X-Auth-Project: Craton API X-Auth-Project
    X-Auth-User: Craton API X-Auth-User
    X-Auth-Token: Craton API X-Auth-Token
    REGION: Environment variable to indicate which Region we are generating 
            the inventory for.

Usage:
    REGION=1 ansible-playbook -i cratoninventory.py playbook.yaml --list-hosts   
"""

import argparse
import json
import os
import requests
import sys


CRATON_INVENTORY_URL = "http://<host>:<port>/v1/ansible_inventory?region=%s"


def parse_args():
    parser = argparse.ArgumentParser(description='Craton Inventory for Ansible')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--list', action='store_true',
                       help='List active servers')
    group.add_argument('--host', help='List details about the specific host')

    return parser.parse_args()


def main(args):

    try:
        env_name = os.environ['REGION']
    except KeyError, e:
        sys.stderr.write('Unable to load %s\n' % e.message)
        sys.exit(1)

    headers = {
        "Content-Type": "application/json",
        "X-Auth-Token": "<Auth Token>",
        "X-Auth-User": "<Auth User>",
        "X-Auth-Project": "<Auth Project>"
    }

    try:
        url = CRATON_INVENTORY_URL % env_name
        resp = requests.get(url, headers=headers, verify=False)
        if resp.status_code != 200:
            print ("Got non 200 response from Craton Inventory API")
            sys.exit(1)
    except Exception:
        print ("Error generating inventory from Craton Inventory API")
        sys.exit(1)

    return resp.json()

if __name__ == '__main__':
    args = parse_args()
    output = main(args)
    print(json.dumps(output))
    sys.exit(0)
