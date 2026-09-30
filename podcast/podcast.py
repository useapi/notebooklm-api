"""
Turn web pages and YouTube videos into a NotebookLM Audio Overview (the "podcast") with the Gemini Notebook API by useapi.net.
For every entry in prompts.json: create a notebook, add the URLs as sources, wait until Google has processed them,
generate an Audio Overview (POST /artifacts, type "audio", async), poll GET /jobs, and download the .m4a.
Docs: https://useapi.net/docs/api-gemini-notebook-v1/post-gemini-notebook-artifacts

Usage: python3 podcast.py <API_TOKEN> [EMAIL] [PROMPTS_FILE]
Requires Python 3.8+. No dependencies.
"""
import json, re, sys, time, urllib.error, urllib.parse, urllib.request

API = 'https://api.useapi.net/v1/gemini-notebook'
if len(sys.argv) < 2:
    sys.exit('Usage: python3 podcast.py <API_TOKEN> [EMAIL] [PROMPTS_FILE]')
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


enc = lambda s: urllib.parse.quote(s, safe='')

for i, p in enumerate(json.load(open(prompts_file, encoding='utf-8'))):
    print(f"\n#{i + 1} {p['title']}")
    body = {'title': p['title']}
    if email:
        body['email'] = email
    notebook = call('POST', 'notebooks', body)['notebook']
    print('  notebook', notebook)

    call('POST', 'sources', {'notebook': notebook, 'urls': p['urls']})
    # Google fetches and indexes every source before it can be used
    while True:
        statuses = [s['status'] for s in call('GET', f'notebooks/{enc(notebook)}')['sources']]
        print('  sources:', ', '.join(statuses))
        if all(s in ('ready', 'error') for s in statuses):
            break
        time.sleep(10)

    audio = {'notebook': notebook, 'type': 'audio', 'mode': 'async'}
    for k in ('format', 'length', 'language'):
        if p.get(k):
            audio[k] = p[k]
    jobid = call('POST', 'artifacts', audio)['jobid']
    print('  audio job', jobid)

    while True:
        job = call('GET', f'jobs/{enc(jobid)}')
        if job['status'] in ('completed', 'failed'):
            break
        print('  status:', job['status'])
        time.sleep(15)
    if job['status'] == 'failed':
        print('  failed:', job.get('error'))
        continue

    result = job['result']
    for f in result.get('files', []):
        req = urllib.request.Request(f['url'], headers={'Authorization': f'Bearer {token}', 'User-Agent': UA})
        name = re.sub(r'[^\w-]+', '_', p['title'])[:60] + '.' + f['format']
        with urllib.request.urlopen(req, timeout=300) as r, open(name, 'wb') as out:
            out.write(r.read())
        print(f"  saved {name} ({result.get('duration', '?')} s): \"{result.get('title')}\"")
