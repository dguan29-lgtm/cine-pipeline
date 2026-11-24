import http from 'node:http';
import { readFile, mkdir, writeFile } from 'node:fs/promises';
import { resolve } from 'node:path';
import { randomBytes } from 'node:crypto';

// One loopback-only receiver per active task. No access to Codex credentials or APIs.
const args = process.argv.slice(2);
const option = (name, fallback) => {
  const i = args.indexOf(name);
  return i < 0 ? fallback : args[i + 1];
};
const outArg = option('--out');
const thread = option('--thread');
if (!outArg || !thread) throw new Error('Usage: node gate-session.mjs --thread TASK_ID --out SESSION_DIRECTORY [--seed JSON_FILE] [--timeout 1200]');
const out = resolve(outArg);
const token = randomBytes(24).toString('hex');
const session = randomBytes(12).toString('hex');
const prefix = '/' + token;
const seedPath = option('--seed');
const seed = seedPath ? JSON.parse(await readFile(resolve(seedPath), 'utf8')) : null;
const timeout = Number(option('--timeout', '1200'));
if (!Number.isFinite(timeout) || timeout < 10 || timeout > 3600) throw new Error('timeout must be 10..3600 seconds');
const panel = await readFile(new URL('../tools/门禁控制面板.html', import.meta.url), 'utf8');
await mkdir(out, { recursive: true });
let accepted = null, saving = null, origin, expiry;
const resultPath = resolve(out, 'submission-' + session + '.json');
const emit = (value) => process.stdout.write(JSON.stringify(value) + '\n');
const json = (res, status, value) => {
  res.writeHead(status, {'Content-Type':'application/json; charset=utf-8', 'Cache-Control':'no-store'});
  res.end(JSON.stringify(value));
};
const server = http.createServer(async (req, res) => {
  try {
    if (req.headers.host !== new URL(origin).host) return json(res, 403, {error:'host'});
    if (req.method === 'GET' && req.url === prefix + '/') {
      const bootstrap = JSON.stringify({session, submit:prefix+'/submit', seed}).replace(/</g, '\\u003c');
      const html = panel.replace('<script>', '<script>window.__PIPELINE_HANDOFF__=' + bootstrap + ';</script>\n<script>');
      res.writeHead(200, {'Content-Type':'text/html; charset=utf-8', 'Cache-Control':'no-store', 'X-Frame-Options':'DENY', 'Referrer-Policy':'no-referrer'});
      return res.end(html);
    }
    if (req.method !== 'POST' || req.url !== prefix + '/submit') return json(res, 404, {error:'not found'});
    if (req.headers.origin !== origin || !String(req.headers['content-type']).startsWith('application/json')) return json(res, 403, {error:'origin or content type'});
    if (Number(req.headers['content-length']) > 65536) return json(res, 413, {error:'too large'});
    let raw = '';
    for await (const chunk of req) {
      raw += chunk;
      if (Buffer.byteLength(raw) > 65536) return json(res, 413, {error:'too large'});
    }
    let data;
    try { data = JSON.parse(raw); } catch { return json(res, 400, {error:'invalid JSON'}); }
    const g = data?.gates;
    if (!g || !['model','imagePrompt','genre','ratio','durMode','sound','naming'].every(k=>typeof g[k]==='string' && g[k].length>0)
      || !Number.isFinite(g.dur) || g.dur < 1 || g.dur > 3600
      || !['16:9','9:16','3:4','21:9','4:3','1:1'].includes(g.ratio)
      || !['ChatGPT','Midjourney'].includes(g.imagePrompt)
      || !['即梦','ShuoCanvas'].includes(g.naming)
      || !(g.style?.type === 'preset' ? typeof g.style.style?.name==='string' : g.style?.type === 'custom' && !!g.customText?.trim())
      || !data.payload || typeof data.payload !== 'object' || typeof data.yaml !== 'string') return json(res, 422, {error:'incomplete gates'});
    // First completed write wins. An identical retry receives the existing receipt.
    if (accepted) {
      if (JSON.stringify(accepted.gates) !== JSON.stringify(g)) return json(res, 409, {error:'session already submitted'});
      await saving;
      return json(res, 200, {status:'accepted', session});
    }
    accepted = {session, thread, receivedAt:new Date().toISOString(), gates:g, payload:data.payload, yaml:data.yaml};
    try {
      saving = writeFile(resultPath, JSON.stringify(accepted, null, 2), {encoding:'utf8', flag:'wx'});
      await saving;
    } catch(error) { accepted = null; throw error; }
    emit({event:'GATES_SUBMITTED', resultPath, submission:accepted});
    json(res, 200, {status:'accepted', session});
    clearTimeout(expiry);
    expiry = setTimeout(()=>server.close(), 15000);
  } catch(error) { json(res, 500, {error:'could not save submission'}); }
});
server.requestTimeout = 15000;
server.listen(0, '127.0.0.1', async ()=>{
  origin = 'http://127.0.0.1:' + server.address().port;
  const info = {event:'GATES_READY', session, thread, url:origin+prefix+'/', resultPath, timeoutSeconds:timeout};
  await writeFile(resolve(out, 'session-' + session + '.json'), JSON.stringify(info, null, 2));
  emit(info);
  expiry = setTimeout(()=>{emit({event:'GATES_EXPIRED', session}); server.close();}, timeout*1000);
});
