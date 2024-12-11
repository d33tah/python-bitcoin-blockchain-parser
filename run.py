import json
import base64
import sys
import datetime
import traceback

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
    resp = requests.get(url)
    try:
        h = resp.json()["hash"]
    except Exception as e:
        raise Exception(f"Error getting hash: {e}. {resp.text=}") from e
    return h


def get_bitcoin_by_block_hash(h):
    url2 = f"https://blockchain.info/rawblock/{h}?format=hex"
    resp = requests.get(url2)
    try:
        b = base64.b16decode(resp.text.upper().encode())
    except Exception as e:
        raise Exception(f"Error getting hash: {e}. {resp.text=}") from e
    return b


@app.route("/v1/byhash/<h>")
def get_by_hash(h):
    try:
        buf = get_bitcoin_by_block_hash(h)
    except Exception as e:
        tb = traceback.format_exc()
        return flask.Response(f"Error: {e}. {tb=}", status=500)
    sys.stderr.write(f"{buf=}\n")
    block = Block(buf)
    j = json.dumps(block.__dict__, cls=BytesEncoder, indent=4)
    return flask.Response(j, mimetype="application/json")

@app.route("/v1/byblockno/<int:n>")
def get_by_blockno(n):
    try:
        buf = get_bitcoin_by_block_hash(get_hash_by_block_no(n))
    except Exception as e:
        tb = traceback.format_exc()
        return flask.Response(f"Error: {e}. {tb=}", status=500)
    sys.stderr.write(f"{buf=}\n")
    block = Block(buf)
    j = json.dumps(block.__dict__, cls=BytesEncoder, indent=4)
    return flask.Response(j, mimetype="application/json")


if __name__ == "__main__":
    app.run(host="0.0.0.0")
