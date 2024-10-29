from collections import Counter
import os
import requests

data_path = 'legacy_data/'
os.makedirs(data_path, exist_ok=True)
existing_files = [i for i in os.listdir(data_path)]

urls = [
    'https://github.com/BYVoid/ytenx/raw/80a6e2a/ytenx/sync/kyonh/CjengMuxNgixQim.txt',
    'https://github.com/BYVoid/ytenx/raw/80a6e2a/ytenx/sync/kyonh/YonhMuxNgixQim.txt',
    'https://github.com/BYVoid/ytenx/raw/3666370/ytenx/sync/kyonh/SieuxYonh.txt',
]

authors = {
    'karlgren': '高本漢',
    'yanglik': '王力',
    'lixyeng': '李榮',
    'zjeuhyengphyon': '邵榮芬',
    'drienghtriangzjangpyang': '鄭張尚芳',
    'phuanngohyon': '潘悟雲',
    'pulleyblank': '蒲立本',
}

# Download files
for url in urls:
    filename = url.split('/')[-1]
    if filename in existing_files:
        print(f'{filename}: already exists')
        continue
    r = requests.get(url)  # may add proxies={'https': '...'}
    if r.status_code != 200:
        print(f'{filename}: failed to download')
        continue
    with open(f'{data_path}{filename}', 'w', encoding='utf-8') as f:
        f.write(r.text)
    print(f'{filename}: downloaded')


initials = {}
finals = {}
for dct, filename in [
    (initials, 'CjengMuxNgixQim.txt'),
    (finals, 'YonhMuxNgixQim.txt'),
]:
    with open(f'{data_path}{filename}', encoding='utf-8') as f:
        header = f.readline().strip().split(' ')
        for line in f:
            line = line.strip().split(' ')
            dct[line[0]] = dict(zip(header[1:], line[1:]))

lines = []
chars = Counter()
with open(f'{data_path}SieuxYonh.txt', encoding='utf-8') as f:
    for line in f:
        line = line.strip().split(' ')
        rime_num = line[0]
        initial = line[2]
        final = line[3]
        new_line = [rime_num]
        for author in authors:
            syllable = initials[initial][author] + finals[final][author]
            if author == 'karlgren':
                if 'ăt' in syllable:
                    syllable = syllable.replace('ăt', 'at')
                elif 'at' in syllable:
                    syllable = syllable.replace('at', 'ăt')
            elif author == 'yanglik':
                syllable = syllable.replace('ǐ', 'i\u0306')
                syllable = syllable.replace('ĕ', 'e\u0306')
                if final[0] in ('眞', '質'):
                    syllable = syllable.replace('u', 'w')
                else:
                    syllable = syllable.replace('uɛt', 'wɛt')
            elif author == 'phuanngohyon':
                syllable = syllable.replace('ʃ', 'ʂ')
                syllable = syllable.replace('iei', 'iɛi')
                syllable = syllable.replace('iet', 'iɛt')
                if final[0] == '戈':
                    syllable = syllable.replace('uɑ', 'ʷɑ')
            new_line.append(syllable)
            for char in syllable:
                chars[char] += 1
        lines.append(new_line)
print(chars)

with open('all_rimes_legacy.tsv', 'w', encoding='utf-8') as f:
    f.write('小韻號')
    for author in authors.values():
        f.write(f'\t{author}')
    f.write('\n')
    for line in lines:
        f.write('\t'.join(line) + '\n')
