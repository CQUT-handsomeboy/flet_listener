import zmq
import sys
import json

from icecream import ic
from time import sleep

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")
while True:
    card = {
        "title":"标题",
        "text":"正文"
    }
    card = json.dumps(card)
    socket.send(card.encode("utf-8"))
    socket.recv()
    sleep(3)
