# -*- coding: utf-8 -*-
"""组装统一门禁控制面板 v7：
- 视觉：苹果官网设计语言 —— #f5f5f7 浅灰底 / 白卡 18px 圆角 / #0071e3 单一蓝强调 /
  胶囊按钮 / 磨砂玻璃导航 / 充分留白 / 精确字重层级（600 标题 vs 400 正文）
- 缩略图加固：img 显式 width/height；onerror 内联 handler 换成全局捕获监听（CSP 安全），
  加载失败时仅隐藏 img、保留渐变兜底层
- 弹窗随 :root 联动换浅色主题，硬编码深色（tab.active 字色 / payload 深底 / thumb 底 /
  虚线框 / 滚动条）在 PANEL_CSS 尾部统一覆盖
"""
import re, io, os, json, base64

SRC = r"D:\Workbuddy folder\2026-09-29-14-13-12\视频风格选择组件.html"
DST = r"C:\Users\Administrator\.skills\cine-pipeline\tools\门禁控制面板.html"
# 第四门禁使用与风格名逐项校对后的无文字缩略图；旧带字截图保留在 thumbs 便于追溯。
THUMBS = r"C:\Users\Administrator\.skills\cine-pipeline\tools\thumbs_clean"

src = io.open(SRC, encoding="utf-8").read()

# 1) 提取原 <style> 块（仅内容，不含标签），并把调色板整体换新（苹果浅色系）
m = re.search(r"<style>(.*?)</style>", src, re.S)
style_block = m.group(1)
style_block = re.sub(
    r":root\{[^}]*\}",
    """:root{
    --bg:#0b0b0e; --panel:#141419; --panel-2:#1b1b22; --card:#141419;
    --border:rgba(255,255,255,.08); --border-2:rgba(255,255,255,.14);
    --text:#f5f5f7; --text-2:#98989f; --text-3:#6e6e76;
    --accent:#2997ff; --accent-soft:rgba(41,151,255,.14);
    --ok:#30d158; --radius:12px;
  }""",
    style_block, count=1)

# 2) 数据块（217 款风格）
m = re.search(r"/\* ================= 数据：.*?(?=/\* ================= DOM)", src, re.S)
data_block = m.group(0)

# 3) 弹窗 HTML（复用结构；emoji 搜索图标换 SVG，弹窗默认关闭）
m = re.search(r"<!-- 风格选择弹窗 -->(.*?)<script>", src, re.S)
modal_html = m.group(1).replace('class="overlay open"', 'class="overlay"')
modal_html = modal_html.replace(
    '<span class="ico">🔍</span>',
    '<span class="ico"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.8-3.8"/></svg></span>')

# 4) 缩略图 base64 内嵌（不依赖相对路径，任何环境直接显示）
thumb_b64 = {}
for fn in sorted(os.listdir(THUMBS)):
    if fn.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
        raw = open(os.path.join(THUMBS, fn), 'rb').read()
        mime = 'image/jpeg' if fn.lower().endswith(('.jpg', '.jpeg')) else 'image/png'
        thumb_b64[fn] = f"data:{mime};base64,{base64.b64encode(raw).decode('ascii')}"
THUMB_JS = ("/* 缩略图 base64 内嵌：显示用 _thumbSrc；s.thumb 保留原文件名供载荷引用 */\n"
            f"const THUMB_B64 = {json.dumps(thumb_b64)};\n"
            "STYLES.forEach(s=>{ const k=s.thumb.split('/').pop(); if(THUMB_B64[k]) s._thumbSrc=THUMB_B64[k]; });\n")

