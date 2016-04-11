try:
   from ctkapi import Connector, Request, Query, Where, QueueView
except ImportError:
    raise Exception("Please install ctkapi from rackspace github")

def clean_data(data):

 try:
    if len(data) == 1:
      return str(data[0])
    return str(data)
 except TypeError:
    return "Unef"

def query_device(id_num,attribute):

  query = [
        {
            "class": "Computer.Computer",
            "load_arg": {
                "class": "Computer.ComputerWhere",
                "values": [
                    ["number", "=", id_num],
                    "&",
                    ["status_group", "in", ["active", "online"]]
                ],
                "limit": 1000,
            },
            "attributes": [ attribute ]
        }
    ]

  connector = Connector()
  connector.auth()
  data = connector.query(query)

  return clean_data(data[0]['result'][0][attribute])

