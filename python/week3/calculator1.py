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


def read_bracket_open(line, index):
    token = {'type': 'OPEN'}
    return token, index+1


def read_bracket_close(line, index):
    token = {'type': 'CLOSE'}
    return token, index+1


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
        elif line[index] == '(':
            (token, index) = read_bracket_open(line, index)
        elif line[index] == ')':
            (token, index) = read_bracket_close(line, index)
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens


def evaluate_bracket(tokens):
    """
    () の中を計算する

    トークンのリストを逆順にたどる
    ( を見つけたら、順にたどってペアの ) を探す
    () の中を計算する
    リストから、() で囲まれた範囲を切り取って、計算結果を挿入する
    TODO: () のペアが揃わなかったときの処理
    """

    index = len(tokens) - 1

    while index >= 0:
        if tokens[index]['type'] == 'OPEN':
            for i in range(index + 1, len(tokens)):
                if tokens[i]['type'] == 'CLOSE':
                    tmp = evaluate(tokens[index + 1:i]) # Note: index と i があるとわかりにくい？
                    del tokens[index:i]
                    tokens[index] = {'type':'NUMBER', 'number':tmp}
                    break
        index -= 1

    return tokens


def evaluate_four_operations(tokens):
    """
    四則演算

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
                if tokens[index+1]['number'] == 0:
                    return None # TODO: 0 で割ろうとしたときの処理
                tmp = tokens[index - 1]['number'] / tokens[index + 1]['number'] # 徐算をする
                del tokens[index - 1:index + 1] # 計算した部分をリストから削除
                tokens[index - 1] = {'type':'NUMBER', 'number': tmp} # 計算結果をリストに挿入
            else:
                print('divide_error')
        elif tokens[index]['type'] == 'NUMBER' or tokens[index]['type'] == 'PLUS' or tokens[index]['type'] == 'MINUS':
            index += 1
        else:
            print('token_type_error')
            exit(1)

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


def evaluate(tokens):
    tokens = evaluate_bracket(tokens)
    answer = evaluate_four_operations(tokens)
    return answer


def test(line):
    tokens = tokenize(line)
    actual_answer = evaluate(tokens)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" %
              (line, expected_answer, actual_answer))


# Add more tests to this function :)
def run_test():
    print("==== Test started! ====")

    test("1")
    test("+1")      # 正数
    test("-1")      # 負数
    test("1.1")     # 小数

    """
    整数 整数
    整数 小数
    小数 整数
    小数 小数

    0 整数
    整数 0
    0 小数
    小数 0
    """

    # test of +
    test("1+2")
    test("1+0.2")
    test("0.1+2")
    test("0.1+0.2")

    # test of -
    test("1-2")
    test("1-0.2")
    test("0.1-2")
    test("0.1-0.2")

    # test of *
    test("1*2")
    test("1*0.2")
    test("0.1*2")
    test("0.1*0.2")

    # test of /
    test("1/2")
    test("1/0.2")
    test("0.1/2")
    test("0.1/0.2")
    test("0/1")
    # test("1/0")
    test("0/1.0")
    # test("1.0/0")

    # mix
    test("1+2-3")
    test("1+2*3")
    test("1+2/3")
    test("1-2*3")
    test("1-2/3")
    test("1*2/3")
  
    test("1.0+2.1-3")
    test("1.0+2.1*3")
    test("1.0+2.1/3")
    test("1.0-2.1*3")
    test("1.0-2.1/3")
    test("1.0*2.1/3")

    # test of brackets
    test("(1)")
    test("(((1)))")
    test("(1+2)")
    test("(1+2)-3")

    # too big or small
    test("0.12345678901234567890")
    test("100000000000000000000*10000000000000")

    print("==== Test finished! ====\n")


run_test()


while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)
