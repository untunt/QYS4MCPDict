const recon2schema = {
  '切韻拼音': schemas.tupa,
  '白一平拼音': schemas.baxter,
  '古韻羅馬字': schemas.polyhedron,
  '有女羅馬字': schemas.blankego,
  '高本漢': schemas.karlgren,
  '王力1957': schemas.wangli,
  '王力1985': schemas.wangli,
  '潘悟雲2000': schemas.panwuyun,
  '潘悟雲2013': schemas.panwuyun,
  '潘悟雲2023': schemas.panwuyun,
  'unt2020': schemas.unt,
  'unt2022': schemas.unt,
  'unt通俗擬音': schemas.unt,
  'msoeg': schemas.msoeg_v8,
};

const recon2params = {
  '切韻拼音': {},
  '白一平拼音': {},
  '古韻羅馬字': {},
  '有女羅馬字': {},
  '高本漢': { 音標體系: '國際音標（通用）', 聲調記號: '不標', 濁送氣: 'ʱ' },
  '王力1957': { 擬音版本: '漢語史稿', 音標體系: '國際音標（通用）', 聲調記法: '不標' },
  '王力1985': { 擬音版本: '漢語語音史（隋——中唐音系）', 音標體系: '國際音標（通用）', 聲調記法: '不標' },
  '潘悟雲2000': { 版本: '2000：漢語歷史音韻學', 非前三等介音: 'i', 聲調記號: '隱藏', 送氣記號: 'ʰ', 支韻: 'iɛ', 虞韻: 'iʊ' },
  '潘悟雲2013': { 版本: '2013：漢語中古音', 非前三等介音: 'i', 聲調記號: '隱藏' },
  '潘悟雲2023': { 版本: '2023：漢語古音手冊', 非前三等介音: 'i', 聲調記號: '隱藏' },
  'unt2020': { 版本: '2020：切韻擬音 J', 後低元音: 'a', 聲調記號: '\u0301\u0300', 鈍C介音: '開ɣ 唇ʋ 合ɣw' },
  'unt2022': { 版本: '2022：切韻擬音 L', 後低元音: 'a', 聲調記號: '\u0301\u0300', 鈍C介音: '開∅ 合w' },
  'unt通俗擬音': { 版本: '2023：切韻通俗擬音', 後低元音: '歌陽唐ɑ 其他a', 聲調記號: '\u0301\u0300', 鈍C介音: '開ɨ 唇低ɨ 唇非低ʉ 合ʉ', 見組非三等簡寫作軟腭音: true },
  'msoeg': { r化元音記號: '\u02DE', 通江宕攝韻尾: 'ɴ/q', 聲調記號: '上ʔ 去h', 章組: '腭噝音 tɕ', 莊三韻母起始: '普通', 宕攝入聲附加: '無' },
};

function getRime(小韻號, from小韻號 = null) {
  let firstEntry = TshetUinh.資料.廣韻.get小韻(from小韻號 || 小韻號)[0];
  let 音韻地位 = 音韻地位patch[小韻號] || propsRimeToDelete[小韻號] || firstEntry.音韻地位;
  let line = {
    小韻號,
    切韻音系描述: 音韻地位.描述,
    攝: 音韻地位.攝 + '攝',
    方音字彙描述: schemas.zihui(音韻地位, null, {}),
    廣韻韻目: 廣韻韻目字to廣韻韻目[firstEntry.來源.韻目],
    平水韻目: 廣韻韻目字to平水韻目[firstEntry.來源.韻目],
    反切: 反切patch[小韻號] || propsRime直音[小韻號] || firstEntry.反切,
  };
  Object.keys(recon2schema).forEach(recon => {
    line[recon] = recon2schema[recon](音韻地位, firstEntry.字頭, recon2params[recon]);
  });
  return line;
}

function getChars(小韻號, from小韻號 = null) {
  const lines = [];
  let entries = TshetUinh.資料.廣韻.get小韻(from小韻號 || 小韻號);
  if (小韻號 === '2767b') entries = entries.slice(0, 1);
  else if (小韻號 === '2767c') entries = entries.slice(1);
  entries.forEach(entry => {
    let { 字頭, 釋義 } = entry;
    lines.push({ 小韻號, 字頭, 釋義 });
    if (charInsertionsAfter[字頭]) {
      [字頭, 釋義] = charInsertionsAfter[字頭];
      lines.push({ 小韻號, 字頭, 釋義 });
    }
  });
  return lines;
}

function getAllRimes() {
  let lines = [];
  for (const rimeNum of TshetUinh.資料.廣韻.iter小韻號()) {
    lines.push(getRime(rimeNum));
    if (rimeNum === '2767b') lines.push(getRime('2767c', rimeNum));
  }
  return lines;
}

function getAllChars() {
  let lines = [];
  for (const rimeNum of TshetUinh.資料.廣韻.iter小韻號()) {
    lines.push(...getChars(rimeNum));
    if (rimeNum === '2767b') lines.push(...getChars('2767c', rimeNum));
  }
  return lines;
}

function downloadLines(lines, filename) {
  lines = [Object.keys(lines[0])] // head
    .concat(lines.map(Object.values)); // body
  lines = lines.map(line => line.join('\t')).join('\n');
  const blob = new Blob([lines], { type: 'text/plain' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}
