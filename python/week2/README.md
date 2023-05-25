# week2 - data structure & algorithm 1

## 1. `hash_table.py`
Implement a hash table work with mostly O(1).

### Usage
```bash
python hash_table.py
```

### 1. Implement `delete(key)`
- 削除するデータの前後に要素がある場合 -> 前後のデータをポインタで繋ぐ
- 削除するデータが先頭である場合 -> 削除するデータの次のデータを先頭にする

### 2. Implement rehashing
再ハッシュを実装して、データを追加してもほぼ O(1) で動くようにする 
-> テーブルサイズを調節する関数 `expand_hash_table()` , `shrink_hash_table()` を実装した

- 要素数がテーブルサイズの 70% を上回った場合、テーブルサイズを 2 倍に拡張する（ `expand_hash_table()` ）
- 要素数がテーブルサイズの 30% を下回った場合、テーブルサイズを半分に縮小する（ `shrink_hash_table()` ）
- ハッシュの衝突を防ぐため、テーブルサイズは素数になるように再設定する（ `update_table_size()` ）

- 未実装：テーブルサイズが下限を下回りそうになったときの処理が必要？
- 未実装：テーブルサイズを調節する2つの関数は処理が似ているので、ひとつにまとめる

-> `performance_test()` の結果はあまり変化がなかった

### [未完成] 3. Improve the hash function
問題点：アナグラムとなる文字列は同じハッシュ値になるため、ハッシュの衝突が起こりやすい
解決策：ハッシュ関数を改善する


## 2. Hash Table vs. Tree
- データが増えたとき、ハッシュテーブルは再ハッシュを行い、木構造は木を回転させてバランス木を再構築する。再ハッシュよりバランス木を構築する方が簡単にできる？
- 木構造の場合はポインタを使用するため、ハッシュテーブルと比べてメモリの使用量が少ない
- 膨大なデータをハッシュテーブルに収める場合、ハッシュ値を求めるのに時間がかかる（複雑なハッシュ関数を容易する必要がある）
- 木構造の方が容易に検索できる？値が順番に並んでいるので範囲を絞り込みやすい？

## 3. Design a cache that achieves the following operations with mostly O(1)
ハッシュテーブルにキューの要素を加えて実装する？

## [未完成] 4. `cache.py`



