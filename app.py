from flask import Flask, request, jsonify, send_from_directory
import requests
import re

app = Flask(__name__, static_folder='.')

def check_page_has_likes(uid):
    url = f"https://www.facebook.com/profile.php?id={uid}"
    try:
        res = requests.get(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "vi-VN,vi;q=0.9"
        }, timeout=10)
        text = res.text
        has_likes = "lượt thích" in text and "người theo dõi" in text
        return {"uid": uid, "has_likes": has_likes}
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
