from flask import Flask, request, jsonify, send_from_directory
import requests
import re

app = Flask(__name__, static_folder='.')

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept-Language": "vi-VN,vi;q=0.9",
}

def check_page_has_likes(uid):
    url = f"https://www.facebook.com/profile.php?id={uid}&sk=friends_likes"
    try:
        res = requests.get(url, headers=HEADERS, timeout=10, allow_redirects=True)
        html = res.text

        # Nếu bị redirect về login
        if "login" in res.url:
            return {"uid": uid, "has_likes": False}

        # Debug: trả về 500 ký tự đầu để xem
        # return {"uid": uid, "debug": html[:500]}

        # Page có lượt thích: URL giữ nguyên sk=friends_likes và có nội dung likes
        # Page không có: Facebook redirect hoặc không render tab likes

        # Tìm pattern phân biệt 2 loại page
        # Page 2 (có likes): có "friends_likes" trong phần selected/active tab
        # Page 1 (không có): không có tab này

        has_likes = bool(
            re.search(r'"sk":"friends_likes"', html) or
            re.search(r'selected.*?friends_likes|friends_likes.*?selected', html) or
            re.search(r'"activeTab":"friends_likes"', html) or
            re.search(r'lượt thích.*?\d', html, re.IGNORECASE)
        )

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
    uid = request.args.get("uid", "")
    if not uid:
        return jsonify({"error": "Thiếu uid"}), 400
    return jsonify(check_page_has_likes(uid))

# Route debug: xem raw HTML Facebook trả về
@app.route("/debug")
def debug():
    uid = request.args.get("uid", "")
    if not uid:
        return "Thêm ?uid=xxx", 400
    url = f"https://www.facebook.com/profile.php?id={uid}&sk=friends_likes"
    try:
        res = requests.get(url, headers=HEADERS, timeout=10, allow_redirects=True)
        # Trả về 2000 ký tự để tìm pattern
        return f"URL: {res.url}\n\nHTML:\n{res.text[:2000]}", 200, {"Content-Type": "text/plain"}
    except Exception as e:
        return str(e), 500

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
