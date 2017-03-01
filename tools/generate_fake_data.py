import argparse
from ipaddress import ip_address
import json
import requests
import sys

CLOUDS = [{"CLOUD1": {
           "openstack_release": "juno"}},
          {"CLOUD2": {
           "openstack_release": "kilo"}}]

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
        self.ip_addresses = self.generate_ip_addresses(32, u'192.168.1.5')
        self.container_ips = self.generate_ip_addresses(128, u'172.0.0.2')

        self.headers = {"Content-Type": "application/json",
                        "X-Auth-Project": self.project_id,
                        "X-Auth-User": self.auth_user,
                        "X-Auth-Token": self.auth_key}

    def generate_ip_addresses(self, num_ips, starting_ip):
        start_ip_address = ip_address(starting_ip)
        ips = [str(start_ip_address + i) for i in range(num_ips)]
        return ips

    def create_cloud(self, cloud, data=None):
        cloud_url = self.url + "/clouds"
        payload = {"name": cloud}

        print("Creating cloud entry for %s with data %s" % (payload, data))
        resp = requests.post(cloud_url, headers=self.headers,
                             data=json.dumps(payload), verify=False)
        if resp.status_code != 201:
            raise Exception(resp.text)

        self.cloud = resp.json()
        if data:
            reg_id = self.cloud["id"]
            cloud_data_url = self.url + "/clouds/%s/variables" % reg_id
            resp = requests.put(cloud_data_url, headers=self.headers,
                                data=json.dumps(data), verify=False)
            if resp.status_code != 200:
                print(resp.text)

    def create_region(self, region, data=None):
        region_url = self.url + "/regions"
        payload = {"name": region, "cloud_id": self.cloud.get("id")}

        print("Creating region entry for %s with data %s" % (payload, data))
        resp = requests.post(region_url, headers=self.headers,
                             data=json.dumps(payload), verify=False)
        if resp.status_code != 201:
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
        region_url = self.url + "/cells"
        payload = {"region_id": self.region.get("id"),
                   "cloud_id": self.cloud.get("id"), "name": cell}

        print("Creating cell entry %s with data %s" % (payload, data))
        resp = requests.post(region_url, headers=self.headers,
                             data=json.dumps(payload), verify=False)
        if resp.status_code != 201:
            raise Exception(resp.text)

        self.cell = resp.json()
        if data:
            c_id = resp.json()["id"]
            region_data_url = self.url + "/cells/%s/variables" % c_id
            resp = requests.put(region_data_url, headers=self.headers,
                                data=json.dumps(data), verify=False)
            if resp.status_code != 200:
                print(resp.text)

    def create_container(self, host_obj, data=None):
        region_url = self.url + "/hosts"

        payload = {"region_id": host_obj.get("region_id"),
                   "cloud_id": host_obj.get("cloud_id"),
                   "cell_id": host_obj.get("cell_id"),
                   "ip_address": self.container_ips.pop(0),
                   "device_type": "container"}

        payload["parent_id"] = host_obj["id"]
        name = "container_{}".format(host_obj["name"])
        payload["name"] = name

        print("Creating container entry %s with data %s" % (payload, data))
        container_obj = requests.post(region_url, headers=self.headers,
                                      data=json.dumps(payload), verify=False)

    def create_device(self, host, device_type, parent=None, data=None):
        region_url = self.url + "/hosts"
        payload = {"region_id": self.region.get("id"),
                   "cloud_id": self.cloud.get("id"),
                   "cell_id": self.cell.get("id"),
                   "name": host,
                   "ip_address": self.ip_addresses.pop(0),
                   "device_type": device_type}

        if parent is not None:
            payload["parent_id"] = parent

        print("Creating host entry %s with data %s" % (payload, data))
        device_obj = requests.post(region_url, headers=self.headers,
                                   data=json.dumps(payload), verify=False)

        if device_obj.status_code != 201:
            raise Exception(device_obj.text)

        if data:
            device_id = device_obj.json()["id"]
            region_data_url = self.url + "/hosts/%s/variables" % device_id
            resp = requests.put(region_data_url, headers=self.headers,
                                data=json.dumps(data), verify=False)
            if resp.status_code != 200:
                print(resp.text)

        return device_obj.json()

    def create_network(self, name, cidr, gateway, netmask, block_type):
        networks_url = self.url + "/networks"
        payload = {"name": name,
                   "cidr": cidr,
                   "gateway": gateway,
                   "netmask": netmask,
                   "ip_block_type": block_type,
                   "cloud_id": self.cloud.get("id"),
                   "region_id": self.region.get("id"),
                   "cell_id": self.cell.get("id")}

        print("Creating new network: %s" % payload)
        resp = requests.post(networks_url, headers=self.headers,
                             data=json.dumps(payload), verify=False)
        if resp.status_code != 201:
            raise Exception(resp.text)

        return resp.json()

    def create_netdevice(self, name, device_type):
        network_devices_url = self.url + "/network-devices"
        payload = {"name": name,
                   "model_name": "model-x",
                   "os_version": "version-1",
                   "device_type": device_type,
                   "ip_address": "10.10.1.1",
                   "active": True,
                   "cloud_id": self.cloud.get("id"),
                   "region_id": self.region.get("id"),
                   "cell_id": self.cell.get("id")}

        resp = requests.post(network_devices_url, headers=self.headers,
                             data=json.dumps(payload), verify=False)
        if resp.status_code != 201:
            raise Exception(resp.text)

        return resp.json()

    def create_net_interface(self, device, int_num, network=None):
        netinterfaces_url = self.url + "/network-interfaces"
        name = "eth%s" % int_num
        payload = {"name": name,
                   "interface_type": "ethernet",
                   "vlan_id": 1,
                   "port": int_num,
                   "duplex": "full",
                   "speed": 1000,
                   "link": "up",
                   "device_id": device.get("id"),
                   "ip_address": "10.10.0.1"}
        if network:
            payload["network_id"] = network.get("id")

        print("Creating network interface %s on device %s for network %s"
              % (name, device.get("id"), network.get("id")))
        resp = requests.post(netinterfaces_url, headers=self.headers,
                             data=json.dumps(payload), verify=False)
        if resp.status_code != 201:
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

    for cloud in CLOUDS:
        # First create cloud
        cloud_name = list(cloud.keys())[0]
        Inv.create_cloud(cloud_name, data=cloud[cloud_name])

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
                    host_obj = Inv.create_device(host, 'server', parent=switch['id'])
                    # Create container on each host
                    Inv.create_container(host_obj)
                    # Create network interface on the host to connect to the
                    # private network, the interfaces allows us to conncet this
                    # host to the switch or other devices, such that we can
                    # form logical or physical groupings such as a cab.
                    Inv.create_net_interface(host_obj, 0, network=network)
