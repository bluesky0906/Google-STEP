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
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens


# 掛け算と割り算を計算
## answerを計算しているわけではないが、evaluate_plus_minusと返り値を揃えるために
## answerを返した方がいいのでしょうか…？
def evaluate_multi_devide(tokens):
    index = 1
    while index < len(tokens):
        # a * b ->　aの部分に計算結果を保存
        if tokens[index]['type'] in ['MULTI', 'DIVIDE']:
            if tokens[index]['type'] == 'MULTI':
                tokens[index - 1]['number'] = tokens[index - 1]['number'] * tokens[index + 1]['number']
            elif tokens[index]['type'] == 'DIVIDE':
                tokens[index - 1]['number'] = tokens[index - 1]['number'] / tokens[index + 1]['number']
            # a * b ->　* と b は削除
            tokens.pop(index+1)
            tokens.pop(index)
            # 削除した分indexを戻しておく
            index -= 1
        index += 1


# 足し算と引き算を評価
def evaluate_plus_minus(tokens):
    answer = 0
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
    tokens.insert(0, {'type': 'PLUS'})  # Insert a dummy '+' token
    
    # 割り算と掛け算は優先
    evaluate_multi_devide(tokens)
    # 足し算と引き算はそのあと
    answer = evaluate_plus_minus(tokens)

    return answer


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
    print("==== Test finished! ====\n")


runTest()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)
