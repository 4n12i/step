# week4 - Data structure & algorithm 2
### Usage

```bash
python wikipedia.py pages_file links_file
```

```bash
$ python --version
Python 3.10.8
```

### 1. `find_shortest_path()`
あるページから別のページへの最短経路を求める。

- 幅優先探索をして経路が存在するか確認する
- 経路がある場合、探索した逆順にノードをたどって最短経路を求める

```bash
$ python wikipedia.py wikipedia_dataset/pages_medium.txt wikipedia_dataset/links_medium.txt          
Finished reading wikipedia_dataset/pages_medium.txt
Finished reading wikipedia_dataset/links_medium.txt

渋谷 -> ギャルサー_(テレビドラマ) -> 小野妹子
```

### 2. `find_most_popular_pages()`
ページランクを計算して、重要度の高いページ Top10 を求める。

- 収束条件: ループの前後において小数点以下2位で丸めたページランクが等しい
- データセット `small` では正常に動作した
- `medium` と `large` はプログラムが終了しない

```bash
$ python wikipedia.py wikipedia_dataset/pages_small.txt wikipedia_dataset/links_small.txt
Popular pages
C
D
B
E
F
A
```