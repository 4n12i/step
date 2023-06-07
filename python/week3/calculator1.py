#! /usr/bin/env python
# -*- coding: utf-8 -*-

def read_number(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal
            decimal /= 10
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index


def read_plus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1


def read_minus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1


def read_mult(line, index):
    token = {'type': 'MULTIPLY'}
    return token, index + 1


def read_div(line, index):
    token = {'type': 'DIVIDE'}
    return token, index + 1


def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = read_number(line, index)
        elif line[index] == '+':
            (token, index) = read_plus(line, index)
        elif line[index] == '-':
            (token, index) = read_minus(line, index)
        elif line[index] == '*':
            (token, index) = read_mult(line, index)
        elif line[index] == '/':
            (token, index) = read_div(line, index)
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens


def evaluate(tokens):
    """
    エラー処理などは考えずに一旦最低限の機能だけ実装
    リストを2回ループして計算する
    1回目: * /
    2回目: + -
    """

    answer = 0
    tokens.insert(0, {'type': 'PLUS'})  # Insert a dummy '+' token
    index = 1

    """
    Example: 2*3+6/2

    0 1 2 3 4 5 6 7 (index_of_tokens)
    + 2 * 3 + 6 / 2   index=1 pass
    + 2 * 3 + 6 / 2   index=2 type == *
    + 3 + 6 / 2       index=2 del tokens[1:3] result_token = {'type' = 'NUMBER', 'number' = 2*3}
    + 6 + 6 / 2       index=2 tokens[1] = result_token
    + 6 + 6 / 2       index=2 pass
    + 6 + 6 / 2       index=3 pass
    + 6 + 6 / 2       index=4 type == /
    + 6 + 2           index=4 del tokens[3:5] result_token = {'type' = 'NUMBER', 'number' = 6/2}
    + 6 + 6           index=4 tokens[3] = result_token
    """
 
    # * or / 
    while index < len(tokens):
        if tokens[index]['type'] == 'MULTIPLY':
            if tokens[index - 1]['type'] == 'NUMBER' and tokens[index - 1]['type'] == 'NUMBER': # 演算子の前後の数字をチェック
                tmp = tokens[index - 1]['number'] * tokens[index + 1]['number'] # 乗算をする
                del tokens[index - 1:index + 1] # 計算した部分をリストから削除
                tokens[index - 1] = {'type':'NUMBER', 'number': tmp} # 計算結果をリストに挿入
            else:
                print('multiply_error')
        elif tokens[index]['type'] == 'DIVIDE':
            if tokens[index - 1]['type'] == 'NUMBER' and tokens[index - 1]['type'] == 'NUMBER': # 演算子の前後の数字をチェック
                tmp = tokens[index - 1]['number'] / tokens[index + 1]['number'] # 徐算をする
                del tokens[index - 1:index + 1] # 計算した部分をリストから削除
                tokens[index - 1] = {'type':'NUMBER', 'number': tmp} # 計算結果をリストに挿入
            else:
                print('divide_error')
        elif tokens[index]['type'] == 'NUMBER' or tokens[index]['type'] == 'PLUS' or tokens[index]['type'] == 'MINUS':
            index += 1
        else:
            print('token_type_error')

    # + or -
    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
            else:
                print('Invalid syntax')
                exit(1)
        index += 1
    return answer


def test(line):
    tokens = tokenize(line)
    evaluate(tokens)
    actual_answer = evaluate(tokens)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" %
              (line, expected_answer, actual_answer))


def test_tokenize(line):
    token = tokenize(line)
    print(token)

# Add more tests to this function :)
def run_test():
    print("==== Test started! ====")
    # 1数
    test("1")
    test("+1")      # 正数
    test("-1")      # 負数
    test("1.1")     # 小数

    # 2数の四則演算
    test("1+2")
    test("1-2")
    test("1*2")
    test("1/2")

    # 3数の四則演算
    test("1+2-3")
    test("1+2*3")
    test("1+2/3")
    test("1-2*3")
    test("1-2/3")
    test("1*2/3")
  
    test("1.0+2.1-3")
    test("3*2+4/2") 

    print("==== Test finished! ====\n")


run_test()


while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)
