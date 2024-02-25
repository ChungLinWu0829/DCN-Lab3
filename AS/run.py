from socket import *
import collections


serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(("", 53533))
hashTable = collections.defaultdict(str)
hashTable[("A","abcde.com")] = "localhost" # Test data

while True:

    message, address = serverSocket.recvfrom(2048)
    modifiedMessage = message.decode()
    name_type_val = modifiedMessage.split("\n")

    if len(name_type_val) >= 3: 
        #There are 3 parameters, name, type, and value for register
        type, name, value = name_type_val[0].split("=")[1], name_type_val[1].split("=")[1], name_type_val[2].split("=")[1]
        hashTable[(type, name)] = value
        serverSocket.sendto("Succeed".encode(), address)
    else:
        #There are only 2 parameters, name and type for query
        type, name = name_type_val[0].split("=")[1], name_type_val[1].split("=")[1]
        value = hashTable[(type, name)]
        #If there is a corresponding DNS record
        if value:
            msg = "TYPE={0}\nNAME={1}\nVALUE={2}\nTTL={3}".format(type, name, value, 10)
            serverSocket.sendto(msg.encode(), address)
        else:
            serverSocket.sendto("No record".encode(), address)


serverSocket.close()