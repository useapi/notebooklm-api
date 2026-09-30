/*
Run NotebookLM Deep Research with the Gemini Notebook API by useapi.net and save the report as Markdown.
For every entry in prompts.json: create a notebook, start a Deep Research run (POST /research, type "deep", async),
poll GET /jobs, then save the report (.md) and the sources Google read, marking which ones the report cites (.json).
A research run does not change the notebook; import what you want to keep with POST /research/import.
Docs: https://useapi.net/docs/api-gemini-notebook-v1/post-gemini-notebook-research

Usage: node research.mjs <API_TOKEN> [EMAIL] [PROMPTS_FILE]
Requires Node.js 21+ (built-in fetch). No dependencies.
*/
import fs from 'node:fs/promises'

const API = 'https://api.useapi.net/v1/gemini-notebook'
const [token, email, promptsFile = 'prompts.json'] = process.argv.slice(2)
if (!token) { console.error('Usage: node research.mjs <API_TOKEN> [EMAIL] [PROMPTS_FILE]'); process.exit(1) }

const headers = { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' }
const sleep = ms => new Promise(r => setTimeout(r, ms))
const call = async (method, path, body) => {
  const res = await fetch(`${API}/${path}`, { method, headers, body: body ? JSON.stringify(body) : undefined })
  const json = await res.json().catch(() => ({}))
  if (!res.ok) throw new Error(`${method} /${path} → HTTP ${res.status}: ${JSON.stringify(json)}`)
  return json
}

for (const [i, p] of JSON.parse(await fs.readFile(promptsFile, 'utf8')).entries()) {
  console.log(`\n#${i + 1} ${p.query}`)
  const { notebook } = await call('POST', 'notebooks', { title: p.title ?? p.query.slice(0, 100), ...(email ? { email } : {}) })
  const { jobid } = await call('POST', 'research', { notebook, query: p.query, type: 'deep', mode: 'async' })
  console.log('  research job', jobid)

  let job
  for (;;) {
    job = await call('GET', `jobs/${encodeURIComponent(jobid)}`)
    if (job.status === 'completed' || job.status === 'failed') break
    console.log('  status:', job.status)
    await sleep(20000)
  }
  if (job.status === 'failed') { console.error('  failed:', job.error); continue }

  const base = (p.title ?? p.query).replace(/[^\w-]+/g, '_').slice(0, 60)
  const { report, sources = [] } = job.result
  await fs.writeFile(`${base}.md`, report?.markdown ?? '')
  await fs.writeFile(`${base}.sources.json`, JSON.stringify(sources, null, 2))
  console.log(`  saved ${base}.md: "${report?.title}" (${sources.length} sources, ${sources.filter(s => s.cited).length} cited)`)
}
