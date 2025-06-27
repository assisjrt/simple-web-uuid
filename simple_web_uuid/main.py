import platform
from uuid import uuid4

from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world() -> dict[str, str]:
    uuid = uuid4()
    hostname = platform.node()
    return {"hostname": str(hostname), "uuid": str(uuid)}


@app.route("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
