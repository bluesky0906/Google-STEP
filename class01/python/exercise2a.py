from webdriver import get_input, send_answer, record_score
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

DIC_NAME = '../data/dictionary.txt'

# 一つずつ文字をつかうかどうか

# 二分探索(使わない)
def my_binary_search(trg, dic):
    left = 0
    right = len(dic) - 1

    while right >= left:
        mid = (right + left) // 2
        guess = dic[mid][0]
        if guess == trg:
            return mid
        elif guess > trg:
            right = mid - 1
        elif guess < trg:
            left = mid + 1
    return -1

# 文字列をsortする関数
def quick_sort_string(arr):
    if len(arr) <= 1:
        return arr

    partition = arr[0]
    count = 0
    left = ''
    right = ''

    for ele in arr:
        if partition > ele:
            left += ele
        elif partition < ele:
            right += ele
        else:
            count += 1
    return quick_sort_string(left) + (partition * count) + quick_sort_string(right)

# 辞書を読む
def read_dictionary(path):
    with open(path) as f:
        lines = [s.strip() for s in f.readlines()]
    return lines

# ソートされた辞書を作る
def create_sorted_dictionary(path):
    lines = read_dictionary(path)
    dic = {quick_sort_string(line): line for line in lines}
    return dic

# quについて
def consider_qu (input_string, anagrams):
    input_q = input_string.count('q')
    input_u = input_string.count('u')
    if input_q <= 0 :
        return anagrams

    considerd_anagram = [anagram for anagram in anagrams if (anagram.count('u') - anagram.count('q')) <= (input_u - input_q)]
    
    return considerd_anagram

# 新しい組み合わせを作って探索 2^(文字列の長さ) * log(辞書の長さ)
def string_combination_solution(s, dic):
    candidates = ['']
    anagrams = []
    for c in s:
        current_candidates = candidates.copy()
        for prev in current_candidates:
            new_candidates = prev + c
            if new_candidates in dic :
                anagrams.append(dic[new_candidates])
            candidates.append(new_candidates)

    # quについての条件を満たさない場合は消す
    considerd_anagrams = consider_qu(s, anagrams)
    return considerd_anagrams

# 点数計算
def calculate_score(s):
    score = 0
    for c in s:
        if c in ['a', 'b', 'd', 'e', 'g', 'i', 'n', 'o', 'r', 's', 't', 'u']:
            score += 1
        # qも2点として扱う
        elif c in ['c', 'f', 'h', 'l', 'm', 'p', 'v', 'w', 'y', 'q']:
            score += 2
        else:
            score += 3
    return (score + 1) ** 2

# どれを答えにするか選ぶ
def choose_answer(anagrams):
    highest = 0
    highest_answer = ''
    for anagram in anagrams:
        score = calculate_score(anagram)
        if score > highest :
            highest_answer = anagram
            highest = score
    return (highest_answer, highest)

if __name__ == '__main__':
    options = Options()
    options.add_argument('--headless')
    # 辞書の読み込み
    dic = create_sorted_dictionary(DIC_NAME)
    driver = webdriver.Chrome(options=options)
    
    count = 10000
    while (count > 0) :
        driver.get('https://icanhazwordz.appspot.com/')

        try_count = 0
        score = 0
        while (try_count < 10):
            input_string = get_input(driver)
            # 入力をsortする
            s = quick_sort_string(input_string)
            # anagramの候補
            anagrams = string_combination_solution(s, dic)
            # 一番得点が高いものを選ぶ
            answer = choose_answer(anagrams)
            score += answer[1]

            send_answer(driver, answer[0])

            try_count += 1
        
        # 記録するかどうか
        print(score)
        if score > 2100 :
            record_score(driver)

        count -= 1

    driver.quit()
