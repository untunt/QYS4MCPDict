all_rimes = {}
all_rimes_legacy = {}
all_chars = []

for dct, filename in [
    (all_rimes, 'all_rimes.tsv'),
    (all_rimes_legacy, 'all_rimes_legacy.tsv'),
    (all_chars, 'all_chars.tsv'),
]:
    with open(filename, encoding='utf-8') as f:
        header = f.readline().strip().split('\t')
        if filename != 'all_chars.tsv':
            header = header[1:]
        for line in f:
            line = line.strip().split('\t')
            rime_num = line[0]
            if filename != 'all_chars.tsv':
                line = line[1:]
            line = dict(zip(header, line))
            if filename == 'all_chars.tsv':
                dct.append(line)
            else:
                dct[rime_num] = line

# Split legacy rimes
for rime_num in all_rimes:
    if rime_num.isdigit():
        continue
    all_rimes_legacy[rime_num] = all_rimes_legacy[rime_num[:-1]]

# Compare
for (author, author_legacy) in [
    ('高本漢', '高本漢'),
    ('王力1957', '王力'),
    ('潘悟雲2000', '潘悟雲'),
]:
    diff = []
    for rime_num in all_rimes:
        ipa = all_rimes[rime_num][author]
        ipa_legacy = all_rimes_legacy[rime_num][author_legacy]
        if author_legacy == '高本漢':
            if ipa[0] != 'j':
                ipa = ipa.replace('ji', 'i').replace('jwi', 'wi')
                ipa = ipa.replace('je̯i', 'e̯i').replace('jwe̯i', 'we̯i')
        elif author_legacy == '王力':
            ipa = ipa.replace('ʱ', '').replace('nʑ', 'ȵʑ')
        elif author_legacy == '潘悟雲':
            ipa = ipa.replace('iʊ', 'io')
        ipa_legacy = ipa_legacy.replace('g', 'ɡ')
        if ipa_legacy == ipa:
            continue
        diff.append((rime_num, all_rimes[rime_num]['切韻音系描述'], ipa_legacy, ipa))
    with open(f'diff_{author_legacy}.tsv', 'w', encoding='utf-8') as f:
        for line in diff:
            f.write('\t'.join(line) + '\n')

# Join 3 tables
header = list(all_rimes['1'].keys())
i = header.index('潘悟雲2000')
header = header[:i] + ['李榮', '邵榮芬', '蒲立本', '鄭張尚芳'] + header[i:]
header = ['小韻號', '字頭'] + header + ['釋義']
result = [header]
for line in all_chars:
    rime_num = line['小韻號']
    new_line = []
    for k in header:
        if k in line:
            new_line.append(line[k])
        elif k in all_rimes[rime_num]:
            new_line.append(all_rimes[rime_num][k])
        else:
            new_line.append(all_rimes_legacy[rime_num][k])
    result.append(new_line)
with open('廣韻.tsv', 'w', encoding='utf-8') as f:
    for line in result:
        f.write('\t'.join(line) + '\n')
