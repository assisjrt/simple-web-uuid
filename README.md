# simple-web-uuid

---

## GET all items

```bash
curl http://localhost:8080/items
```

## GET item

```bash
curl http://localhost:8080/items/<UUID>
```

## POST

```bash
curl http://localhost:8080/items --header 'Content-Type: application/json' --data '{"name": "test01"}'
```

## PUT

```bash
curl --request PUT http://localhost:8080/items/<UUID>' --header 'Content-Type: application/json' --data '{"name": "<NAME>"}'
```

## DELETE

```bash
curl --request DELETE http://localhost:8080/items/<UUID>'
```

## Generate items

```python
import json
import urllib.request

url = "http://localhost:8080/items"
headers = {"Content-Type": "application/json"}

for i in range(1, 101):
    name = f"test{i:02d}"
    data = json.dumps({"name": name}).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")  # noqa: S310

    with urllib.request.urlopen(req) as resp:  # noqa: S310
        print(f"{name} -> {resp.status} - {resp.read().decode()}")  # noqa: T201
```

or

```bash
pip install httpie

for i in $(seq -f "%02g" 1 100); do http -F POST localhost:8080/items name=test$i; done
```
