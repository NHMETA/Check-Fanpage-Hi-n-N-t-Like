from flask import Flask, request, jsonify, send_from_directory
import requests
import re

app = Flask(__name__, static_folder='.')

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept-Language": "vi-VN,vi;q=0.9",
}

def check_page_has_likes(uid):
    url = f"https://www.facebook.com/profile.php?id={uid}"
    try:
        res = requests.get(url, headers=HEADERS, timeout=10, allow_redirects=True)
        has_likes = "sk=friends_likes" in res.text
        return {"uid": uid, "has_likes": has_likes}
    except Exception as e:
        return {"uid": uid, "error": str(e)}

def get_uid_from_username(username):
    url = f"https://www.facebook.com/{username}"
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        m = re.search(r'"userID":"(\d+)"', res.text)
        if m: return m.group(1)
        m = re.search(r'profile_id=(\d+)', res.text)
        if m: return m.group(1)
        return None
    except:
        return None

@app.route("/")
def index():
    return send_from_directory('.', 'index.html')

@app.route("/check")
def check():
    uid = request.args.get("uid", "").strip()
    if not uid:
        return jsonify({"error": "Thiếu uid"}), 400
    return jsonify(check_page_has_likes(uid))

@app.route("/check-bulk", methods=["POST"])
def check_bulk():
    uids = request.json.get("uids", [])
    results = [check_page_has_likes(uid) for uid in uids]
    return jsonify(results)

@app.route("/get-uid")
def get_uid():
    username = request.args.get("username", "").strip()
    if not username:
        return jsonify({"error": "Thiếu username"}), 400
    uid = get_uid_from_username(username)
    if uid:
        return jsonify({"username": username, "uid": uid})
    return jsonify({"username": username, "uid": None, "error": "Không tìm thấy UID"})

if __name__ == "__main__":
    app.run()
