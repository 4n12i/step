// アナグラムになる単語のリストを返す
fn find_anagram(random_word: &Vec<String>, dictionary: &Vec<Vec<String>>) -> Vec<String> {
    let mut anagrams: Vec<String> = Vec::new();

    let sorted_random_word = random_word.sort();

    // Note: sort ができないのでデータ構造を考え直す必要がある？
    let mut new_dictionary: Vec<(&Vec<String>, &Vec<String>)> = Vec::new();
    for word in dictionary {
        new_dictionary.push((sort(word), word));
    }

    return anagrams;
}


// 二分探索して、アナグラムになりうる単語を探す
fn binary_search(word: &Vec<String>, dict: &Vec<(&Vec<String>, &Vec<String>)>) -> Vec<Vec<&String>> {
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
fn read_file(file_name: &str) {
    
}


// [未実装] ファイルへの書き込み
fn write_anagram(list_of_anagram: &Vec<Vec<String>>) {

}


// [未実装]
fn main() {
    // 引数の受け取り

    // dictionary = read_file(file_name);
    // answer = find_anagram(random_word, dictionary);
    // write_anagram(answer)
}
