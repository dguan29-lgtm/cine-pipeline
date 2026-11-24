import test from 'node:test';
import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { mkdtemp, readFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createInterface } from 'node:readline';
import { runInNewContext, Script } from 'node:vm';

test('actual panel click handler reports success, failure, and standalone mode correctly', async()=>{
  const html = await readFile(new URL('../tools/门禁控制面板.html', import.meta.url),'utf8');
  const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];
  new Script(script); // Parse the complete original panel, including its embedded catalogue.
  const handler = script.slice(script.indexOf("$('genBtn').onclick ="),script.indexOf("$('copyBtn').onclick ="));
  for(const mode of ['success','failure','standalone']) {
    const elements = new Map();
    const element = id=>{
      if(!elements.has(id)) elements.set(id,{textContent:'',disabled:false,classList:{add(){},remove(){}},scrollIntoView(){}});
      return elements.get(id);
    };
    let fetchCount = 0, sent;
    const context = {
      $:element, RATIOS:[{r:'16:9',orient:'横屏'}],
      gates:{model:'Seedance 2.5',modelCap:12,imagePrompt:'ChatGPT',genre:'短片',ratio:'16:9',dur:80,durMode:'自定义时长',sound:'模型原生对白',naming:'即梦',style:{type:'preset'}},
      state:{customText:''}, segCount:()=>7, buildStylePayload:()=>({视觉风格:{风格名:'国产悬疑'}}),
      saveJSON(){}, LS_GATES:'test', toYAML:JSON.stringify,
      handoff:mode==='standalone'?null:{session:'test-session',submit:'/submit'},
      handoffBusy:false,handoffDone:false,
      updateCount(){element('genBtn').disabled=context.handoffBusy||context.handoffDone;},
      document:{querySelectorAll:()=>[]},AbortController,setTimeout,clearTimeout,
      fetch:async(_url,options)=>{fetchCount++;sent=JSON.parse(options.body);if(mode==='failure')throw new Error('offline');return{ok:true,json:async()=>({status:'accepted',session:'test-session'})};}
    };
    runInNewContext(handler,context);
    await element('genBtn').onclick();
    if(mode==='success') {
      assert.equal(sent.gates.dur,80);
      assert.equal(context.handoffDone,true);
      assert.match(element('handoffStatus').textContent,/已回传至当前任务/);
      await element('genBtn').onclick();
      assert.equal(fetchCount,1);
    } else if(mode==='failure') {
      assert.equal(context.handoffDone,false);
      assert.equal(element('genBtn').disabled,false);
      assert.equal(element('genBtn').textContent,'重试回传');
      assert.match(element('handoffStatus').textContent,/回传未确认/);
    } else {
      assert.equal(fetchCount,0);
      assert.match(element('handoffStatus').textContent,/尚未回传/);
    }
  }
});

test('panel submission returns the confirmed gates to exactly one task', async t=>{
  const dir = await mkdtemp(join(tmpdir(), 'cine-gates-test-'));
  const child = spawn(process.execPath, [fileURLToPath(new URL('./gate-session.mjs', import.meta.url)), '--out', dir, '--thread', 'test-thread', '--timeout', '30'], {stdio:['ignore','pipe','pipe']});
  t.after(()=>child.kill());
  const events = [];
  const ready = await new Promise((resolve,reject)=>{
    child.on('error',reject);
    child.on('exit',code=>{if(!events.length) reject(new Error('early exit '+code));});
    createInterface({input:child.stdout}).on('line',line=>{const e=JSON.parse(line); events.push(e); if(e.event==='GATES_READY') resolve(e);});
  });
  const origin = new URL(ready.url).origin;
  const html = await (await fetch(ready.url)).text();
  assert.match(html,/window\.__PIPELINE_HANDOFF__=/);
  assert.match(html,/生成项目档案并继续/);
  assert.match(html,/已回传至当前任务/);
  assert.equal((await fetch(origin+'/')).status,404);
  const data = {gates:{model:'Seedance 2.5',modelCap:12,imagePrompt:'ChatGPT',genre:'短片',ratio:'16:9',durMode:'自定义时长',dur:80,sound:'模型原生对白',naming:'即梦',style:{type:'preset',style:{name:'国产悬疑'}}},payload:{片型:'短片',资产图提示词平台:'ChatGPT'},yaml:'片型: 短片'};
  const post = (body, requestOrigin=origin)=>fetch(ready.url+'submit',{method:'POST',headers:{'Content-Type':'application/json',Origin:requestOrigin},body:JSON.stringify(body)});
  assert.equal((await post(data,'http://outside.invalid')).status,403);
  assert.equal((await post({gates:{}})).status,422);
  assert.equal((await post({...data,gates:{...data.gates,imagePrompt:'unknown'}})).status,422);
  const responses = await Promise.all([post(data),post(data)]);
  for(const r of responses){assert.equal(r.status,200);assert.deepEqual(await r.json(),{status:'accepted',session:ready.session});}
  const saved = JSON.parse(await readFile(ready.resultPath,'utf8'));
  assert.equal(saved.thread,'test-thread');
  assert.deepEqual(saved.gates,data.gates);
  assert.equal((await post({...data,gates:{...data.gates,dur:120}})).status,409);
  // Allow stdout delivery, then verify a retry did not trigger a second continuation.
  await new Promise(resolve=>setTimeout(resolve,30));
  assert.equal(events.filter(e=>e.event==='GATES_SUBMITTED').length,1);
});
