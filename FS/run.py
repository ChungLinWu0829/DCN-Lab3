from flask import Flask, request, Response
from socket import *


app = Flask(__name__)

@app.route('/register', methods=["PUT"])
def register():
    data = request.get_json()
    ip = data.get('ip')
    as_ip = data.get('as_ip')
    as_port = data.get('as_port')
    hostname = data.get('hostname')

    if not all([ip, as_ip, as_port, hostname]):
        return Response("Required parameters are missing", 400, )

    message_to_send = f"Type=A\nName={hostname}\nValue={ip}\nTTL=10"
    with socket(AF_INET, SOCK_RAW) as clientSocket:
        clientSocket.sendto(message_to_send.encode(), (as_ip, int(as_port)))
        message, _ = clientSocket.recvfrom(2048)
        modifiedMessage = message.decode()

    if modifiedMessage == "200":
        return Response("Successed", status=201, ) 
    else:
        return Response("Bad Request", status=500, ) 

def get_fibonacci_number(number):
    if number == 1:
        return 0
    if number == 2:
        return 1
    return get_fibonacci_number(number-1)+get_fibonacci_number(number-2)

@app.route('/fibonacci', methods=["GET"])
def fibonacci():
    sequence_number = request.args.get("number")
    if sequence_number == "":
        return Response("Bad Format", status=400, )
    else:
        if int(sequence_number) <= 0:
            return Response("Invalid Number", status=400, )
        else:
            result = get_fibonacci_number(int(sequence_number))
            return Response(str(result), status=201, ) 



app.run(host='0.0.0.0',
        port=9090,
        debug=True)
