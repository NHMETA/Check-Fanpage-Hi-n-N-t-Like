from flask import Flask, request, jsonify, send_from_directory
import requests
import re

app = Flask(__name__, static_folder='.')

ACCESS_TOKEN = "EAAVi5UFSu9cBRQMkbZBqo8ZBdAeOojyP7ZAS0qUtZCNnLE1rCqh5rdMKC5ZAWcSSEIOOYdyhZBWWSnI9MJNpDRkgwf6XNcm9GBzjxozeetYMIsYZAQqbSrJ2UGG6BPJ1n0PPMi0nHaGUdICd81wZBG5bHYMtRHnz3vrj9g3MiGMmHjJtFWHFm0Lv2oK5V3xQPxtANZCmnmDNhALkML43805uiHsnqY6H9tzJg4F8WW5hn9BApfILZAnzra5zwzygz20QetWZAHbmx42evoKCcZBX2eBLl8TA2mnDnuNsQ53CZA3xP0P0uMHhqLjZCk6XlXBUZBZBS510F8VL13LJApTNh4iT0BssxQHNGwZDZD"

def check_page_has_likes(uid):
    url = f"https://graph.facebook.com/{uid}"
    try:
        res = requests.get(url, params={
            "fields": "fan_count,name",
            "access_token": ACCESS_TOKEN
        }, timeout=10)
        data = res.json()
        if "error" in data:
            return {"uid": uid, "has_likes": False, "error": data["error"]["message"]}
        fan_count = data.get("fan_count", 0)
        return {"uid": uid, "has_likes": fan_count > 0, "fan_count": fan_count, "name": data.get("name", "")}
    except Exception as e:
        return {"uid": uid, "error": str(e)}

@app.route("/")
def index():
    return send_from_directory('.', 'index.html')

@app.route("/check")
def check():
    uid = request.args.get("uid", "")
    if not uid:
        return jsonify({"error": "Thiếu uid"}), 400
    return jsonify(check_page_has_likes(uid))

@app.route("/check-bulk", methods=["POST"])
def check_bulk():
    uids = request.json.get("uids", [])
    results = [check_page_has_likes(uid) for uid in uids]
    return jsonify(results)

@app.route("/get-uid", methods=["POST"])
def get_uid():
    link = request.json.get("link", "")
    uid = extract_uid_from_link(link)
    if uid:
        return jsonify({"uid": uid})
    return jsonify({"error": "Không tìm thấy UID"}), 400

def extract_uid_from_link(link):
    match = re.search(r'id=(\d+)', link)
    if match:
        return match.group(1)
    return None

if __name__ == "__main__":
    app.run()
