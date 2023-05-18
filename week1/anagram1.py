def find_anagram(random_word, dictionary):
    sorted_random_word = sorted(random_word)

    new_dictionary = [[sorted(word), word] for word in dictionary]
    new_dictionary.sort()
    
    anagram = binary_search(sorted_random_word, new_dictionary)
    return anagram

def binary_search(sorted_random_word, new_dictionary):
    left = 0
    right = len(new_dictionary)-1

    answer = []

    while right >= left:
        middle = (right + left)//2

        if sorted_random_word < new_dictionary[middle][0]:
            right = middle - 1
        elif sorted_random_word > new_dictionary[middle][0]:
            left = middle + 1
        else:
            for i in range(middle, -1, -1):
                if sorted_random_word == new_dictionary[i][0]:
                    answer.append(new_dictionary[i][1])
                else:
                    break
            for i in range(middle+1, len(new_dictionary)):
                if sorted_random_word == new_dictionary[i][0]:
                    answer.append(new_dictionary[i][1])
                else:
                    break
            break
    return answer

def read_dictionary():
    dictionary = []
    with open('words.txt', 'r', encoding='utf-8') as a_file:
        for a_line in a_file:
            a_string = a_line.split()[0]
            dictionary.append(a_string)
    return dictionary

def write_anagram(list_of_anagram):
    if not list_of_anagram:
        print('no anagrams')
    else:
        with open('output.txt', 'w', encoding='utf-8') as a_file:
            a_file.write('\n'.join(list_of_anagram))

def main():
    dictionary = read_dictionary()
    
    print("input a string")
    random_word = input()

    answer = find_anagram(random_word, dictionary)

    write_anagram(answer)
    

if __name__ == '__main__':
    main()
