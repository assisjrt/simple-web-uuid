import platform
import secrets
from datetime import datetime, timedelta, timezone
from typing import Literal
from uuid import uuid4

from flask import Flask, request

app = Flask(__name__)

data_store: dict[str, dict[str, str]] = {}


def get_random_color() -> str:
    return secrets.choice(["red", "blue", "yellow", "green", "orange", "purple"])


@app.route("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.route("/")
def hello_world() -> dict[str, str]:
    uuid = uuid4()
    hostname = platform.node()
    return {"hostname": str(hostname), "uuid": str(uuid)}


@app.route("/items", methods=["GET"])
def get_items() -> dict[str, dict[str, str]]:
    return data_store


@app.route("/items/<item_id>", methods=["GET"])
def get_item(item_id: str) -> tuple[dict[str, str], Literal[404]] | dict[str, str]:
    if item_id not in data_store:
        return {"error": "item not found"}, 404
    return {"item": str(data_store[item_id])}


@app.route("/items", methods=["POST"])
def create_item() -> tuple[dict[str, str], Literal[201]]:
    data = request.get_json() or {}
    item_id = str(uuid4())

    item = {
        "name": data.get("name", ""),
        "color": get_random_color(),
        "created_at": datetime.now(timezone(timedelta(hours=-3))).isoformat(),
    }

    data_store[item_id] = item
    return {"message": "item created success", "item": str(item)}, 201


@app.route("/items/<item_id>", methods=["PUT"])
def update_item(item_id: str) -> tuple[dict[str, str], Literal[404]] | dict[str, str]:
    if item_id not in data_store:
        return {"error": "item not found"}, 404

    data = request.get_json() or {}
    item = data_store[item_id]

    item["name"] = data.get("name", item["name"])
    item["updated_at"] = platform.node()

    return {"message": "item update success", "item": str(item)}


@app.route("/items/<item_id>", methods=["DELETE"])
def delete_item(item_id: str) -> tuple[dict[str, str], Literal[404]] | dict[str, str]:
    if item_id not in data_store:
        return {"error": "item not found"}, 404

    deleted_item = data_store.pop(item_id)
    return {"message": "item deleted success", "deleted_item": str(deleted_item)}
