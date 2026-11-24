const { chromium } = require('playwright-core');

(async () => {
  const browser = await chromium.launch({ headless: true, executablePath: 'C:/Users/Administrator/AppData/Local/ms-playwright/chromium_headless_shell-1243/chrome-headless-shell-win64/chrome-headless-shell.exe' });
  const page = await browser.newPage();
  const errors = [];
  page.on('pageerror', e => errors.push('PAGEERROR: ' + e.message));
  page.on('console', m => { if (m.type() === 'error') errors.push('CONSOLE: ' + m.text()); });

  await page.goto('file:///C:/Users/Administrator/.skills/cine-pipeline/tools/%E9%97%A8%E7%A6%81%E6%8E%A7%E5%88%B6%E9%9D%A2%E6%9D%BF.html');
  await page.waitForTimeout(500);

  // 1. 初始状态：模型预选 SD2.5 + 时长默认，已完成 2/8
  let cnt = await page.textContent('#gateCount');
  console.log('initial gateCount =', cnt.trim());

  // 2. 选资产图提示词平台
  await page.click('[data-gate="imagePrompt"] [data-val="ChatGPT"]');
  // 3. 选片型
  await page.click('[data-gate="genre"] [data-val="短剧"]');
  // 4. 选画幅 16:9
  await page.click('.ratio-card[data-r="16:9"]');
  // 5. 拖时长滑块到 180s（自定义）
  await page.fill('#durSlider', '180');
  await page.dispatchEvent('#durSlider', 'input');
  // 6. 选声音策略
  await page.click('[data-gate="sound"] [data-val="模型原生对白"]');
  // 7. 选命名规则
  await page.click('[data-gate="naming"] [data-val="即梦"]');

  cnt = await page.textContent('#gateCount');
  console.log('after chips gateCount =', cnt.trim());
  console.log('durVal =', await page.textContent('#durVal'));

  // 8. 打开画风弹窗，选一个预设风格并确认
  await page.click('#openStyleBtn');
  await page.waitForTimeout(300);
  await page.click('.card[data-name="电影感"]');
  await page.click('#confirmBtn');
  await page.waitForTimeout(300);
  console.log('style card shows:', (await page.textContent('#styleCurrent')).replace(/\s+/g, ' ').slice(0, 60));

  cnt = await page.textContent('#gateCount');
  console.log('final gateCount =', cnt.trim());
  console.log('genBtn disabled =', await page.isDisabled('#genBtn'));

  // 9. 生成项目档案
  await page.click('#genBtn');
  await page.waitForTimeout(300);
  const payload = await page.textContent('#payload');
  console.log('--- payload head ---');
  console.log(payload.split('\n').slice(0, 12).join('\n'));

  // 10. localStorage 持久化
  const saved = await page.evaluate(() => JSON.parse(localStorage.getItem('pipelineGates')));
  console.log('saved gates: model=%s imagePrompt=%s genre=%s ratio=%s dur=%s sound=%s naming=%s',
    saved.gates.model, saved.gates.imagePrompt, saved.gates.genre, saved.gates.ratio, saved.gates.dur, saved.gates.sound, saved.gates.naming);

  // 11. 截图
  await page.screenshot({ path: 'C:/Users/Administrator/.skills/cine-pipeline/tools/_panel_smoke.png', fullPage: false });

  // 12. 刷新恢复
  await page.reload();
  await page.waitForTimeout(500);
  console.log('after reload gateCount =', (await page.textContent('#gateCount')).trim());

  console.log('ERRORS:', errors.length ? errors : 'NONE');
  await browser.close();
})().catch(e => { console.error('FATAL', e); process.exit(1); });
// v2 追加断言已在上方主体内
