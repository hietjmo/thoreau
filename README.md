# Thoreau

Text tools in interlingua

## Thoreau re

Cerca in dictionarios (files texto). Per exemplo

`python thoreau-re.py ~/interlingua/macovei/wikisource/dictionario-encyclopedic-2021-06-28.txt --num 100 --log`

![thoreau-re-screencap-1](https://github.com/hietjmo/thoreau/blob/main/scriptor-screencap-2.png?raw=true)

![thoreau-re-screencap-2](https://github.com/hietjmo/thoreau/blob/main/scriptor-screencap-2.png?raw=true)

## Thoreau scriptor

Le 'ngrammas' que le programma usa es hic: https://github.com/hietjmo/frequentia/tree/main/ngrams
Face un directory 'ngrams/' e extrahe le pacchettos in isto (6 files csv, in toto 140 MB).

![scriptor-screencap-2](https://github.com/hietjmo/thoreau/blob/main/scriptor-screencap-2.png?raw=true)

Usa le option `--log` a monstrar le messages de function `log_me`.
```
python thoreau-scriptor.py --log +BCDEFGHW
```
![scriptor-screencap-1](https://github.com/hietjmo/thoreau/blob/main/scriptor-screencap-1.png?raw=true)
