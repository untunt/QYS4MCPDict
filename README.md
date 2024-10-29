# QYS4MCPDict

Generate Qieyun 切韻 system (QYS) data for [MCPDict 漢字音典](https://github.com/osfans/MCPDict) (new data from [TshetUinh.js](https://github.com/nk2028/tshet-uinh-js) &amp; legacy data from [ytenx 韻典網](https://github.com/BYVoid/ytenx))

## Process

1. Run `deriver_schemas.py` to generate `deriver_schemas.js`
2. Open `deriver.html` to generate `all_rimes.tsv` and `all_chars.tsv` in the browser’s download directory
3. Move the `.tsv` files into this repository
4. Run `legacy.py` to generate `all_rimes_legacy.tsv`
5. Run `join.py` to generate `廣韻.tsv`

## Other sources

Patches for rime properities in `deriver_consts.js` are derived from the [discussion](https://github.com/nk2028/tshet-uinh-data/pull/8#issuecomment-2408975945) in nk2028. Some objects in `deriver_consts.js` are cited from the [code](https://github.com/untunt/qieyun-rime-table/blob/main/main.js) of the New Qieyun Rime Table.

## Missing unencoded characters

Serveral unencoded characters are not included in the Guangyun 廣韻 data of [TshetUinh.js](https://github.com/nk2028/tshet-uinh-js) and [ytenx](https://github.com/BYVoid/ytenx), but are noted in poem’s [Guangyun Quanzi Biao 廣韻全字表](https://github.com/nk2028/tshet-uinh-data/blob/main/src/%E5%BB%A3%E9%9F%BB(20170209).csv) (originally on [Zhihu](https://zhuanlan.zhihu.com/p/20430939)). An [issue](https://github.com/nk2028/tshet-uinh-data/issues/9) in [tshet-uinh-data](https://github.com/nk2028/tshet-uinh-data) would add these missing unencoded characters.
