import argparse
from ipaddress import ip_address
import json
import requests
import sys

REGIONS = [{'ORD': {
            "glance_default_store": "swift",
            "neutron_l2_population": True,
            "tempest_public_subnet_cidr": "192.168.1.0/22",
            "nova_console_type": "novnc"}},
           {'DFW': {
            "glance_default_store": "swift",
            "neutron_l2_population": True,
            "tempest_public_subnet_cidr": "192.168.4.0/22",
            "nova_console_type": "novnc"}}]

CELLS = [{'C0001': {"cell_capabilities": "flavor_classes=performance2",
                    "console_host": "10.10.1.100"}},
         {'C0002': {"cell_capabilities": "flavor_classes=performance1",
                    "console_host": "10.20.1.100"}}]


def make_hosts(region, cell):
    # no of hosts need to match ip_address available
    no_of_hosts = 2
    cab1 = region + "." + cell + "." + "C-1"
    cab2 = region + "." + cell + "." + "C-2"

    hosts = []
    for host in range(no_of_hosts):
        hostname = "host%s.%s.example1.com" % (host, cab1)
        hosts.append(hostname)

    for host in range(no_of_hosts):
        hostname = "host%s.%s.example2.com" % (host, cab2)
        hosts.append(hostname)

    return hosts


class Inventory(object):
    def __init__(self, url, project_id, auth_user, auth_key):
        self.url = url
        self.auth_user = auth_user
        self.auth_key = auth_key
        self.project_id = project_id or 1
        self.region = None
        self.cell = None
        self.ip_addresses = self.generate_ip_addresses(16)

        self.headers = {"Content-Type": "application/json",
                        "X-Auth-Project": str(self.project_id),
                        "X-Auth-User": self.auth_user,
                        "X-Auth-Token": self.auth_key}

    def generate_ip_addresses(self, num_ips):
        start_ip_address = ip_address(u'192.168.1.5')
        ips = [str(start_ip_address + i) for i in range(num_ips)]
        return ips

    def create_region(self, region, data=None):
        region_url = self.url + "/regions"
        payload = {"name": region, "project": self.project_id}

        print("Creating region entry for %s with data %s" % (payload, data))
        resp = requests.post(region_url, headers=self.headers,
                             data=json.dumps(payload), verify=False)
        if resp.status_code != 200:
            raise Exception(resp.text)

        self.region = resp.json()
        if data:
            region_data_url = self.url + "/regions/%s/data" % self.region["id"]
            resp = requests.put(region_data_url, headers=self.headers,
                                data=json.dumps(data), verify=False)
            if resp.status_code != 200:
                print(resp.text)

    def create_cell(self, cell, data=None):
        region_url = self.url + "/cells"
        payload = {"region": self.region.get("id"), "name": cell,
                   "project": self.project_id}

        print("Creating cell entry %s with data %s" % (payload, data))
        resp = requests.post(region_url, headers=self.headers,
                             data=json.dumps(payload), verify=False)
        if resp.status_code != 200:
            raise Exception(resp.text)

        self.cell = resp.json()
        if data:
            region_data_url = self.url + "/cells/%s/data" % resp.json()["id"]
            resp = requests.put(region_data_url, headers=self.headers,
                                data=json.dumps(data), verify=False)
            if resp.status_code != 200:
                print(resp.text)

    def create_device(self, host, device_type, data=None):
        region_url = self.url + "/hosts"
        payload = {"region": self.region.get("id"),
                   "cell": self.cell.get("id"),
                   "project": self.project_id,
                   "name": host,
                   "ip_address": self.ip_addresses.pop(0),
                   "device_type": device_type}

        print("Creating host entry %s with data %s" % (payload, data))
        resp = requests.post(region_url, headers=self.headers,
                             data=json.dumps(payload), verify=False)

        if resp.status_code != 200:
            raise Exception(resp.text)

        if data:
            region_data_url = self.url + "/hosts/%s/data" % resp.json()["id"]
            resp = requests.put(region_data_url, headers=self.headers,
                                data=json.dumps(data), verify=False)
            if resp.status_code != 200:
                print(resp.text)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', help='Endpoint for Craton Service')
    parser.add_argument('--user', help='User id')
    parser.add_argument('--project', type=int, help='Project id')
    parser.add_argument('--key', help='Auth Key for the sevice')
    args = parser.parse_args()

    if not args.url:
        print("--url is requred. This is your craton api endpoint")
        sys.exit(1)
    if not args.user:
        print("--user is requred. This is your craton user id.")
        sys.exit(1)
    if not args.project:
        print("--project is requred. This is your craton project id.")
        sys.exit(1)
    if not args.key:
        print("--key is requred. This is your craton auth key.")
        sys.exit(1)

    Inv = Inventory(args.url, args.project, args.user, args.key)

    for region in REGIONS:
        # Frist create region
        region_name = region.keys()[0]
        Inv.create_region(region_name, data=region[region_name])

        for cell in CELLS:
            cell_name = cell.keys()[0]
            Inv.create_cell(cell_name, data=cell[cell_name])
            # Get host in the cell
            hosts = make_hosts(region_name, cell_name)
            for host in hosts:
                Inv.create_device(host, 'server')
