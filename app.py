<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>FB Page Likes Checker</title>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@300;400;500&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: #0a0a0a;
    --surface: #111111;
    --border: #222222;
    --border2: #2a2a2a;
    --text: #e8e8e8;
    --muted: #666;
    --accent: #00e5a0;
    --accent-dim: rgba(0,229,160,0.08);
    --red: #ff4d4d;
    --red-dim: rgba(255,77,77,0.08);
    --yellow: #ffd166;
    --blue: #4da6ff;
    --blue-dim: rgba(77,166,255,0.08);
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background: var(--bg); color: var(--text); font-family: 'IBM Plex Sans', sans-serif; font-size: 14px; min-height: 100vh; padding: 40px 20px; }
  .wrap { max-width: 760px; margin: 0 auto; }
  header { margin-bottom: 32px; }
  .logo { font-family: 'IBM Plex Mono', monospace; font-size: 11px; font-weight: 600; letter-spacing: 0.15em; color: var(--accent); text-transform: uppercase; margin-bottom: 10px; }
  h1 { font-size: 28px; font-weight: 300; letter-spacing: -0.02em; line-height: 1.2; }
  h1 span { color: var(--accent); font-weight: 500; }
  .subtitle { color: var(--muted); font-size: 13px; margin-top: 6px; }
  .tabs { display: flex; gap: 4px; margin-bottom: 20px; border-bottom: 1px solid var(--border); }
  .tab { font-family: 'IBM Plex Mono', monospace; font-size: 11px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; padding: 10px 18px; cursor: pointer; color: var(--muted); border-bottom: 2px solid transparent; margin-bottom: -1px; transition: all 0.15s; background: none; border-top: none; border-left: none; border-right: none; }
  .tab:hover { color: var(--text); }
  .tab.active { color: var(--accent); border-bottom-color: var(--accent); }
  .tab-content { display: none; }
  .tab-content.active { display: block; }
  .card { background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 20px; margin-bottom: 16px; }
  label { display: block; font-family: 'IBM Plex Mono', monospace; font-size: 11px; letter-spacing: 0.1em; color: var(--muted); text-transform: uppercase; margin-bottom: 8px; }
  textarea { width: 100%; background: var(--bg); border: 1px solid var(--border2); border-radius: 6px; color: var(--text); font-family: 'IBM Plex Mono', monospace; font-size: 13px; padding: 12px; outline: none; transition: border-color 0.2s; line-height: 1.6; resize: vertical; min-height: 120px; }
  textarea:focus { border-color: var(--accent); }
  textarea::placeholder { color: #333; }
  .hint { font-size: 12px; color: var(--muted); margin-top: 6px; }
  .actions { display: flex; gap: 10px; margin-top: 16px; align-items: center; }
  button { font-family: 'IBM Plex Mono', monospace; font-size: 12px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; border: none; border-radius: 6px; padding: 10px 20px; cursor: pointer; transition: all 0.15s; }
  .btn-primary { background: var(--accent); color: #000; }
  .btn-primary:hover { background: #00ffb3; }
  .btn-primary:disabled { background: #1a3d30; color: #2a6a50; cursor: not-allowed; }
  .btn-blue { background: var(--blue); color: #000; }
  .btn-blue:hover { background: #7dc0ff; }
  .btn-blue:disabled { background: #1a2a3d; color: #2a4a6a; cursor: not-allowed; }
  .btn-ghost { background: transparent; color: var(--muted); border: 1px solid var(--border2); }
  .btn-ghost:hover { color: var(--text); border-color: #444; }
  .progress-bar { height: 2px; background: var(--border); border-radius: 2px; margin-top: 16px; overflow: hidden; display: none; }
  .progress-fill { height: 100%; background: var(--accent); border-radius: 2px; transition: width 0.3s; width: 0%; }
  .progress-fill.blue { background: var(--blue); }
  .stats { display: none; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 16px; }
  .stat { background: var(--surface); border: 1px solid var(--border); border-radius: 6px; padding: 14px; text-align: center; }
  .stat-num { font-family: 'IBM Plex Mono', monospace; font-size: 22px; font-weight: 600; line-height: 1; margin-bottom: 4px; }
  .stat-label { font-size: 11px; color: var(--muted); text-transform: uppercase; letter-spacing: 0.08em; }
  .stat-num.green { color: var(--accent); }
  .stat-num.red { color: var(--red); }
  .stat-num.blue { color: var(--blue); }
  .results { display: none; }
  .result-header { display: grid; gap: 12px; padding: 8px 14px; font-family: 'IBM Plex Mono', monospace; font-size: 10px; letter-spacing: 0.1em; color: var(--muted); text-transform: uppercase; border-bottom: 1px solid var(--border); margin-bottom: 4px; }
  .rh-likes { grid-template-columns: 1fr 160px 80px; }
  .rh-uid { grid-template-columns: 1fr 160px 60px; }
  .result-item { display: grid; gap: 12px; padding: 10px 14px; border-radius: 6px; margin-bottom: 3px; align-items: center; transition: background 0.1s; animation: fadeIn 0.2s ease; }
  .ri-likes { grid-template-columns: 1fr 160px 80px; }
  .ri-uid { grid-template-columns: 1fr 160px 60px; }
  .result-item:hover { background: #151515; }
  @keyframes fadeIn { from { opacity:0; transform:translateY(4px); } to { opacity:1; transform:none; } }
  .uid-link { font-family: 'IBM Plex Mono', monospace; font-size: 13px; color: var(--text); text-decoration: none; display: flex; align-items: center; gap: 6px; overflow: hidden; }
  .uid-link span { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .uid-link .ic { font-size: 10px; opacity: 0.4; flex-shrink: 0; }
  .uid-link:hover { color: var(--accent); }
  .badge { display: inline-flex; align-items: center; gap: 5px; font-family: 'IBM Plex Mono', monospace; font-size: 11px; font-weight: 600; padding: 4px 10px; border-radius: 4px; letter-spacing: 0.05em; white-space: nowrap; }
  .b-likes { background: var(--accent-dim); color: var(--accent); }
  .b-followers { background: var(--red-dim); color: var(--red); }
  .b-error { background: rgba(255,209,102,0.08); color: var(--yellow); }
  .b-loading { background: rgba(255,255,255,0.04); color: var(--muted); animation: pulse 1s infinite; }
  .b-uid { background: var(--blue-dim); color: var(--blue); }
  @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.4} }
  .dot { width:6px; height:6px; border-radius:50%; display:inline-block; }
  .dg { background:var(--accent); } .dr { background:var(--red); } .db { background:var(--blue); }
  .copy-btn { background: transparent; border: 1px solid var(--border2); color: var(--muted); font-size: 10px; padding: 4px 8px; border-radius: 4px; cursor: pointer; font-family: 'IBM Plex Mono', monospace; text-transform: uppercase; letter-spacing: 0.05em; }
  .copy-btn:hover { color: var(--text); border-color: #444; }
  .export-row { margin-top: 14px; justify-content: flex-end; gap: 8px; display: none; }
</style>
</head>
<body>
<div class="wrap">
  <header>
    <div class="logo">FB Tool</div>
    <h1>Page <span>Likes</span> Checker</h1>
    <p class="subtitle">Kiểm tra fanpage — hàng loạt, không cần token</p>
  </header>

  <div class="tabs">
    <button class="tab active" onclick="switchTab('check',this)">✦ Check Likes</button>
    <button class="tab" onclick="switchTab('uid',this)">⟳ Link → UID</button>
  </div>

  <!-- Tab Check Likes -->
  <div class="tab-content active" id="tab-check">
    <div class="card">
      <label>Danh sách UID (mỗi dòng 1 UID)</label>
      <textarea id="uidInput" placeholder="100095080001436&#10;61574841692449&#10;..."></textarea>
      <p class="hint">Dán thoải mái, tool tự bỏ dòng trống và trùng lặp.</p>
      <div class="actions">
        <button class="btn-primary" id="checkBtn" onclick="startCheck()">▶ Bắt đầu check</button>
        <button class="btn-ghost" onclick="clearCheck()">Xóa</button>
        <span id="statusText" style="font-size:12px;color:var(--muted);margin-left:auto;"></span>
      </div>
      <div class="progress-bar" id="progressBar"><div class="progress-fill" id="progressFill"></div></div>
    </div>
    <div class="stats" id="statsRow">
      <div class="stat"><div class="stat-num" id="totalNum">0</div><div class="stat-label">Tổng</div></div>
      <div class="stat"><div class="stat-num green" id="likesNum">0</div><div class="stat-label">Có lượt thích</div></div>
      <div class="stat"><div class="stat-num red" id="noLikesNum">0</div><div class="stat-label">Chỉ followers</div></div>
    </div>
    <div class="results" id="resultsBox">
      <div class="result-header rh-likes"><div>Page UID</div><div>Trạng thái</div><div>Kết quả</div></div>
      <div id="resultsList"></div>
    </div>
    <div class="export-row" id="exportRow">
      <button class="btn-ghost" onclick="exportCSV()">↓ Xuất CSV</button>
      <button class="btn-ghost" onclick="copyLikes()">Copy UID có likes</button>
    </div>
  </div>

  <!-- Tab Link → UID -->
  <div class="tab-content" id="tab-uid">
    <div class="card">
      <label>Danh sách link hoặc username (mỗi dòng 1 cái)</label>
      <textarea id="linkInput" placeholder="https://facebook.com/profile.php?id=61574841692449&#10;https://facebook.com/zuck&#10;fanpagename&#10;..."></textarea>
      <p class="hint">Hỗ trợ link profile.php?id=..., link username, hoặc username thuần. Link có id= sẽ lấy ngay không cần gọi API.</p>
      <div class="actions">
        <button class="btn-blue" id="uidBtn" onclick="startGetUID()">⟳ Lấy UID</button>
        <button class="btn-ghost" onclick="clearUID()">Xóa</button>
        <span id="uidStatus" style="font-size:12px;color:var(--muted);margin-left:auto;"></span>
      </div>
      <div class="progress-bar" id="uidProgressBar"><div class="progress-fill blue" id="uidProgressFill"></div></div>
    </div>
    <div class="stats" id="uidStatsRow">
      <div class="stat"><div class="stat-num" id="uidTotalNum">0</div><div class="stat-label">Tổng</div></div>
      <div class="stat"><div class="stat-num blue" id="uidOkNum">0</div><div class="stat-label">Lấy được UID</div></div>
      <div class="stat"><div class="stat-num red" id="uidErrNum">0</div><div class="stat-label">Thất bại</div></div>
    </div>
    <div class="results" id="uidResultsBox">
      <div class="result-header rh-uid"><div>Link / Username</div><div>UID</div><div>Copy</div></div>
      <div id="uidResultsList"></div>
    </div>
    <div class="export-row" id="uidExportRow">
      <button class="btn-ghost" onclick="exportUIDCSV()">↓ Xuất CSV</button>
      <button class="btn-ghost" onclick="copyAllUIDs()">Copy tất cả UID</button>
      <button class="btn-ghost" onclick="sendToChecker()">→ Gửi sang Check Likes</button>
    </div>
  </div>
</div>

<script>
const API = 'https://check-fanpage-hi-n-n-t-like.onrender.com';
let results = [], uidResults = [], running = false;

function switchTab(name, el) {
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
  el.classList.add('active');
  document.getElementById('tab-' + name).classList.add('active');
}

function parseLines(text) {
  return [...new Set(text.split('\n').map(l=>l.trim()).filter(Boolean))];
}

// ===== CHECK LIKES =====
async function startCheck() {
  if (running) return;
  const uids = parseLines(document.getElementById('uidInput').value);
  if (!uids.length) { alert('Nhập ít nhất 1 UID!'); return; }
  running = true; results = [];
  document.getElementById('checkBtn').disabled = true;
  document.getElementById('progressBar').style.display = 'block';
  document.getElementById('statsRow').style.display = 'grid';
  document.getElementById('resultsBox').style.display = 'block';
  document.getElementById('exportRow').style.display = 'none';
  document.getElementById('resultsList').innerHTML = '';
  document.getElementById('totalNum').textContent = uids.length;
  updateCheckStats();
  for (const uid of uids) addLikesRow(uid);
  let done = 0;
  for (let i = 0; i < uids.length; i += 3) {
    await Promise.all(uids.slice(i,i+3).map(async uid => {
      let r;
      try {
        const res = await fetch(`${API}/check?uid=${uid}`);
        const d = await res.json();
        r = { uid, has_likes: d.has_likes, error: !!d.error };
      } catch(e) { r = { uid, has_likes: false, error: true }; }
      results.push(r); updateLikesRow(uid, r);
      done++;
      document.getElementById('progressFill').style.width = (done/uids.length*100)+'%';
      document.getElementById('statusText').textContent = `${done}/${uids.length}`;
      updateCheckStats();
    }));
  }
  running = false;
  document.getElementById('checkBtn').disabled = false;
  document.getElementById('statusText').textContent = `Xong ${uids.length} page`;
  document.getElementById('exportRow').style.display = 'flex';
}

function addLikesRow(uid) {
  const d = document.createElement('div');
  d.className = 'result-item ri-likes'; d.id = 'lrow-'+uid;
  d.innerHTML = `<a href="https://facebook.com/profile.php?id=${uid}" target="_blank" class="uid-link"><span>${uid}</span><span class="ic">↗</span></a><span class="badge b-loading">Đang check...</span><span style="color:var(--muted)">—</span>`;
  document.getElementById('resultsList').appendChild(d);
}

function updateLikesRow(uid, r) {
  const row = document.getElementById('lrow-'+uid); if (!row) return;
  if (r.error) row.innerHTML = `<a href="https://facebook.com/profile.php?id=${uid}" target="_blank" class="uid-link"><span>${uid}</span><span class="ic">↗</span></a><span class="badge b-error">⚠ Lỗi</span><span style="color:var(--muted)">—</span>`;
  else if (r.has_likes) row.innerHTML = `<a href="https://facebook.com/profile.php?id=${uid}" target="_blank" class="uid-link"><span>${uid}</span><span class="ic">↗</span></a><span class="badge b-likes"><span class="dot dg"></span>Có lượt thích</span><span style="color:var(--accent);font-family:'IBM Plex Mono',monospace;font-size:12px;">✓</span>`;
  else row.innerHTML = `<a href="https://facebook.com/profile.php?id=${uid}" target="_blank" class="uid-link"><span>${uid}</span><span class="ic">↗</span></a><span class="badge b-followers"><span class="dot dr"></span>Chỉ followers</span><span style="color:var(--red);font-family:'IBM Plex Mono',monospace;font-size:12px;">✗</span>`;
}

function updateCheckStats() {
  document.getElementById('likesNum').textContent = results.filter(r=>r.has_likes).length;
  document.getElementById('noLikesNum').textContent = results.filter(r=>!r.has_likes&&!r.error).length;
}

function clearCheck() {
  document.getElementById('uidInput').value='';
  ['resultsList','progressBar','statsRow','resultsBox','exportRow'].forEach(id=>{
    const el=document.getElementById(id); if(el){el.innerHTML=id==='resultsList'?'':undefined; el.style.display='none';}
  });
  document.getElementById('statusText').textContent=''; results=[];
  document.getElementById('progressFill').style.width='0%';
  document.getElementById('progressBar').style.display='none';
  document.getElementById('statsRow').style.display='none';
  document.getElementById('resultsBox').style.display='none';
  document.getElementById('exportRow').style.display='none';
  document.getElementById('resultsList').innerHTML='';
}

function exportCSV() {
  const rows=[['UID','Co_luot_thich','Loi'],...results.map(r=>[r.uid,r.has_likes?'Co':'Khong',r.error?'Co':''])];
  const a=document.createElement('a'); a.href='data:text/csv;charset=utf-8,'+encodeURIComponent(rows.map(r=>r.join(',')).join('\n')); a.download='fb_likes_check.csv'; a.click();
}

function copyLikes() {
  navigator.clipboard.writeText(results.filter(r=>r.has_likes).map(r=>r.uid).join('\n'))
    .then(()=>alert('Đã copy '+results.filter(r=>r.has_likes).length+' UID có likes!'));
}

// ===== LINK → UID =====
function extractUID(raw) {
  const m1 = raw.match(/[?&]id=(\d+)/); if (m1) return { uid: m1[1], needLookup: false };
  const m2 = raw.match(/\/pages\/[^/]+\/(\d+)/); if (m2) return { uid: m2[1], needLookup: false };
  if (/^\d+$/.test(raw)) return { uid: raw, needLookup: false };
  const m3 = raw.match(/facebook\.com\/([^/?&\n]+)/);
  const username = m3 ? m3[1] : raw.replace(/^\/+/,'');
  if (username && username !== 'profile.php') return { uid: null, username, needLookup: true };
  return { uid: null, username: raw, needLookup: true };
}

async function lookupUID(username) {
  try {
    const res = await fetch(`${API}/get-uid?username=${encodeURIComponent(username)}`);
    const d = await res.json();
    return d.uid || null;
  } catch(e) { return null; }
}

async function startGetUID() {
  if (running) return;
  const lines = parseLines(document.getElementById('linkInput').value);
  if (!lines.length) { alert('Nhập ít nhất 1 link!'); return; }
  running = true; uidResults = [];
  document.getElementById('uidBtn').disabled = true;
  document.getElementById('uidProgressBar').style.display = 'block';
  document.getElementById('uidStatsRow').style.display = 'grid';
  document.getElementById('uidResultsBox').style.display = 'block';
  document.getElementById('uidExportRow').style.display = 'none';
  document.getElementById('uidResultsList').innerHTML = '';
  document.getElementById('uidTotalNum').textContent = lines.length;
  for (const raw of lines) addUIDRow(raw);
  let done = 0;
  for (const raw of lines) {
    const parsed = extractUID(raw);
    let uid = parsed.uid;
    if (!uid && parsed.needLookup) uid = await lookupUID(parsed.username);
    const r = { raw, uid: uid||null, error: !uid };
    uidResults.push(r); updateUIDRow(raw, r);
    done++;
    document.getElementById('uidProgressFill').style.width = (done/lines.length*100)+'%';
    document.getElementById('uidStatus').textContent = `${done}/${lines.length}`;
    document.getElementById('uidOkNum').textContent = uidResults.filter(r=>r.uid).length;
    document.getElementById('uidErrNum').textContent = uidResults.filter(r=>!r.uid).length;
  }
  running = false;
  document.getElementById('uidBtn').disabled = false;
  document.getElementById('uidStatus').textContent = `Xong ${lines.length} link`;
  document.getElementById('uidExportRow').style.display = 'flex';
}

function safeId(raw) { return 'urow-' + btoa(unescape(encodeURIComponent(raw))).replace(/[^a-zA-Z0-9]/g,'').slice(0,20) + raw.length; }

function addUIDRow(raw) {
  const short = raw.length>40 ? raw.slice(0,40)+'…' : raw;
  const d = document.createElement('div');
  d.className = 'result-item ri-uid'; d.id = safeId(raw);
  d.innerHTML = `<span style="font-family:'IBM Plex Mono',monospace;font-size:12px;color:var(--muted);overflow:hidden;text-overflow:ellipsis;white-space:nowrap;" title="${raw}">${short}</span><span class="badge b-loading">Đang lấy...</span><span>—</span>`;
  document.getElementById('uidResultsList').appendChild(d);
}

function updateUIDRow(raw, r) {
  const row = document.getElementById(safeId(raw)); if (!row) return;
  const short = raw.length>40 ? raw.slice(0,40)+'…' : raw;
  const label = `<span style="font-family:'IBM Plex Mono',monospace;font-size:12px;color:var(--muted);overflow:hidden;text-overflow:ellipsis;white-space:nowrap;" title="${raw}">${short}</span>`;
  if (!r.uid) {
    row.innerHTML = `${label}<span class="badge b-error">⚠ Không tìm thấy</span><span>—</span>`;
  } else {
    row.innerHTML = `${label}<span class="badge b-uid"><span class="dot db"></span>${r.uid}</span><button class="copy-btn" onclick="navigator.clipboard.writeText('${r.uid}').then(()=>{this.textContent='✓';setTimeout(()=>this.textContent='Copy',1500)})">Copy</button>`;
  }
}

function clearUID() {
  document.getElementById('linkInput').value='';
  document.getElementById('uidResultsList').innerHTML='';
  document.getElementById('uidResultsBox').style.display='none';
  document.getElementById('uidStatsRow').style.display='none';
  document.getElementById('uidProgressBar').style.display='none';
  document.getElementById('uidExportRow').style.display='none';
  document.getElementById('uidStatus').textContent='';
  document.getElementById('uidProgressFill').style.width='0%';
  uidResults=[];
}

function exportUIDCSV() {
  const rows=[['Input','UID','Loi'],...uidResults.map(r=>['"'+r.raw+'"',r.uid||'',r.error?'Co':''])];
  const a=document.createElement('a'); a.href='data:text/csv;charset=utf-8,'+encodeURIComponent(rows.map(r=>r.join(',')).join('\n')); a.download='fb_uid_lookup.csv'; a.click();
}

function copyAllUIDs() {
  navigator.clipboard.writeText(uidResults.filter(r=>r.uid).map(r=>r.uid).join('\n'))
    .then(()=>alert('Đã copy '+uidResults.filter(r=>r.uid).length+' UID!'));
}

function sendToChecker() {
  const uids = uidResults.filter(r=>r.uid).map(r=>r.uid).join('\n');
  document.getElementById('uidInput').value = uids;
  switchTab('check', document.querySelectorAll('.tab')[0]);
}
</script>
</body>
</html>
