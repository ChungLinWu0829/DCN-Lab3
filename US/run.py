from flask import Flask, request, Response
from socket import *
import requests

app = Flask(__name__)

@app.route('/fibonacci', methods=["GET"])
def fibonacci():
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')
    sequence_number = request.args.get('number')
    if not hostname or not fs_port or not sequence_number or not as_ip or not as_port:
        return Response("BAD REQUEST", status=400, )
    with socket(AF_INET, SOCK_DGRAM) as clientSocket:
        msg = "TYPE=A\nNAME={0}".format(hostname)
        clientSocket.sendto(msg.encode(), (as_ip, int(as_port)))
        message, _ = clientSocket.recvfrom(2048)
        clientSocket.close()

    if message.decode() == "No record":
        return Response("No record", status=200, )
    ip = message.decode().split('\n')[2].split('=')[1]
    fibonacci_number = requests.get("http://{0}:{1}/fibonacci?number={2}".format(ip, fs_port, sequence_number))
    return Response(fibonacci_number, status=200, )



app.run(host='0.0.0.0',
        port=8080,
        debug=True)
