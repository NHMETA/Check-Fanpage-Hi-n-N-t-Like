from flask import Flask, request, jsonify, send_from_directory
import requests

app = Flask(__name__, static_folder='.')

@app.route("/")
def index():
    return send_from_directory('.', 'index.html')

@app.route("/check")
def check():
    uid = request.args.get("uid", "").strip()
    token = request.args.get("token", "").strip()
    if not uid:
        return jsonify({"error": "Thiếu uid"}), 400
    if not token:
        return jsonify({"error": "Thiếu token"}), 400
    try:
        url = f"https://graph.facebook.com/v19.0/{uid}?fields=fan_count,followers_count,name&access_token={token}"
        res = requests.get(url, timeout=10)
        data = res.json()
        if "error" in data:
            return jsonify({"uid": uid, "error": data["error"]["message"]})
        has_likes = "fan_count" in data
        return jsonify({
            "uid": uid,
            "name": data.get("name", ""),
            "has_likes": has_likes,
            "fan_count": data.get("fan_count"),
            "followers_count": data.get("followers_count"),
        })
    except Exception as e:
        return jsonify({"uid": uid, "error": str(e)})

@app.route("/check-bulk", methods=["POST"])
def check_bulk():
    uids = request.json.get("uids", [])
    token = request.json.get("token", "")
    results = []
    for uid in uids:
        try:
            url = f"https://graph.facebook.com/v19.0/{uid}?fields=fan_count,followers_count,name&access_token={token}"
            res = requests.get(url, timeout=10)
            data = res.json()
            if "error" in data:
                results.append({"uid": uid, "error": data["error"]["message"]})
            else:
                results.append({
                    "uid": uid,
                    "name": data.get("name", ""),
                    "has_likes": "fan_count" in data,
                    "fan_count": data.get("fan_count"),
                    "followers_count": data.get("followers_count"),
                })
        except Exception as e:
            results.append({"uid": uid, "error": str(e)})
    return jsonify(results)

@app.route("/get-uid")
def get_uid():
    username = request.args.get("username", "").strip()
    token = request.args.get("token", "").strip()
    if not username or not token:
        return jsonify({"error": "Thiếu username hoặc token"}), 400
    try:
        url = f"https://graph.facebook.com/v19.0/{username}?fields=id,name&access_token={token}"
        res = requests.get(url, timeout=10)
        data = res.json()
        if "error" in data:
            return jsonify({"username": username, "uid": None, "error": data["error"]["message"]})
        return jsonify({"username": username, "uid": data.get("id"), "name": data.get("name")})
    except Exception as e:
        return jsonify({"username": username, "uid": None, "error": str(e)})

if __name__ == "__main__":
    app.run()
