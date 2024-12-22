from opcua import Server
import time
from random import randint
import datetime
import random

server = Server()

url = "opc.tcp://localhost:4840"
server.set_endpoint(url)

# Create a new address space
address_space = server.register_namespace("MyNamespace")

# Create a folder node to organize the nodes
folder = server.get_objects_node().add_object(address_space, "MyFolder")

# Add nodes to the address space
individual_weight_node = folder.add_variable(address_space, "Individual Weight", 0)
request_to_collect_node = folder.add_variable(address_space, "Request to Collect", 0)
#individual_weight_node.add_property(address_space, "Unit", "kg")
print(individual_weight_node)
print(request_to_collect_node)
# Set the nodes as writable
individual_weight_node.set_writable()
request_to_collect_node.set_writable()

# Assign values to the nodes
individual_weight_node.set_value(1500)
request_to_collect_node.set_value(2000)

# Start the OPC UA server
server.start()
#print("OPC UA server started at", url)
#print(((folder.get_children())[0].get_properties())[0].get_data_value())

def generate_random_weight():
    random_number = random.randint(1500, 3000)
    return random_number
    #return 1000

# Run the server indefinitely
try:
    while True:
        time.sleep(2)
        # if request_to_collect is false set it to true

        weight = generate_random_weight()
        individual_weight_node.set_value(weight)

        request_to_collect_node.set_value(generate_random_weight())
        print(request_to_collect_node.get_value())

except KeyboardInterrupt:
    server.stop()
    print("OPC UA server stopped")