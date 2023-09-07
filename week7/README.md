# week7 - malloc challenge

## Usage

```bash
# move into malloc dir
cd malloc

# build
make

# run a benchmark (for score board)
make run

# run a small benchmark for tracing (NOT for score board, just for visualization and debugging purpose)
make run_trace
```

## Report

### List of `malloc` programs
- [malloc.c](malloc/malloc.c) : 一番性能が良い `malloc` 
- [simple_malloc.c](malloc/simple_malloc.c) : 
- [malloc_bestfit.c](malloc/malloc_bestfit.c) 
- [malloc_worstfit.c](malloc/malloc_worstfit.c) 

### Simple-fit, Best-fit, Worst-fit の性能比較 

### Free-list-bin の実装
- 最初 bin の数を 10個（2の冪乗で区切る）にしてみた  
→ 速度が速くなった！

- 次に、bin の数を512個（4096/8）にした  
→ さらに速度が速くなった！

### 空き領域の結合（未完成）
- 領域を開放するときに右側に空き領域があった場合は、領域を結合する
- 左側の結合は未実装

## License

[MIT](./LICENSE)

## Reference

[malloc_challenge](https://github.com/hikalium/malloc_challenge) 

