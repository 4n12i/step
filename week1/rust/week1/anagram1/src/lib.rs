use std::error::Error;
use std::fs::File;
use std::io::prelude::*;

pub struct Config {
    pub file_name: String, 
    pub word: String,
}

impl  Config {
    pub fn new(args: &[String]) -> Result<Config, &'static str> {
        // 引数の数をチェック
        if args.len() < 3 {
            return Err("not enough arguments");
        }

        let file_name: String = args[1].clone();
        let word: String = args[2].clone();

        Ok(Config { file_name, word })
    }
}

pub fn run(config: Config) -> Result<(), Box<dyn Error>> {
    // Note: ok のときは (), error のときは Box を返す
    // Note: 呼び出し元が処理できるように ? 演算子を使用してエラー値を返す
    // ファイルの読み込み
    let mut a_file = File::open(config.file_name)?;

    let mut dictionary = String::new();
    a_file.read_to_string(&mut dictionary)?;

    // テキストは \n{}
    println!("With text:\n{}", dictionary);

    test();

    Ok(())
}

fn test() {
    println!("this is function test !");
}

struct Word {
    word: String, 
    sorted_word: String,

}

impl Word {
    // 文字列を ASCII コードのベクタに変換する
    // fn string_to_bytes(word: String) -> Vec<u8> {
        
    // }
    fn sort_random_word(word: &str) -> String {
        let mut sorted_word = word.clone();
        sorted_word.sort();
    }
}

// fn string_to_bytes(word: &str) -> Vec<u8> {
//     let mut bytes: Vec<u8> = Vec::new();
//     for c in word.bytes() {
//         println!("{:x}", c);
//     }
//     return bytes;
// }


// // アナグラムになる単語のリストを返す
// fn find_anagram(word: &str, dictionary: &Vec<Vec<String>>) -> Vec<String> {
//     let mut anagrams: Vec<String> = Vec::new();

//     let mut sorted_word = string_to_bytes(word).sort();

//     // Note: sort ができないのでデータ構造を考え直す必要がある？
//     let mut new_dictionary: Vec<(&Vec<String>, &Vec<String>)> = Vec::new();
//     for word in dictionary {
//         new_dictionary.push((sort(word), word));
//     }

//     return anagrams;
// }


// // 二分探索して、アナグラムになりうる単語を探す
// fn binary_search(word: str, dict: &Vec<(&Vec<String>, &Vec<String>)>) -> Vec<Vec<&String>> {
//     let left: usize = 0;
//     let right: usize = dict.len() - 1;

//     let mut anagrams: Vec<&Vec<String>> = Vec::new();

//     while right >= left {
//         let mut middle: usize = (left + right) / 2;

//         if word < dict[middle].0 {
//             right = middle - 1;
//         } else if word > dict[middle].0 {
//             left = middle + 1;
//         } else {
//             for i in (0..middle).rev() {
//                 if word == dict[i].0 {
//                     anagrams.push(dict[i].1);
//                 } else {
//                     break;
//                 }
//             }
//             for i in middle+1..dict.len() {
//                 if word == dict[i].0 {
//                     anagrams.push(dict[i].1);
//                 } else {
//                     break;
//                 }
//             }
//             break;
//         }
//     }

//     // Note: life time のエラーが出る
//     //       そしてまだ life time が何かわかっていない 
//     return anagrams;
// }


// // [未実装] ファイルへの書き込み
// fn write_anagram(list_of_anagram: &Vec<Vec<String>>) {

// }
