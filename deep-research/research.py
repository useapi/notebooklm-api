"""
Run NotebookLM Deep Research with the Gemini Notebook API by useapi.net and save the report as Markdown.
For every entry in prompts.json: create a notebook, start a Deep Research run (POST /research, type "deep", async),
poll GET /jobs, then save the report (.md) and the sources Google read, marking which ones the report cites (.json).
Docs: https://useapi.net/docs/api-gemini-notebook-v1/post-gemini-notebook-research

Usage: python3 research.py <API_TOKEN> [EMAIL] [PROMPTS_FILE]
Requires Python 3.8+. No dependencies.
"""
import json, re, sys, time, urllib.error, urllib.parse, urllib.request

API = 'https://api.useapi.net/v1/gemini-notebook'
if len(sys.argv) < 2:
    sys.exit('Usage: python3 research.py <API_TOKEN> [EMAIL] [PROMPTS_FILE]')
token = sys.argv[1]
email = sys.argv[2] if len(sys.argv) > 2 else None
prompts_file = sys.argv[3] if len(sys.argv) > 3 else 'prompts.json'
# api.useapi.net's Cloudflare edge rejects urllib's default User-Agent (error 1010, HTTP 403), so send a named one
UA = 'useapi-gemini-notebook-example/1.0'
HEADERS = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json', 'User-Agent': UA}


def call(method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(f'{API}/{path}', data=data, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req, timeout=320) as r:
            return json.loads(r.read() or b'{}')
    except urllib.error.HTTPError as e:
        raise RuntimeError(f'{method} /{path} -> HTTP {e.code}: {e.read().decode()}')


for i, p in enumerate(json.load(open(prompts_file, encoding='utf-8'))):
    print(f"\n#{i + 1} {p['query']}")
    body = {'title': p.get('title') or p['query'][:100]}
    if email:
        body['email'] = email
    notebook = call('POST', 'notebooks', body)['notebook']
    jobid = call('POST', 'research', {'notebook': notebook, 'query': p['query'], 'type': 'deep', 'mode': 'async'})['jobid']
    print('  research job', jobid)

    while True:
        job = call('GET', 'jobs/' + urllib.parse.quote(jobid, safe=''))
        if job['status'] in ('completed', 'failed'):
            break
        print('  status:', job['status'])
        time.sleep(20)
    if job['status'] == 'failed':
        print('  failed:', job.get('error'))
        continue

    base = re.sub(r'[^\w-]+', '_', p.get('title') or p['query'])[:60]
    report = job['result'].get('report') or {}
    sources = job['result'].get('sources') or []
    open(f'{base}.md', 'w', encoding='utf-8').write(report.get('markdown', ''))
    json.dump(sources, open(f'{base}.sources.json', 'w', encoding='utf-8'), indent=2)
    print(f"  saved {base}.md: \"{report.get('title')}\" ({len(sources)} sources, {sum(1 for s in sources if s.get('cited'))} cited)")
