import requests


# Workaround fo newer urlib and anyoing certificates
import ssl
try:
   ssl._create_default_https_context = ssl._create_unverified_context
except:
    pass

def query_url(dc, device):
    kirAPI = requests.session()

    if "IAD3" in dc: #IAD 3
        kir_url_base = "https://iad3.kir.kickstart.rackspace.com"

    if "ORD1" in dc: #ORD1
        kir_url_base = "https://ord1.kir.kickstart.rackspace.com"

    if "LON3" in dc: #LON3
        kir_url_base = "https://lon3.kir.kickstart.rackspace.com"

    if "HK1" in dc: #HK1
        kir_url_base = "https://hkg1.kir.kickstart.rackspace.com"

    if "SYD2" in dc: #SYD2
        kir_url_base = "https://syd2.kir.kickstart.rackspace.com"

    if "DFW" in dc: # DFW
        kir_url_base = "https://dfw1.kir.kickstart.rackspace.com"

    tmp = kirAPI.get('%s/dc/api/inventory/get_ids_by_server_number/%s' % (kir_url_base, device),verify=False).json()

    if len(tmp['objects']) == 0:
        return None, None

    if len(tmp['objects']) == 1:

        kir_id = tmp['objects'][0]['id']
        kir_url = tmp['objects'][0]['url']
        return str(kir_url)

    else:
        kir_timestamp = 0
        for id in tmp['objects']:
            tmp2 = kirAPI.get(id['url']).json()

            if tmp2['time_created'] > kir_timestamp:
                kir_timestamp = tmp2['time_created']
                kir_id = id['id']
                kir_url = id['url']

        return str(kir_url)