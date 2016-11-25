import argparse
from ipaddress import ip_address
import json
import requests
import sys

REGIONS = [{'ORD135': {
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
        self.project_id = project_id
        self.region = None
        self.cell = None
        self.ip_addresses = self.generate_ip_addresses(16)

        self.headers = {"Content-Type": "application/json",
                        "X-Auth-Project": self.project_id,
                        "X-Auth-User": self.auth_user,
                        "X-Auth-Token": self.auth_key}

    def generate_ip_addresses(self, num_ips):
        start_ip_address = ip_address(u'192.168.1.5')
        ips = [str(start_ip_address + i) for i in range(num_ips)]
        return ips

    def create_region(self, region, data=None):
        region_url = self.url + "/regions"
        payload = {"name": region}

        print("Creating region entry for %s with data %s" % (payload, data))
        resp = requests.post(region_url, headers=self.headers,
                             data=json.dumps(payload), verify=False)
        if resp.status_code != 200:
            raise Exception(resp.text)

        self.region = resp.json()
        if data:
            reg_id = self.region["id"]
            region_data_url = self.url + "/regions/%s/variables" % reg_id
            resp = requests.put(region_data_url, headers=self.headers,
                                data=json.dumps(data), verify=False)
            if resp.status_code != 200:
                print(resp.text)

    def create_cell(self, cell, data=None):
        region_url = self.url + "/regions/{}/cells".format(self.region['id'])
        payload = {"name": cell}

        print("Creating cell entry %s with data %s" % (payload, data))
        resp = requests.post(region_url, headers=self.headers,
                             data=json.dumps(payload), verify=False)
        if resp.status_code != 200:
            raise Exception(resp.text)

        self.cell = resp.json()
        if data:
            c_id = resp.json()["id"]
            region_data_url = self.url + "/cells/%s/variables" % c_id
            resp = requests.put(region_data_url, headers=self.headers,
                                data=json.dumps(data), verify=False)
            if resp.status_code != 200:
                print(resp.text)

    def create_device(self, host, device_type, data=None):
        region_url = self.url + "/regions/{}/hosts".format(self.region['id'])
        payload = {
            "cell_id": self.cell.get("id"),
            "name": host,
            "ip_address": self.ip_addresses.pop(0),
            "device_type": device_type
        }

        print("Creating host entry %s with data %s" % (payload, data))
        device_obj = requests.post(region_url, headers=self.headers,
                                   data=json.dumps(payload), verify=False)

        if device_obj.status_code != 200:
            raise Exception(device_obj.text)

        if data:
            device_id = device_obj.json()["id"]
            region_data_url = region_url + "/%s/variables" % device_id
            resp = requests.put(region_data_url, headers=self.headers,
                                data=json.dumps(data), verify=False)
            if resp.status_code != 200:
                print(resp.text)

        return device_obj.json()

    def create_network(self, name, cidr, gateway, netmask, block_type):
        networks_url = "{}/regions/{}/networks".format(
            self.url, self.region['id']
        )
        payload = {"name": name,
                   "cidr": cidr,
                   "gateway": gateway,
                   "netmask": netmask,
                   "ip_block_type": block_type,
                   "cell_id": self.cell.get("id")}

        print("Creating new network: %s" % payload)
        resp = requests.post(networks_url, headers=self.headers,
                             data=json.dumps(payload), verify=False)
        if resp.status_code != 200:
            raise Exception(resp.text)

        return resp.json()

    def create_netdevice(self, name, device_type):
        netdevices_url = "{}/regions/{}/netdevices".format(
            self.url, self.region['id']
        )
        payload = {"hostname": name,
                   "model_name": "model-x",
                   "os_version": "version-1",
                   "device_type": device_type,
                   "ip_address": "10.10.1.1",
                   "active": True,
                   "cell_id": self.cell.get("id")}

        resp = requests.post(netdevices_url, headers=self.headers,
                             data=json.dumps(payload), verify=False)
        if resp.status_code != 200:
            raise Exception(resp.text)

        return resp.json()

    def create_net_interface(self, device, int_num, network=None):
        netinterfaces_url = "{}/devices/{}/net_interfaces".format(
            self.url, device['id']
        )
        name = "eth%s" % int_num
        payload = {
            "name": name,
            "interface_type": "ethernet",
            "vlan_id": 1,
            "port": int_num,
            "duplex": "full",
            "speed": 1000,
            "link": "up",
        }
        if network:
            payload["network_id"] = network.get("id")

        print("Creating network interface %s on device %s for network %s"
              % (name, device.get("id"), network.get("id")))
        resp = requests.post(netinterfaces_url, headers=self.headers,
                             data=json.dumps(payload), verify=False)
        if resp.status_code != 200:
            raise Exception(resp.text)

        return resp.json()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', help='Endpoint for Craton Service')
    parser.add_argument('--user', help='User id')
    parser.add_argument('--project', help='Project id')
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
        region_name = list(region.keys())[0]
        Inv.create_region(region_name, data=region[region_name])

        for cell in CELLS:
            cell_name = list(cell.keys())[0]
            Inv.create_cell(cell_name, data=cell[cell_name])
            # Create a example private network for the cell
            network_name = "private_net_%s" % cell_name
            network = Inv.create_network(network_name,
                                         "192.168.1.0",
                                         "192.168.1.1",
                                         "255.255.255.0",
                                         "private")
            # Create a ToR switch for this cell
            _name = "switch1.%s.%s.example.com" % (cell_name, region_name)
            switch = Inv.create_netdevice(_name, "switch")
            # NOTE(sulo): Create 6 switch ports on the switch with the
            # above network, the same switch can have other networks
            # as well.
            for int_num in range(5):
                Inv.create_net_interface(switch, int_num, network=network)
            # Get host in the cell
            hosts = make_hosts(region_name, cell_name)
            for host in hosts:
                host_obj = Inv.create_device(host, 'server')
                # Create network interface on the host to connect to the
                # private network, the interfaces allows us to conncet this
                # host to the switch or other devices, such that we can form
                # logical or physical groupings such as a cab.
                Inv.create_net_interface(host_obj, 0, network=network)
