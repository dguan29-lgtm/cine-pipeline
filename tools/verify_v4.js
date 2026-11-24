const { chromium } = require('playwright-core');

(async () => {
  const browser = await chromium.launch({ headless: true, executablePath: 'C:/Users/Administrator/AppData/Local/ms-playwright/chromium_headless_shell-1243/chrome-headless-shell-win64/chrome-headless-shell.exe' });
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  const errors = [];
  page.on('pageerror', e => errors.push('PAGEERROR: ' + e.message));
  page.on('console', m => { if (m.type() === 'error') errors.push('CONSOLE: ' + m.text()); });

  await page.goto('file:///C:/Users/Administrator/.skills/cine-pipeline/tools/%E9%97%A8%E7%A6%81%E6%8E%A7%E5%88%B6%E9%9D%A2%E6%9D%BF.html');
  await page.evaluate(() => localStorage.clear());
  await page.reload();
  await page.waitForTimeout(600);

  // A. 首屏截图
  await page.screenshot({ path: 'C:/Users/Administrator/.skills/cine-pipeline/tools/_v4_initial.png', fullPage: true });

  // B. 弹窗打开 + 网格缩略图检查
  await page.click('#openStyleBtn');
  await page.waitForTimeout(500);
  const modalThumb = await page.evaluate(() => {
    const imgs = [...document.querySelectorAll('#grid .card .thumb img')];
    const loaded = imgs.filter(i => i.complete && i.naturalWidth > 0);
    const first = imgs[0];
    const r = first ? first.getBoundingClientRect() : null;
    return { total: imgs.length, loaded: loaded.length, firstRect: r ? { w: Math.round(r.width), h: Math.round(r.height) } : null };
  });
  console.log('modal grid thumbs:', JSON.stringify(modalThumb));
  await page.screenshot({ path: 'C:/Users/Administrator/.skills/cine-pipeline/tools/_v4_modal.png' });

  // C. 选风格并确认 → 面板卡片缩略图检查（computed 尺寸 + 加载状态）
  await page.click('.card[data-name="电影感"]');
  await page.click('#confirmBtn');
  await page.waitForTimeout(400);
  const cardThumb = await page.evaluate(() => {
    const box = document.querySelector('#styleCurrent .sthumb');
    const img = document.querySelector('#styleCurrent .sthumb img');
    if (!box || !img) return { present: false };
    const rb = box.getBoundingClientRect(), ri = img.getBoundingClientRect();
    const cs = getComputedStyle(box);
    return { present: true,
      boxRect: { w: Math.round(rb.width), h: Math.round(rb.height) },
      imgRect: { w: Math.round(ri.width), h: Math.round(ri.height) },
      natural: img.naturalWidth, complete: img.complete,
      display: cs.display, overflow: cs.overflow, opacity: getComputedStyle(img).opacity,
      srcHead: img.src.slice(0, 30) };
  });
  console.log('panel style thumb:', JSON.stringify(cardThumb));
  await page.screenshot({ path: 'C:/Users/Administrator/.skills/cine-pipeline/tools/_v4_stylecard.png' });

  // D. 其余门禁走完 + 生成档案 + 全页截图
  await page.click('[data-gate="imagePrompt"] [data-val="Midjourney"]');
  await page.click('[data-gate="genre"] [data-val="短剧"]');
  await page.click('.ratio-card[data-r="16:9"]');
  await page.click('[data-gate="sound"] [data-val="模型原生对白"]');
  await page.click('[data-gate="naming"] [data-val="即梦"]');
  await page.click('#genBtn');
  await page.waitForTimeout(400);
  console.log('gateCount =', (await page.textContent('#gateCount')).trim());
  await page.screenshot({ path: 'C:/Users/Administrator/.skills/cine-pipeline/tools/_v4_full.png', fullPage: true });

  // E. 对比度抽查（正文/次级文字 vs 白卡）
  const contrast = await page.evaluate(() => {
    function lum(c){ const [r,g,b]=c.match(/\d+/g).map(Number).map(v=>{v/=255;return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4)});return .2126*r+.7152*g+.0722*b }
    function ratio(fg,bg){ const a=lum(fg),b=lum(bg); return ((Math.max(a,b)+.05)/(Math.min(a,b)+.05)).toFixed(2) }
    const g = (sel, prop) => { const el = document.querySelector(sel); return el ? getComputedStyle(el)[prop] : null };
    return {
      body_text_on_bg: ratio(g('body','color'), 'rgb(245,245,247)'),
      text2_on_white: ratio(g('.gate .hint','color'), 'rgb(255,255,255)'),
      title_on_white: ratio(g('.gate-head h3','color'), 'rgb(255,255,255)'),
      chip_active: '#1d1d1f bg / #ffffff text = ' + ratio('rgb(255,255,255)','rgb(29,29,31)'),
    };
  });
  console.log('contrast:', JSON.stringify(contrast, null, 1));

  // F. 刷新恢复
  await page.reload();
  await page.waitForTimeout(500);
  console.log('after reload gateCount =', (await page.textContent('#gateCount')).trim());
  const reloadedThumb = await page.evaluate(() => {
    const img = document.querySelector('#styleCurrent .sthumb img');
    return img ? { complete: img.complete, natural: img.naturalWidth } : null;
  });
  console.log('reload style thumb:', JSON.stringify(reloadedThumb));

  console.log('ERRORS:', errors.length ? errors : 'NONE');
  await browser.close();
})().catch(e => { console.error('FATAL', e); process.exit(1); });