PANEL_CSS = """
  /* ===== 设计方向 v7：全深色影院模式 + 苹果式渐变字 hero =====
     #0b0b0e 深灰画布 + #141419 深卡片；#2997ff 单一蓝强调（苹果深色模式蓝）；
     选中胶囊白底黑字（Apple Store 深色选择器范式）；磨砂玻璃黑导航；
     黑 hero 58px 大标题 + 蓝紫粉渐变字。 */
  body{background:var(--bg);color:var(--text);font-size:15px;line-height:1.5;
    font-family:-apple-system,BlinkMacSystemFont,"SF Pro Text","SF Pro Display","PingFang SC","Helvetica Neue","Microsoft YaHei",sans-serif;
    -webkit-font-smoothing:antialiased}
  ::selection{background:rgba(41,151,255,.28)}
  *::-webkit-scrollbar{width:10px;height:10px}
  *::-webkit-scrollbar-track{background:transparent}
  *::-webkit-scrollbar-thumb{background:#2e2e36;border-radius:5px;border:3px solid var(--bg)}
  *::-webkit-scrollbar-thumb:hover{background:#3f3f48}
  :focus-visible{outline:2px solid var(--accent);outline-offset:2px;border-radius:6px}

  /* ===== 磨砂玻璃黑顶栏 ===== */
  .topbar{position:sticky;top:0;z-index:50;background:rgba(11,11,14,.72);
    -webkit-backdrop-filter:saturate(180%) blur(20px);backdrop-filter:saturate(180%) blur(20px);
    border-bottom:1px solid rgba(255,255,255,.08);padding:14px 24px;display:flex;align-items:center;gap:12px}
  .topbar::after{content:'';position:absolute;left:0;right:0;bottom:-1px;height:2px;
    background:var(--accent);transform-origin:left;transform:scaleX(var(--prog,0));transition:transform .5s cubic-bezier(.2,.7,.2,1)}
  .topbar .logo{color:var(--accent);flex:none;display:flex;align-items:center}
  .topbar h1{font-size:15px;font-weight:600;letter-spacing:-.01em;color:var(--text)}
  .topbar .sub{font-size:12px;color:var(--text-3);margin-top:1px}
  .topbar .chip-count{margin-left:auto;font-size:12px;color:var(--text-2);background:var(--panel-2);
    border:1px solid rgba(255,255,255,.08);border-radius:980px;padding:6px 14px;white-space:nowrap;font-variant-numeric:tabular-nums}
  .topbar .chip-count b{color:var(--accent);font-weight:600}

  /* ===== Hero：黑底电影感大区块（苹果产品页黑白交替范式） ===== */
  .wrap{max-width:880px;margin:0 auto;padding:28px 22px 48px}
  .hero{background:linear-gradient(to bottom,#000 55%,#0b0b0e 100%);
    padding:104px 24px 88px;text-align:center;position:relative;overflow:hidden}
  .hero::before{content:'';position:absolute;inset:0;background:
    radial-gradient(52% 60% at 50% 108%,rgba(41,151,255,.28),transparent 70%),
    radial-gradient(38% 46% at 82% 118%,rgba(255,95,162,.16),transparent 70%);
    pointer-events:none}
  .hero .kicker{display:inline-block;font-size:13px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;
    color:#86868b;margin-bottom:22px}
  .hero h2{font-size:58px;font-weight:600;letter-spacing:-.028em;line-height:1.06;color:#f5f5f7;
    margin:0 auto;white-space:nowrap;position:relative}
  @media (max-width:640px){.hero h2{font-size:30px;letter-spacing:-.02em}}
  .hero h2 .grad-text{background:linear-gradient(96deg,#2997ff 2%,#6a5bff 48%,#ff5fa2 96%);
    -webkit-background-clip:text;background-clip:text;color:transparent}
  .hero p{font-size:19px;color:#86868b;margin-top:20px;line-height:1.5;max-width:56ch;
    margin-left:auto;margin-right:auto;position:relative}

  /* ===== 门禁卡片：深卡 + 20px 圆角 + 悬浮阴影层次 ===== */
  .gate{background:var(--panel);border-radius:20px;padding:30px 32px 32px;margin-bottom:22px;
    box-shadow:0 2px 10px rgba(0,0,0,.3);transition:box-shadow .3s}
  .gate:hover{box-shadow:0 8px 24px rgba(0,0,0,.4)}
  .gate.done{box-shadow:0 0 0 1.5px rgba(41,151,255,.45),0 8px 24px rgba(0,0,0,.4)}
  .gate-head{display:flex;align-items:center;gap:12px;margin-bottom:5px}
  .gate-head .num{width:24px;height:24px;border-radius:50%;color:var(--text-3);font-size:11px;font-weight:600;
    font-variant-numeric:tabular-nums;display:flex;align-items:center;justify-content:center;flex:none;
    background:#26262e;transition:.25s}
  .gate.done .gate-head .num{color:#0b0b0e;background:var(--accent)}
  @keyframes pop{from{transform:scale(.4);opacity:0}to{transform:scale(1);opacity:1}}
  .gate.done .gate-head .num{animation:pop .22s cubic-bezier(.2,.8,.3,1.25)}
  .gate-head h3{font-size:19px;font-weight:600;color:var(--text);letter-spacing:-.014em}
  .gate-head .req{font-size:10.5px;color:var(--text-3);border:1px solid rgba(255,255,255,.1);background:var(--panel-2);
    border-radius:980px;padding:2.5px 9px;flex:none;font-weight:600;letter-spacing:.05em}
  .gate.done .gate-head .req{display:none}
  .gate-head .ok-flag{font-size:12px;color:var(--accent);font-weight:600;display:none;margin-left:1px}
  .gate.done .gate-head .ok-flag{display:inline-flex;align-items:center;gap:4px}
  .gate .hint{font-size:13px;color:var(--text-3);margin:3px 0 19px;line-height:1.6}

  /* ===== 胶囊 chips（Apple Store 深色选择器范式：选中 = 白底黑字） ===== */
  .chips{display:flex;flex-wrap:wrap;gap:9px}
  .chip{border:1px solid rgba(255,255,255,.16);background:var(--panel-2);color:var(--text);font-size:14px;
    padding:9px 18px;border-radius:980px;cursor:pointer;transition:background .18s,border-color .18s,color .18s;
    font-family:inherit;display:inline-flex;align-items:center;gap:8px}
  .chip:hover{background:#20202a;border-color:rgba(255,255,255,.22)}
  .chip:active{transform:scale(.97)}
  .chip.active{background:#f5f5f7;border-color:#f5f5f7;color:#0b0b0e;font-weight:600}
  .chip .tag{font-size:11px;opacity:.62;font-weight:400}

  /* ===== 画幅：深底内嵌瓦片，选中 = 蓝环 ===== */
  .ratios{display:grid;grid-template-columns:repeat(auto-fill,minmax(122px,1fr));gap:10px}
  .ratio-card{background:var(--panel-2);border-radius:14px;cursor:pointer;
    padding:19px 8px 14px;display:flex;flex-direction:column;align-items:center;gap:11px;transition:.18s;
    color:var(--text-2)}
  .ratio-card:hover{background:#20202a}
  .ratio-card:active{transform:scale(.97)}
  .ratio-card.active{background:#20202a;box-shadow:0 0 0 2px var(--accent)}
  .ratio-box{border:1.5px solid #4a4a52;border-radius:4px;background:#101015;transition:.18s}
  .ratio-card.active .ratio-box{border-color:var(--accent)}
  .ratio-label{font-size:14px;font-weight:600;color:var(--text);font-variant-numeric:tabular-nums;letter-spacing:-.01em}
  .ratio-card.active .ratio-label{color:var(--accent)}
  .ratio-orient{font-size:10.5px;color:var(--text-3)}

  /* ===== 时长 ===== */
  .dur-chips{display:flex;gap:9px;margin-bottom:20px;flex-wrap:wrap}
  .dur-readout{display:flex;align-items:baseline;gap:9px;margin-bottom:12px}
  .dur-readout .val{font-size:56px;font-weight:600;font-variant-numeric:tabular-nums;letter-spacing:-.03em;color:var(--text);line-height:1}
  .dur-readout .unit{font-size:13px;color:var(--text-3)}
  .dur-readout .seg{font-size:12px;color:var(--text-3);margin-left:auto;background:var(--panel-2);
    border-radius:980px;padding:6px 13px;font-variant-numeric:tabular-nums}
  .dur-readout .seg b{color:var(--text-2);font-weight:600}
  input[type=range]{-webkit-appearance:none;appearance:none;width:100%;height:4px;border-radius:2px;outline:none;cursor:pointer;
    background:linear-gradient(90deg,var(--accent) 0%,var(--accent) var(--fill,25%),#3a3a42 var(--fill,25%),#3a3a42 100%)}
  input[type=range]:focus-visible{outline:2px solid var(--accent);outline-offset:6px;border-radius:6px}
  input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:24px;height:24px;border-radius:50%;
    background:#fff;border:none;box-shadow:0 1px 4px rgba(0,0,0,.25),0 4px 10px rgba(0,0,0,.08);cursor:grab;transition:transform .12s}
  input[type=range]::-webkit-slider-thumb:active{cursor:grabbing;transform:scale(1.08)}
  input[type=range]::-moz-range-thumb{width:24px;height:24px;border-radius:50%;background:#fff;
    border:none;box-shadow:0 1px 4px rgba(0,0,0,.25);cursor:grab}
  .dur-ticks{position:relative;height:14px;font-size:10.5px;color:var(--text-3);margin-top:10px;font-variant-numeric:tabular-nums}
  .dur-ticks span{position:absolute;transform:translateX(-50%);white-space:nowrap}
  .dur-note{font-size:12px;color:var(--text-3);margin-top:14px;line-height:1.6;max-width:75ch}

  /* ===== 选项卡（声音/命名）：深底瓦片，选中 = 蓝环 ===== */
  .sound-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:10px}
  .opt-card{background:var(--panel-2);border:none;border-radius:14px;cursor:pointer;
    padding:15px 17px;transition:.18s;color:var(--text-2);font-family:inherit;text-align:left}
  .opt-card:hover{background:#20202a}
  .opt-card:active{transform:scale(.98)}
  .opt-card.active{background:#20202a;box-shadow:0 0 0 2px var(--accent)}
  .opt-card .t{font-size:14px;font-weight:600;display:flex;align-items:center;gap:8px;color:var(--text)}
  .opt-card .t svg{flex:none;color:var(--text-3)}
  .opt-card.active .t svg{color:var(--accent)}
  .opt-card .d{font-size:12px;color:var(--text-3);margin-top:6px;line-height:1.55}

  /* ===== 画风当前选择 ===== */
  .style-current{display:flex;align-items:center;gap:18px;background:var(--panel-2);
    border-radius:14px;padding:16px 18px;min-height:96px;transition:box-shadow .25s}
  .style-current.has-style{background:#20202a;box-shadow:0 0 0 1.5px rgba(41,151,255,.45)}
  .style-current .sthumb{width:152px;height:86px;border-radius:10px;overflow:hidden;flex:none;position:relative;
    background:#26262e;box-shadow:0 2px 10px rgba(0,0,0,.45)}
  .style-current .sthumb img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block}
  .style-current .sname{font-size:15px;font-weight:600;color:var(--text);letter-spacing:-.01em}
  .style-current .scat{display:inline-block;font-size:11px;color:var(--text-2);background:#26262e;
    border-radius:980px;padding:2.5px 9px;margin:7px 0 3px}
  .style-current .sdesc{font-size:12px;color:var(--text-3);margin-top:5px;line-height:1.55;
    display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
  .style-current .empty{font-size:13px;color:var(--text-3);line-height:1.7}
  .style-current .btn{margin-left:auto;flex:none}
  .style-current .btn-ghost{margin-top:0}

  /* ===== 弹窗深色化修正（原组件硬编码项随新 :root 联动后的适配） ===== */
  .overlay{background:rgba(0,0,0,.6)}
  .modal{border:none;border-radius:20px;box-shadow:0 32px 90px rgba(0,0,0,.6)}
  .modal .card.selected .check{color:#fff}
  .tab.active{background:#f5f5f7;color:#1d1d1f;border-color:#f5f5f7}
  .tab.fav-tab.active .star{color:#c99700}
  .thumb{background:#26262e}
  .card.custom .thumb{border:2px dashed #3a3a42}
  .grid-wrap{scrollbar-color:#3a3a42 transparent}
  .btn-primary:disabled{background:#26262e;color:#6e6e76;filter:none}
  .search-bar{background:var(--panel-2)}

  /* ===== 结果载荷：深底代码块 ===== */
  .result-card{margin-top:28px;background:var(--panel);border-radius:20px;
    padding:26px 28px;display:none;box-shadow:0 2px 10px rgba(0,0,0,.3)}
  .result-card.show{display:block}
  .result-card .label{font-size:12px;color:var(--text-3);margin-bottom:6px;letter-spacing:.05em;font-weight:600}
  .payload{margin-top:12px;border-radius:14px;background:#0a0a0d;border:1px solid rgba(255,255,255,.07);
    padding:18px 20px;font-family:"SF Mono","Menlo","Cascadia Mono","Consolas",monospace;font-size:12px;line-height:1.8;
    color:#c9c9d1;white-space:pre-wrap;word-break:break-all}
  .payload-head{display:flex;align-items:center;justify-content:space-between;margin-top:14px;margin-bottom:8px}
  .payload-head .t{font-size:12px;color:var(--text-3)}
  .btn{display:inline-flex;align-items:center;justify-content:center;gap:6px;border:none;cursor:pointer;
    font-size:14px;font-weight:600;border-radius:980px;padding:11px 24px;transition:background .18s,transform .12s;font-family:inherit}
  .btn:active{transform:scale(.98)}
  .btn-primary{background:var(--accent);color:#fff}
  .btn-primary:hover{background:#3da2ff}
  .btn-primary:disabled{background:#26262e;color:#6e6e76;cursor:not-allowed}
  .btn-ghost{background:transparent;color:var(--text-2);border:1px solid rgba(255,255,255,.18);margin-top:14px}
  .btn-ghost:hover{color:var(--text);border-color:rgba(255,255,255,.32);background:var(--panel-2)}
  .btn-copy{background:transparent;color:var(--accent);border:1px solid rgba(41,151,255,.4);
    font-size:11.5px;padding:5px 14px;border-radius:980px;cursor:pointer;font-family:inherit;transition:.18s;margin-top:0}
  .btn-copy:hover{background:var(--accent-soft);border-color:var(--accent)}
  .btn-copy.done{color:var(--ok);border-color:var(--ok)}

  /* ===== 磨砂玻璃黑底栏 ===== */
  .footbar{position:sticky;bottom:0;z-index:50;background:rgba(11,11,14,.72);
    -webkit-backdrop-filter:saturate(180%) blur(20px);backdrop-filter:saturate(180%) blur(20px);
    border-top:1px solid rgba(255,255,255,.08);padding:13px 24px;display:flex;align-items:center;gap:16px}
  .footbar .status{font-size:13px;color:var(--text-2);font-variant-numeric:tabular-nums}
  .footbar .status b{color:var(--accent);font-weight:600}
  .footbar .ver{font-size:11px;color:#3a3a42;font-variant-numeric:tabular-nums;margin-left:4px}
  .footbar .btn{margin-left:auto}
"""

