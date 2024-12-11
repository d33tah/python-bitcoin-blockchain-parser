import json
import base64
import sys
import datetime

import flask
import requests

from blockchain_parser.block import Block

app = flask.Flask(__name__)


class BytesEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return base64.b16encode(obj).decode()
        # if it's an object, return the object's dict
        if hasattr(obj, "__dict__"):
            return obj.__dict__
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)


def get_hash_by_block_no(n):
    url = f"https://api.blockcypher.com/v1/btc/main/blocks/{n}"
    h = requests.get(url).json()["hash"]
    return h


def get_bitcoin_by_block_hash(h):
    url2 = f"https://blockchain.info/rawblock/{h}?format=hex"
    b = base64.b16decode(requests.get(url2).text.upper().encode())
    return b


@app.route("/<int:n>")
def get_block(n):
    buf = get_bitcoin_by_block_hash(get_hash_by_block_no(n))
    sys.stderr.write(f"{buf=}\n")
    block = Block(buf)
    j = json.dumps(block.__dict__, cls=BytesEncoder, indent=4)
    sys.stderr.write(f"{block.__dict__=}\n")
    sys.stderr.write(f"{block.transactions[0].__dict__=}\n")
    return flask.Response(j, mimetype="application/octet-stream")


if __name__ == "__main__":
    app.run(host="0.0.0.0")
