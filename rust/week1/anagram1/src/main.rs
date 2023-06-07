use std::env;
use std::fs::File;
use std::io::prelude::*;

// 文字列を ASCII コードのベクタに変換する
fn string_to_bytes(word: &str) -> Vec<u8> {
    let mut bytes: Vec<u8> = Vec::new();
    for c in word.bytes() {
        println!("{:x}", c);
    }
    return bytes;
}


// アナグラムになる単語のリストを返す
fn find_anagram(word: &str, dictionary: &Vec<Vec<String>>) -> Vec<String> {
    let mut anagrams: Vec<String> = Vec::new();

    let mut sorted_word = string_to_bytes(word).sort();

    // Note: sort ができないのでデータ構造を考え直す必要がある？
    let mut new_dictionary: Vec<(&Vec<String>, &Vec<String>)> = Vec::new();
    for word in dictionary {
        new_dictionary.push((sort(word), word));
    }

    return anagrams;
}


// 二分探索して、アナグラムになりうる単語を探す
fn binary_search(word: str, dict: &Vec<(&Vec<String>, &Vec<String>)>) -> Vec<Vec<&String>> {
    let left: usize = 0;
    let right: usize = dict.len() - 1;

    let mut anagrams: Vec<&Vec<String>> = Vec::new();

    while right >= left {
        let mut middle: usize = (left + right) / 2;

        if word < dict[middle].0 {
            right = middle - 1;
        } else if word > dict[middle].0 {
            left = middle + 1;
        } else {
            for i in (0..middle).rev() {
                if word == dict[i].0 {
                    anagrams.push(dict[i].1);
                } else {
                    break;
                }
            }
            for i in middle+1..dict.len() {
                if word == dict[i].0 {
                    anagrams.push(dict[i].1);
                } else {
                    break;
                }
            }
            break;
        }
    }

    // Note: life time のエラーが出る
    //       そしてまだ life time が何かわかっていない 
    return anagrams;
}


// [未実装] ファイルの読み込み
fn read_file(file_name: &String) {
    let mut a_file = File::open(file_name)
    // ファイルが見つからない
    .expect("file not found");

    let mut dictionary = String::new();
    a_file.read_to_string(&mut dictionary)
        // ファイルの読み込み中に問題が発生
        .expect("something went wrong reading the file");

    // テキストは \n{}
    println!("With text:\n{}", dictionary);   
}


// [未実装] ファイルへの書き込み
fn write_anagram(list_of_anagram: &Vec<Vec<String>>) {

}


struct Config {
    file_name: String, 
    word: String,
}


fn parse_config(args: &[String]) -> Config {
    let file_name = args[1].clone();
    let word = args[2].clone();

    Config { file_name, word }
}


// [未実装]
fn main() {
    // 引数の受け取り
    // anagram1.py dictionary_file a_word
    let args: Vec<String> = env::args().collect();
    println!("{:?}", args);

    let config = parse_config(&args);
    println!("file: {}, word: {}", config.file_name, config.word);

    read_file(&config.file_name);

    // dictionary = read_file(file_name);
    // answer = find_anagram(random_word, dictionary);
    // write_anagram(answer)
}