PANEL_BODY = """
<header class="topbar" id="topbar">
  <div class="logo">
    <svg width="21" height="21" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M20.2 6 3 11l-.9-2.4c-.3-1.1.3-2.2 1.4-2.5l13.5-4c1.1-.3 2.2.3 2.5 1.4Z"/><path d="m6.2 5.3 3.1 3.9"/><path d="m12.4 3.4 3.1 4"/><path d="M3 11h18v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2Z"/></svg>
  </div>
  <div>
    <h1>制作门禁</h1>
    <div class="sub">cine-pipeline · Stage 3 输入门禁</div>
  </div>
  <div class="chip-count">已确认 <b id="gateCount">0</b> / 8</div>
</header>

<main>
  <section class="hero">
    <div class="kicker">cine-pipeline · Stage 3</div>
    <h2>八项门禁，<span class="grad-text">一键锁定</span></h2>
    <p id="handoffHint">逐项选定后生成项目档案。通过任务接收通道打开时，点击即可自动回传并继续下一步。</p>
  </section>

  <div class="wrap">
  <!-- 1 目标模型 -->
  <section class="gate" id="gate-model">
    <div class="gate-head"><span class="num">1</span><h3>目标模型</h3><span class="req">必选</span><span class="ok-flag"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="m4 12.5 5 5L20 6.5"/></svg>已锁定</span></div>
    <p class="hint">决定单段时长上限、提示词格式与适配器；未说明时按 Seedance 2.5 默认推进。</p>
    <div class="chips" data-gate="model">
      <button class="chip" data-val="Seedance 2.5" data-cap="12">Seedance 2.5 <span class="tag">单段≤12s · 推荐</span></button>
      <button class="chip" data-val="MiniMax H3" data-cap="15">MiniMax H3 <span class="tag">单段≤15s</span></button>
      <button class="chip" data-val="其他模型" data-cap="0">其他模型 <span class="tag">generic 适配</span></button>
    </div>
  </section>

  <!-- 2 资产图提示词平台 -->
  <section class="gate" id="gate-image-prompt">
    <div class="gate-head"><span class="num">2</span><h3>资产图提示词平台</h3><span class="req">二选一</span><span class="ok-flag"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="m4 12.5 5 5L20 6.5"/></svg>已锁定</span></div>
    <p class="hint">决定角色、场景、道具资产图的提示词写法与字符预算；不改变视频分镜提示词格式。</p>
    <div class="sound-grid" data-gate="imagePrompt">
      <button class="opt-card" data-val="ChatGPT"><span class="t">ChatGPT 提示词</span><span class="d">自然语言指令式，可分段写布局、关系和文字；交付预算 ≤4000 字符</span></button>
      <button class="opt-card" data-val="Midjourney"><span class="t">Midjourney 提示词</span><span class="d">英文短语压缩，参数统一置尾；交付预算 ≤1200 字符</span></button>
    </div>
  </section>

  <!-- 3 片型 -->
  <section class="gate" id="gate-genre">
    <div class="gate-head"><span class="num">3</span><h3>片型</h3><span class="req">必选</span><span class="ok-flag"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="m4 12.5 5 5L20 6.5"/></svg>已锁定</span></div>
    <p class="hint">决定题材模块、节奏基准与成片规格预期。</p>
    <div class="chips" data-gate="genre">
      <button class="chip" data-val="短剧">短剧</button>
      <button class="chip" data-val="短片">短片</button>
      <button class="chip" data-val="电影级">电影级</button>
      <button class="chip" data-val="MV">MV</button>
      <button class="chip" data-val="预告片">预告片</button>
      <button class="chip" data-val="广告">广告</button>
    </div>
  </section>

  <!-- 4 画面比例 -->
  <section class="gate" id="gate-ratio">
    <div class="gate-head"><span class="num">4</span><h3>画面比例</h3><span class="req">必选</span><span class="ok-flag"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="m4 12.5 5 5L20 6.5"/></svg>已锁定</span></div>
    <p class="hint">画幅未说明必须问、禁止自行假设——点一下就算你说了。</p>
    <div class="ratios" id="ratioCards"></div>
  </section>

  <!-- 5 画风 -->
  <section class="gate" id="gate-style">
    <div class="gate-head"><span class="num">5</span><h3>画风（视觉风格）</h3><span class="req">必选</span><span class="ok-flag"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="m4 12.5 5 5L20 6.5"/></svg>已锁定</span></div>
    <p class="hint">217 款预设按风格库截图逐格校对；支持搜索、分类、收藏与自定义描述。确认后按 style-library 五要素转写为风格基座。</p>
    <div class="style-current" id="styleCurrent">
      <div class="empty">尚未选择画风<br>点击右侧按钮打开风格库</div>
      <button class="btn btn-ghost" id="openStyleBtn">选择画风</button>
    </div>
  </section>

  <!-- 6 时长 -->
  <section class="gate" id="gate-duration">
    <div class="gate-head"><span class="num">6</span><h3>成片时长</h3><span class="req">必选</span><span class="ok-flag"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="m4 12.5 5 5L20 6.5"/></svg>已锁定</span></div>
    <p class="hint">时长门禁三选一：快节奏版 / 正常语速版 / 自定义；拖动滑块即自定义。信息流素材（15–30 秒）点快捷档。</p>
    <div class="dur-chips">
      <button class="chip" data-mode="快节奏版" data-val="75">快节奏版 <span class="tag">≈75s</span></button>
      <button class="chip" data-mode="正常语速版" data-val="120">正常语速版 <span class="tag">≈120s</span></button>
      <button class="chip" data-mode="自定义时长" data-val="15">信息流 <span class="tag">15s</span></button>
      <button class="chip" data-mode="自定义时长" data-val="21">信息流 <span class="tag">21s</span></button>
      <button class="chip" data-mode="自定义时长" data-val="30">信息流 <span class="tag">30s</span></button>
      <button class="chip" data-mode="自定义时长">自定义时长</button>
    </div>
    <div class="dur-readout">
      <span class="val" id="durVal">2:00</span><span class="unit" id="durUnit">分:秒</span>
      <span class="seg" id="segInfo">约 <b>10</b> 个生成段（按单段上限 12s）</span>
    </div>
    <input type="range" id="durSlider" min="15" max="300" step="1" value="120" aria-label="成片时长">
    <div class="dur-ticks"><span style="left:0;transform:none">15秒</span><span style="left:5.3%">30秒</span><span style="left:15.8%">1分</span><span style="left:36.8%">2分</span><span style="left:57.9%">3分</span><span style="left:78.9%">4分</span><span style="left:100%;transform:translateX(-100%)">5分</span></div>
    <p class="dur-note">滑块范围 15–300 秒（信息流 15–30 秒 / 剧集 1–5 分钟）；时长将作为分镜排期的全片总预算，各段合计必须与该值一致。台词逐字保留；按所选时长及用户明确允许的误差排镜，不用固定字速上限要求删词或擅自延长。</p>
  </section>

  <!-- 7 声音策略 -->
  <section class="gate" id="gate-sound">
    <div class="gate-head"><span class="num">7</span><h3>声音策略</h3><span class="req">必选</span><span class="ok-flag"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="m4 12.5 5 5L20 6.5"/></svg>已锁定</span></div>
    <p class="hint">决定台词字段写法、语速校验口径、音效字段密度与口型要求。</p>
    <div class="sound-grid" data-gate="sound">
      <button class="opt-card" data-val="模型原生对白"><span class="t"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" x2="12" y1="19" y2="22"/></svg>模型原生对白</span><span class="d">视频模型直接生成对白与环境声，音色锚点写进分段提示词</span></button>
      <button class="opt-card" data-val="后期配音"><span class="t"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M3 18v-6a9 9 0 0 1 18 0v6"/><path d="M21 19a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3zM3 19a2 2 0 0 0 2 2h1a2 2 0 0 0 2-2v-3a2 2 0 0 0-2-2H3z"/></svg>后期配音</span><span class="d">TTS/克隆音色后期贴声，提示词不写声音字段</span></button>
      <button class="opt-card" data-val="混合"><span class="t"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M2 18h1.4c1.3 0 2.5-.6 3.3-1.7l6.1-8.6c.7-1.1 2-1.7 3.3-1.7H22"/><path d="m18 2 4 4-4 4"/><path d="M2 6h1.9c1.5 0 2.9.9 3.6 2.2"/><path d="M22 18h-5.9c-1.3 0-2.6-.7-3.3-1.8l-.5-.8"/><path d="m18 14 4 4-4 4"/></svg>混合</span><span class="d">关键对白模型原生，其余后期；分段标注路由</span></button>
      <button class="opt-card" data-val="静默"><span class="t"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4.7 6.5 8.5H3a1 1 0 0 0-1 1v5a1 1 0 0 0 1 1h3.5L11 19.3a.7.7 0 0 0 1.1-.5V5.2a.7.7 0 0 0-1.1-.5Z"/><path d="m16 9.5 5 5"/><path d="m21 9.5-5 5"/></svg>静默</span><span class="d">氛围短片/MV 用；仅环境声或歌词轨</span></button>
    </div>
  </section>

  <!-- 8 资产命名规则 -->
  <section class="gate" id="gate-naming">
    <div class="gate-head"><span class="num">8</span><h3>资产命名规则</h3><span class="req">二选一</span><span class="ok-flag"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="m4 12.5 5 5L20 6.5"/></svg>已锁定</span></div>
    <p class="hint">决定资产表与投喂提示词中 @ 实体的写法，全片统一。</p>
    <div class="sound-grid" data-gate="naming">
      <button class="opt-card" data-val="即梦"><span class="t">即梦</span><span class="d">资产名＋空格；投喂代码块内一律不加 @</span></button>
      <button class="opt-card" data-val="ShuoCanvas"><span class="t">ShuoCanvas</span><span class="d">@资产名＋空格；代码块内保留 @ 引用</span></button>
    </div>
  </section>

  <div class="result-card" id="resultCard">
    <div class="label">项目档案 · 制作门禁（回传载荷）</div>
    <div class="payload-head">
      <span class="t" id="handoffStatus" role="status" aria-live="polite">等待生成项目档案</span>
      <button class="btn-copy" id="copyBtn">复制</button>
    </div>
    <div class="payload" id="payload"></div>
  </div>
  </div>
</main>

<footer class="footbar">
  <span class="status">已确认 <b id="gateCount2">0</b> / 8 项门禁</span><span class="ver">v7</span>
  <button class="btn btn-primary" id="genBtn" disabled>生成项目档案</button>
</footer>
"""

