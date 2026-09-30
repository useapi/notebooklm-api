/*
Turn web pages and YouTube videos into a NotebookLM Audio Overview (the "podcast") with the Gemini Notebook API by useapi.net.
For every entry in prompts.json: create a notebook, add the URLs as sources, wait until Google has processed them,
generate an Audio Overview (POST /artifacts, type "audio", async), poll GET /jobs, and download the .m4a.
Docs: https://useapi.net/docs/api-gemini-notebook-v1/post-gemini-notebook-artifacts

Usage: node podcast.mjs <API_TOKEN> [EMAIL] [PROMPTS_FILE]
  API_TOKEN  your useapi.net token, see https://useapi.net/docs/start-here/setup-useapi
  EMAIL      optional, the connected Google account, see https://useapi.net/docs/start-here/setup-gemini-notebook
Requires Node.js 21+ (built-in fetch). No dependencies.
*/
import fs from 'node:fs/promises'

const API = 'https://api.useapi.net/v1/gemini-notebook'
const [token, email, promptsFile = 'prompts.json'] = process.argv.slice(2)
if (!token) { console.error('Usage: node podcast.mjs <API_TOKEN> [EMAIL] [PROMPTS_FILE]'); process.exit(1) }

const headers = { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' }
const sleep = ms => new Promise(r => setTimeout(r, ms))
const call = async (method, path, body) => {
  const res = await fetch(`${API}/${path}`, { method, headers, body: body ? JSON.stringify(body) : undefined })
  const json = await res.json().catch(() => ({}))
  if (!res.ok) throw new Error(`${method} /${path} → HTTP ${res.status}: ${JSON.stringify(json)}`)
  return json
}
const enc = encodeURIComponent

for (const [i, p] of JSON.parse(await fs.readFile(promptsFile, 'utf8')).entries()) {
  console.log(`\n#${i + 1} ${p.title}`)
  const { notebook } = await call('POST', 'notebooks', { title: p.title, ...(email ? { email } : {}) })
  console.log('  notebook', notebook)

  await call('POST', 'sources', { notebook, urls: p.urls })
  // Google fetches and indexes every source before it can be used
  for (;;) {
    const nb = await call('GET', `notebooks/${enc(notebook)}`)
    const statuses = nb.sources.map(s => s.status)
    console.log('  sources:', statuses.join(', '))
    if (statuses.every(s => s === 'ready' || s === 'error')) break
    await sleep(10000)
  }

  const audio = { notebook, type: 'audio', mode: 'async', format: p.format, length: p.length, language: p.language }
  Object.keys(audio).forEach(k => audio[k] === undefined && delete audio[k])
  const { jobid } = await call('POST', 'artifacts', audio)
  console.log('  audio job', jobid)

  let job
  for (;;) {
    job = await call('GET', `jobs/${enc(jobid)}`)
    if (job.status === 'completed' || job.status === 'failed') break
    console.log('  status:', job.status)
    await sleep(15000)
  }
  if (job.status === 'failed') { console.error('  failed:', job.error); continue }

  for (const f of job.result.files ?? []) {
    const res = await fetch(f.url, { headers: { Authorization: `Bearer ${token}` } })
    const name = `${p.title.replace(/[^\w-]+/g, '_').slice(0, 60)}.${f.format}`
    await fs.writeFile(name, Buffer.from(await res.arrayBuffer()))
    console.log(`  saved ${name} (${job.result.duration ?? '?'} s): "${job.result.title}"`)
  }
}
