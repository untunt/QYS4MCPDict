import os
import requests

schemas_path = 'deriver_schemas/'
os.makedirs(schemas_path, exist_ok=True)
existing_schemas = [i.replace('.js', '') for i in os.listdir(schemas_path)]

schema_urls = {}
for url_prefix, schemas in [(
    'https://github.com/nk2028/tshet-uinh-examples/raw/c0d2c4d/',
    ['tupa', 'baxter', 'karlgren', 'wangli', 'panwuyun', 'unt', 'msoeg_v8'],
), (
    'https://github.com/nk2028/obsolete-romanizations-examples/raw/32a2d47/',
    ['zihui', 'polyhedron', 'blankego'],
)]:
    for schema in schemas:
        schema_urls[schema] = f'{url_prefix}{schema}.js'

# Download schemas
for schema, url in schema_urls.items():
    if schema in existing_schemas:
        print(f'{schema}: already exists')
        continue
    r = requests.get(url)  # may add proxies={'https': '...'}
    if r.status_code != 200:
        print(f'{schema}: failed to download')
        continue
    with open(f'{schemas_path}{schema}.js', 'w', encoding='utf-8') as f:
        f.write(r.text)
    print(f'{schema}: downloaded')

# Join schemas
js_code = 'const schemas = {\n'
for schema in schema_urls:
    if not os.path.exists(f'{schemas_path}/{schema}.js'):
        continue
    js_code += schema + '(音韻地位, 字頭, 選項) {\n'
    with open(f'{schemas_path}{schema}.js', encoding='utf-8') as f:
        js_code += f.read()
    js_code += '},\n'
js_code += '}\n'

with open('deriver_schemas.js', 'w', encoding='utf-8') as f:
    f.write(js_code)
print('schemas.js created')