PANEL_JS = """
/* ================= DOM ================= */
const $ = id => document.getElementById(id);
$('totalCount').textContent = STYLES.length;

/* 缩略图兜底：加载失败只隐藏 img（渐变底保留）。不用内联 onerror，CSP 安全。 */
document.addEventListener('error', e=>{
  if(e.target && e.target.tagName==='IMG') e.target.style.opacity='0';
}, true);

/* ================= 面板门禁状态 ================= */
const handoff = window.__PIPELINE_HANDOFF__ || null;
const LS_GATES = handoff ? 'pipelineGates:' + handoff.session : 'pipelineGates';
let handoffBusy = false, handoffDone = false;
if(handoff){
  $('genBtn').textContent = '生成项目档案并继续';
  $('handoffHint').textContent = '已连接当前任务。选好后点击「生成项目档案并继续」，参数自动回传，无需复制粘贴。';
} else {
  $('handoffHint').textContent = '当前为独立文件模式，尚未连接任务接收通道；生成的档案只保存在浏览器，不能自动回传。';
}
const RATIOS = [
  {r:'21:9', w:121, h:52, orient:'横屏宽幅'},
  {r:'16:9', w:92,  h:52, orient:'横屏'},
  {r:'4:3',  w:69,  h:52, orient:'横屏'},
  {r:'1:1',  w:52,  h:52, orient:'方形'},
  {r:'3:4',  w:39,  h:52, orient:'竖屏'},
  {r:'9:16', w:29,  h:52, orient:'竖屏'},
];
const gates = {
  model:null, modelCap:12,
  imagePrompt:null,
  genre:null, ratio:null, style:null,
  durMode:null, dur:120,
  sound:null, naming:null
};

/* ---------- 通用渲染 ---------- */
function fmtDur(s){ return s<60 ? s+'秒' : Math.floor(s/60)+':'+String(s%60).padStart(2,'0'); }
function segCount(){ return gates.modelCap>0 ? Math.ceil(gates.dur/gates.modelCap) : null; }
function renderDur(){
  $('durVal').textContent = fmtDur(gates.dur);
  $('durUnit').textContent = gates.dur<60 ? '总时长' : '分:秒';
  const sl = $('durSlider');
  sl.value = gates.dur;
  sl.style.setProperty('--fill', ((gates.dur-15)/285*100)+'%');
  const n = segCount();
  $('segInfo').innerHTML = n ? `约 <b>${n}</b> 个生成段（按单段上限 ${gates.modelCap}s）`
                            : `单段上限待定（${gates.model||'未选模型'}）`;
}
function gateDone(id, ok){ $(id).classList.toggle('done', ok); updateCount(); }
function updateCount(){
  const done = ['gate-model','gate-image-prompt','gate-genre','gate-ratio','gate-style','gate-duration','gate-sound','gate-naming']
    .filter(x=>$(x).classList.contains('done')).length;
  $('gateCount').textContent = done; $('gateCount2').textContent = done;
  $('topbar').style.setProperty('--prog', (done/8).toFixed(3));
  $('genBtn').disabled = done<8 || handoffBusy || handoffDone;
}

/* ---------- 画幅卡片 ---------- */
function renderRatios(){
  $('ratioCards').innerHTML = RATIOS.map(x=>`
    <div class="ratio-card ${gates.ratio===x.r?'active':''}" data-r="${x.r}">
      <div class="ratio-box" style="width:${x.w}px;height:${x.h}px"></div>
      <span class="ratio-label">${x.r}</span>
      <span class="ratio-orient">${x.orient}</span>
    </div>`).join('');
  $('ratioCards').querySelectorAll('.ratio-card').forEach(c=>{
    c.onclick = ()=>{ gates.ratio=c.dataset.r; renderRatios(); gateDone('gate-ratio',true); };
  });
}

/* ---------- chips（视频模型/资产图提示词平台/片型/声音/命名） ---------- */
document.querySelectorAll('.chips[data-gate], .sound-grid[data-gate]').forEach(box=>{
  const key = box.dataset.gate;
  box.querySelectorAll('.chip, .opt-card').forEach(btn=>{
    btn.onclick = ()=>{
      box.querySelectorAll('.chip, .opt-card').forEach(b=>b.classList.remove('active'));
      btn.classList.add('active');
      gates[key] = btn.dataset.val;
      if(key==='model'){ gates.modelCap = +btn.dataset.cap || 0; renderDur(); }
      const map = {model:'gate-model', imagePrompt:'gate-image-prompt', genre:'gate-genre', sound:'gate-sound', naming:'gate-naming'};
      gateDone(map[key], true);
    };
  });
});

/* ---------- 时长 ---------- */
document.querySelectorAll('.dur-chips .chip').forEach(btn=>{
  btn.onclick = ()=>{
    document.querySelectorAll('.dur-chips .chip').forEach(b=>b.classList.remove('active'));
    btn.classList.add('active');
    gates.durMode = btn.dataset.mode;
    if(btn.dataset.val){ gates.dur = +btn.dataset.val; renderDur(); }
    gateDone('gate-duration', true);
  };
});
$('durSlider').addEventListener('input', ()=>{
  gates.dur = +$('durSlider').value;
  gates.durMode = '自定义时长';
  document.querySelectorAll('.dur-chips .chip').forEach(b=>{
    b.classList.toggle('active', b.dataset.mode==='自定义时长' && !b.dataset.val);
  });
  renderDur(); gateDone('gate-duration', true);
});

/* ---------- 画风：面板卡片（含缩略图直显）+ 弹窗 ---------- */
function renderStyleCard(){
  const box = $('styleCurrent');
  box.classList.toggle('has-style', !!gates.style);
  if(gates.style && gates.style.type==='preset'){
    const s = gates.style.style;
    box.innerHTML = `
      <div class="sthumb">${thumbHTML(s, STYLES.indexOf(s))}</div>
      <div style="min-width:0;flex:1">
        <div class="sname">${s.name} ${favorites.has(s.name)?'<span style="color:#ffd60a">★</span>':''}</div>
        <span class="scat">${CAT_NAME[s.cat]} / ${FAMILY_NAME[s.family]}</span>
        <div class="sdesc">确认后按 style-library 五要素转写为全片风格基座</div>
      </div>
      <button class="btn btn-ghost" id="openStyleBtn">更换画风</button>`;
  } else if(gates.style && gates.style.type==='custom'){
    box.innerHTML = `
      <div class="sthumb"><div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;color:#6e6e76"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"/><path d="m15 5 4 4"/></svg></div></div>
      <div style="min-width:0;flex:1">
        <div class="sname">自定义风格</div>
        <span class="scat">用户描述</span>
        <div class="sdesc">${(state.customText||'').trim().slice(0,90)||'（空描述）'}</div>
      </div>
      <button class="btn btn-ghost" id="openStyleBtn">更换画风</button>`;
  } else {
    box.innerHTML = `<div class="empty">尚未选择画风<br>点击右侧按钮打开风格库</div>
      <button class="btn btn-ghost" id="openStyleBtn">选择画风</button>`;
  }
  $('openStyleBtn').onclick = openModal;
  gateDone('gate-style', !!gates.style);
}

/* ---------- 弹窗逻辑（复用原组件） ---------- */
function favList(){ return STYLES.filter(s=>favorites.has(s.name)); }
function currentList(){
  let list;
  if(state.tab==='fav') list = favList();
  else if(state.tab==='all') list = STYLES;
  else list = STYLES.filter(s=>s.cat===state.tab);
  const q = state.q.trim();
  if(q) list = list.filter(s=>s.name.includes(q)||CAT_NAME[s.cat].includes(q)||FAMILY_NAME[s.family].includes(q));
  return list;
}
function renderTabs(){
  const defs=[['fav','★ 常用',favList().length],['all','全部',STYLES.length],
    ['real',CAT_NAME.real,STYLES.filter(s=>s.cat==='real').length],
    ['2d',CAT_NAME['2d'],STYLES.filter(s=>s.cat==='2d').length],
    ['3d',CAT_NAME['3d'],STYLES.filter(s=>s.cat==='3d').length]];
  $('tabs').innerHTML = defs.map(([k,label,n])=>
    `<button class="tab ${k==='fav'?'fav-tab ':''}${state.tab===k?'active':''}" data-tab="${k}">${label}<span class="count">${n}</span></button>`).join('');
}
function thumbHTML(s,i){
  const [c1,c2]=FAMILY_COLORS[s.family], deg=120+(i%6)*40;
  return `<div class="grad" style="position:absolute;inset:0;background:linear-gradient(${deg}deg,${c1},${c2})"></div>
          <img src="${s._thumbSrc||s.thumb}" alt="${s.name}" width="320" height="180" loading="lazy" decoding="async">`;
}
function renderGrid(){
  const list = currentList();
  const customSel = state.selected?.type==='custom';
  let html = `<div class="card custom ${customSel?'selected':''}" data-custom>
      <div class="thumb"><div class="plus">＋</div><div class="txt">自定义风格</div></div>
      <div class="name">自定义</div></div>`;
  if(list.length===0){
    html += `<div class="empty-tip">${state.q?`没有匹配「${state.q}」的风格，换个关键词试试`:'暂无收藏风格<br>悬停卡片，点右下角的 ★ 即可收藏到这里'}</div>`;
  }
  html += list.map((s,i)=>{
    const sel = state.selected?.type==='preset' && state.selected.style.name===s.name;
    const fav = favorites.has(s.name);
    return `<div class="card ${sel?'selected':''}" data-name="${s.name}">
      <div class="thumb">${thumbHTML(s,i)}<div class="check">✓</div>
        <button class="fav-star" data-fav="${s.name}" aria-label="${fav?'取消收藏':'收藏'}">${fav?'★':'☆'}</button></div>
      <div class="name">${s.name}</div></div>`;
  }).join('');
  $('grid').innerHTML = html;
}
function renderFooter(){
  const sel = state.selected;
  $('customInput').classList.toggle('show', sel?.type==='custom');
  $('footInfo').style.display = sel?.type==='custom'?'none':'';
  if(!sel){ $('footInfo').textContent='未选择风格'; }
  else if(sel.type==='preset'){ $('footInfo').innerHTML=`已选：<b>${sel.style.name}</b> · ${CAT_NAME[sel.style.cat]}`; }
  $('confirmBtn').disabled = !(sel&&(sel.type==='preset'||state.customText.trim().length>0));
}
function renderAll(){ renderTabs(); renderGrid(); renderFooter(); }
function toggleFav(name){
  if(favorites.has(name)) favorites.delete(name); else favorites.add(name);
  saveJSON(LS_FAVORITES,[...favorites]);
}

$('searchInput').addEventListener('input',()=>{
  state.q = $('searchInput').value;
  $('searchClear').classList.toggle('show', state.q.length>0);
  renderGrid();
});
$('searchClear').addEventListener('click',()=>{
  $('searchInput').value=''; state.q='';
  $('searchClear').classList.remove('show');
  renderGrid(); $('searchInput').focus();
});
$('tabs').addEventListener('click',e=>{
  const t=e.target.closest('.tab'); if(!t)return;
  state.tab=t.dataset.tab; renderAll();
});
$('grid').addEventListener('click',e=>{
  const star=e.target.closest('.fav-star');
  if(star){ e.stopPropagation(); toggleFav(star.dataset.fav); renderTabs(); renderGrid(); return; }
  const card=e.target.closest('.card'); if(!card)return;
  if(card.dataset.custom!==undefined){
    state.selected={type:'custom'}; renderGrid(); renderFooter();
    setTimeout(()=>$('customText').focus(),50); return;
  }
  const s=STYLES.find(x=>x.name===card.dataset.name);
  state.selected={type:'preset',style:s}; renderGrid(); renderFooter();
});
$('customText').addEventListener('input',()=>{
  state.customText=$('customText').value;
  if(state.selected?.type==='custom') renderFooter();
});
function closeModal(){ $('overlay').classList.remove('open'); }
function openModal(){ $('overlay').classList.add('open'); }
$('closeBtn').onclick=closeModal;
$('overlay').addEventListener('click',e=>{ if(e.target===$('overlay')) closeModal(); });
document.addEventListener('keydown',e=>{ if(e.key==='Escape'&&$('overlay').classList.contains('open')) closeModal(); });

$('confirmBtn').onclick = ()=>{
  const sel = state.selected; if(!sel)return;
  gates.style = sel;
  saveJSON(LS_SELECTION,{
    type:sel.type,
    name: sel.type==='preset'?sel.style.name:'自定义',
    payload: buildStylePayload(sel),
    savedAt: new Date().toISOString()
  });
  renderStyleCard();
  closeModal();
};

/* ---------- 载荷生成 ---------- */
function buildStylePayload(sel){
  const now = new Date().toISOString();
  if(sel.type==='preset'){
    const s = sel.style;
    return { 视觉风格:{
      来源:'门禁控制面板（风格库预设）',
      风格名:s.name,
      分类:`${CAT_NAME[s.cat]} / ${FAMILY_NAME[s.family]}`,
      缩略图:s.thumb,
      画面风格描述提示词:'由 cine-pipeline style-library.md 五要素转写法按风格名生成',
      确认时间:now }};
  }
  return { 视觉风格:{
    来源:'门禁控制面板（自定义描述）',
    风格名:'自定义',
    画面风格描述提示词:(state.customText||'').trim(),
    确认时间:now }};
}
function toYAML(obj, indent=0){
  const pad='  '.repeat(indent);
  return Object.entries(obj).map(([k,v])=>{
    if(v&&typeof v==='object') return `${pad}${k}:\\n${toYAML(v,indent+1)}`;
    return `${pad}${k}: ${v}`;
  }).join('\\n');
}

$('genBtn').onclick = async ()=>{
  if($('genBtn').disabled) return;
  const ratio = RATIOS.find(x=>x.r===gates.ratio);
  const payload = {
    来源:'门禁控制面板（cine-pipeline Stage 3 输入门禁统一回传）',
    目标模型: gates.model + (gates.modelCap>0?`（单段上限 ${gates.modelCap}s）`:''),
    资产图提示词平台: gates.imagePrompt==='Midjourney'
      ? 'Midjourney（英文短语压缩，参数置尾，交付预算 ≤1200 字符）'
      : 'ChatGPT（自然语言指令式，可分段描述，交付预算 ≤4000 字符）',
    片型: gates.genre,
    画幅: gates.ratio + `（${ratio?ratio.orient:''}）`,
    成片时长: `${gates.dur} 秒（${gates.durMode}）` + (segCount()?`，约 ${segCount()} 个生成段`:''),
    声音策略: gates.sound,
    资产命名规则: gates.naming==='即梦' ? '即梦（资产名＋空格，投喂代码块内一律不加 @）'
                                        : 'ShuoCanvas（@资产名＋空格，代码块内保留 @）',
    ...buildStylePayload(gates.style),
    确认时间: new Date().toISOString()
  };
  saveJSON(LS_GATES, { gates:{...gates, customText:state.customText}, payload, savedAt:new Date().toISOString() });
  $('payload').textContent = '# 项目档案 · 制作门禁（门禁控制面板回传，Stage 3 输入门禁直接引用）\\n' + toYAML(payload);
  $('resultCard').classList.add('show');
  $('resultCard').scrollIntoView({behavior:'smooth', block:'nearest'});
  const cb=$('copyBtn'); cb.textContent='复制'; cb.classList.remove('done');
  if(!handoff){
    $('handoffStatus').textContent = '已保存在浏览器，尚未回传。请由任务打开自动回传版面板，或复制备用档案。';
    return;
  }
  handoffBusy = true; updateCount();
  $('genBtn').textContent = '正在回传…';
  $('handoffStatus').textContent = '正在提交至当前任务…';
  const controller = new AbortController();
  const timer = setTimeout(()=>controller.abort(), 12000);
  try {
    const response = await fetch(handoff.submit, {
      method:'POST', headers:{'Content-Type':'application/json'},
      body:JSON.stringify({gates:{...gates,customText:state.customText},payload,yaml:$('payload').textContent},
        (key,value)=>key==='_thumbSrc'?undefined:value),
      signal:controller.signal
    });
    if(!response.ok) throw new Error('接收通道返回 ' + response.status);
    const receipt = await response.json();
    if(receipt.status !== 'accepted' || receipt.session !== handoff.session) throw new Error('回执不匹配');
    handoffDone = true;
    $('genBtn').textContent = '已回传 ✓';
    $('handoffStatus').textContent = '已回传至当前任务，接下来由助手校验参数并继续。';
    document.querySelectorAll('.gate').forEach(el=>{el.inert=true;});
  } catch(error) {
    $('genBtn').textContent = '重试回传';
    $('handoffStatus').textContent = '回传未确认，参数已保留。请重试；若接收通道已关闭，请回到对话重新连接。';
  } finally {
    clearTimeout(timer); handoffBusy = false; updateCount();
  }
};

$('copyBtn').onclick = async ()=>{
  const text=$('payload').textContent, btn=$('copyBtn');
  try{ await navigator.clipboard.writeText(text); }
  catch(e){
    const ta=document.createElement('textarea'); ta.value=text; document.body.appendChild(ta);
    ta.select(); document.execCommand('copy'); ta.remove();
  }
  btn.textContent='已复制 ✓'; btn.classList.add('done');
  setTimeout(()=>{ btn.textContent='复制'; btn.classList.remove('done'); },1600);
};

/* ---------- 初始化：恢复上次选择 ---------- */
(function restore(){
  const saved = loadJSON(LS_GATES, null) || (handoff && handoff.seed);
  if(saved && saved.gates){
    const g = saved.gates;
    ['model','imagePrompt','genre','ratio','sound','naming'].forEach(key=>{
      if(!g[key]) return;
      gates[key]=g[key];
      document.querySelectorAll(`[data-gate="${key}"] .chip, [data-gate="${key}"] .opt-card`).forEach(b=>{
        if(b.dataset.val===g[key]) b.classList.add('active');
      });
    });
    if(g.model){
      const btn = document.querySelector(`[data-gate="model"] [data-val="${g.model}"]`);
      gates.modelCap = btn ? (+btn.dataset.cap||0) : 12;
    }
    if(g.durMode){
      gates.durMode=g.durMode; gates.dur=g.dur;
      document.querySelectorAll('.dur-chips .chip').forEach(b=>{
        if(b.dataset.mode===g.durMode && (b.dataset.mode!=='自定义时长' || !b.dataset.val)) b.classList.add('active');
      });
    }
    if(g.style){
      if(g.style.type==='preset'){
        const s = STYLES.find(x=>x.name===g.style.style.name);
        if(s){ gates.style={type:'preset',style:s}; state.selected=gates.style; }
      } else {
        gates.style={type:'custom'}; state.selected={type:'custom'};
        state.customText = g.customText||''; $('customText').value = state.customText;
      }
    }
  } else {
    const def = document.querySelector('[data-gate="model"] [data-val="Seedance 2.5"]');
    if(def){ def.classList.add('active'); gates.model='Seedance 2.5'; gates.modelCap=12; }
    gates.durMode='正常语速版'; gates.dur=120;
    document.querySelector('.dur-chips [data-mode="正常语速版"]').classList.add('active');
  }
  renderRatios(); renderDur(); renderStyleCard();
  const done = {model:!!gates.model, imagePrompt:!!gates.imagePrompt, genre:!!gates.genre, ratio:!!gates.ratio,
                style:!!gates.style, duration:!!gates.durMode, sound:!!gates.sound, naming:!!gates.naming};
  gateDone('gate-model',done.model); gateDone('gate-image-prompt',done.imagePrompt);
  gateDone('gate-genre',done.genre);
  gateDone('gate-ratio',done.ratio); gateDone('gate-style',done.style);
  gateDone('gate-duration',done.duration); gateDone('gate-sound',done.sound);
  gateDone('gate-naming',done.naming);
})();

renderAll();
"""

html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta name="renderer-version" content="v7-dark-cinema">
<title>制作门禁 · cine-pipeline</title>
<style>{style_block}{PANEL_CSS}</style>
</head>
<body>
{PANEL_BODY}
{modal_html}
<script>
{data_block}
{THUMB_JS}
{PANEL_JS}
</script>
</body>
</html>
"""

io.open(DST, "w", encoding="utf-8").write(html)
print(f"written: {DST}  {os.path.getsize(DST)/1024/1024:.2f} MB  (thumbs embedded: {len(thumb_b64)})")
