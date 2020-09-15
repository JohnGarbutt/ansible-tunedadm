import openstack
import json
import pprint

conn = openstack.connection.from_config()
raw_servers = list(conn.compute.servers(details=True))

servers = {server.id: server.name for server in raw_servers if "openhpc-" in server.name}
networking = {server.name: server.addresses['ilab'][0]['addr'] for server in raw_servers if "openhpc-" in server.name}

print("[openhpc]")
for name, ip in networking.items():
    print(f"{name} ansible_host={ip}")

raw_nodes = list(conn.baremetal.nodes())

server_nodes = {}
for node in raw_nodes:
    server_id = node.instance_id
    name = servers.get(server_id)
    if name:
        server_nodes[name] = node.name

b16 = []
b17 = []
for server, node in server_nodes.items():
    if "b16" in node:
        b16.append(server)
    elif "b17" in node:
        b17.append(server)
b16.sort()
b17.sort()

info_list = list(server_nodes.items())
info_list.sort()

print(json.dumps(info_list, indent=2))

print("b16")
print(b16)
print("b17")
print(b17)
