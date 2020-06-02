def readNumber(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        keta = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * keta
            keta /= 10
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index


def readPlus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1


def readMinus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1

# 掛け算
def readMulti(line, index):
    token = {'type': 'MULTI'}
    return token, index + 1


# 割り算
def readDivide(line, index):
    token = {'type': 'DIVIDE'}
    return token, index + 1


# 開きかっこ
def readOpenBrackets(line, index):
    token = {'type': 'OPEN'}
    return token, index + 1


# 閉じかっこ
def readCloseBrackets(line, index):
    token = {'type': 'CLOSE'}
    return token, index + 1


def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = readNumber(line, index)
        elif line[index] == '+':
            (token, index) = readPlus(line, index)
        elif line[index] == '-':
            (token, index) = readMinus(line, index)
        elif line[index] == '*':
            (token, index) = readMulti(line, index)
        elif line[index] == '/':
            (token, index) = readDivide(line, index)
        elif line[index] == '(':
            (token, index) = readOpenBrackets(line, index)
        elif line[index] == ')':
            (token, index) = readCloseBrackets(line, index)
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens


# 負の数を表すマイナスをそのあとの数字に統合
def evaluate_negative_number(tokens, index):
    tokens[index] = {'type': 'NUMBER', 'number': -tokens[index + 1]['number']}
    tokens.pop(index + 1)


# かっこの中身を評価
def evaluate_brackets(tokens):
    index = 0
    while index < len(tokens):
        # 開きかっこがきたら、
        # そのあとの要素を引数にして自分自身を呼び出し
        if tokens[index]['type'] == 'OPEN':
            return tokens[:index] + evaluate_brackets(tokens[index + 1:]) 
        # 閉じかっこがきたら、
        # その前までの要素を計算してNUMBERにしたものと、閉じかっこのあとの要素を引数にして自分自身を呼び出し
        elif tokens[index]['type'] == 'CLOSE':
            return evaluate_brackets([{'type':'NUMBER', 'number':evaluate(tokens[:index])}] + tokens[index + 1:])
        index += 1
    # かっこが無くなったら返す
    return tokens


# 掛け算と割り算を計算
def evaluate_multi_devide(tokens):
    index = 1
    while index < len(tokens):
        # a * b ->　aの部分に計算結果を保存
        if tokens[index]['type'] in ['MULTI', 'DIVIDE']:
            if tokens[index]['type'] == 'MULTI':
                if tokens[index + 1]['type'] == 'MINUS':
                    evaluate_negative_number(tokens, index + 1)
                tokens[index - 1]['number'] *= tokens[index + 1]['number']
            elif tokens[index]['type'] == 'DIVIDE':
                if tokens[index + 1]['type'] == 'MINUS':
                    evaluate_negative_number(tokens, index + 1)
                tokens[index - 1]['number'] /= tokens[index + 1]['number']
            # a * b ->　* と b は削除
            tokens.pop(index+1)
            tokens.pop(index)
            # 削除した分indexを戻しておく
            index -= 1
        index += 1


# 足し算と引き算を評価
def evaluate_plus_minus(tokens):
    # 式の初めがマイナスなら
    if tokens[0]['type'] == 'MINUS':
        evaluate_negative_number(tokens, 0)

    index = 1 

    while index < len(tokens):
        if tokens[index]['type'] in ['PLUS', 'MINUS']:
            if tokens[index]['type'] == 'PLUS':
                if tokens[index + 1]['type'] == 'MINUS':
                    evaluate_negative_number(tokens, index + 1)
                tokens[index - 1]['number'] += tokens[index + 1]['number']
            elif tokens[index]['type'] == 'MINUS':
                if tokens[index + 1]['type'] == 'MINUS':
                    evaluate_negative_number(tokens, index + 1)
                tokens[index - 1]['number'] -= tokens[index + 1]['number']
            else:
                print('Invalid syntax')
                exit(1)
            tokens.pop(index+1)
            tokens.pop(index)
            index -= 1
        index += 1


def evaluate(tokens):
    # まずは()の中身を評価
    tokens_without_branckets = evaluate_brackets(tokens)
    #tokens_without_branckets.insert(0, {'type': 'PLUS'})  # Insert a dummy '+' token
    
    # 割り算と掛け算は優先
    evaluate_multi_devide(tokens_without_branckets)
    # 足し算と引き算はそのあと
    evaluate_plus_minus(tokens_without_branckets)
    
    if len(tokens_without_branckets) != 1:
        print('Invalid syntax')
        exit(1)
    return tokens_without_branckets[0]['number']


def test(line):
    tokens = tokenize(line)
    actualAnswer = evaluate(tokens)
    expectedAnswer = eval(line)
    if abs(actualAnswer - expectedAnswer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expectedAnswer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expectedAnswer, actualAnswer))


# Add more tests to this function :)
def runTest():
    print("==== Test started! ====")

    test("1")
    # 足し算
    test("1+2")
    test("1+5+3+8+10")
    test("1+5+3+8000+10")
    test("1.23456789+2")
    test("1+5.0+3+8.76+10.9")
    # 引き算
    test("2-1")
    test("0-2")
    test("-2-1")
    test("-1-5-3-8-10")
    test("-1-5-300000-8-10")
    test("-2.001-1")
    test("1-5.0-3-8.76-10.9")
    # 足し算と引き算
    test("1.0+2.1-3")
    test("-5.923+2.1-3")
    # 掛け算
    test("1*2")
    test("0*9")
    test("10000*5222*3810")
    test("5*3.8884")
    test("1*5.0*3*8.76*10.9234")
    # 割り算
    test("2/4")
    test("1/5")
    test("0/5")
    test("10000/5222/3810")
    test("1/5.0/3/8.76/10.9")
    # 全部まぜ
    test("3.0+4*2-1/5")
    test("-3.0+4*2-1/5")
    test("-3.0-4*2-1/5")
    test("-3.99991-4.4*2.3321-1/5")
    test("-3.99991-4.4*2.3321-1/5*4/4+1.2222-3.4*333-2144/44444")
    # かっこ
    test("(1)")
    test("(1+2)")
    test("(1+2)+3")
    test("2+(-1)+3")
    test("2*(2+3)")
    test("((1+2)+3)")
    test("((1+2)*3)")
    test("2+(((((1+2)+3)+6)*9))")
    test("(1+2)/(3.0*3-4.6+2)*8-1.9999")
    # 負の数
    test("-2+-1")
    test("-2--1")
    test("-2*-1")
    test("2*-1")
    test("-2/-1")
    test("2/-1")


    print("==== Test finished! ====\n")


runTest()

# while True:
#     print('> ', end="")
#     line = input()
#     tokens = tokenize(line)
#     answer = evaluate(tokens)
#     print("answer = %f\n" % answer)
