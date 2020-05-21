import time
from selenium import webdriver
sorted_dic_path = '../data/sorted_dictionary.txt'

# 二分探索
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

# 辞書を読む
def read_dictionary(path):
    with open(path) as f:
        lines = [s.strip() for s in f.readlines()]
    return lines

# 辞書を読んで空白区切りにする
def read_created_dictionary(path):
    lines = read_dictionary(path)
    dic = [line.split(' ') for line in lines]
    return dic

# quについて
def consider_qu (input_string, anagrams):
    input_q = input_string.count('q')
    input_u = input_string.count('u')
    if input_q < 0 :
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
            key = my_binary_search(new_candidates, dic)
            if key >= 0:
                anagrams.append(dic[key][1])
            candidates.append(new_candidates)

    # quについての条件を満たさない場合は消す
    considerd_anagrams = consider_qu(s, anagrams)
    return considerd_anagrams

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
    # 辞書の読み込み
    dic = read_created_dictionary(sorted_dic_path)
    driver = webdriver.Chrome()
    driver.get('https://icanhazwordz.appspot.com/')

    try_count = 0
    score = 0
    while (try_count < 10):
        elem1 = driver.find_elements_by_css_selector('.letter.p1')
        elem2 = driver.find_elements_by_css_selector('.letter.p2')
        elem3 = driver.find_elements_by_css_selector('.letter.p3')

        elems = elem1 + elem2 + elem3

        input_string = ''
        for elem in elems :
            input_string += elem.text.lower()
        # 入力をsortする
        s = quick_sort_string(input_string)
        
        # anagramの候補
        anagrams = string_combination_solution(s, dic)
        # 一番得点が高いものを選ぶ
        answer = choose_answer(anagrams)
        score += answer[1]

        # 入力
        form = driver.find_element_by_id('MoveField')
        form.send_keys(answer[0])
        # Submitボタン
        button = driver.find_element_by_xpath("//input[@value='Submit']")
        button.click()

        try_count += 1
    
    # 記録するかどうか
    print(score)
    if score > 1900 :
        nick_name = driver.find_element_by_name('NickName')
        nick_name.send_keys('sora')
        name = driver.find_element_by_name('Name')
        name.send_keys('Sora Tagami')
        email = driver.find_element_by_name('Email')
        email.send_keys('bluesky0906.design@gmail.com')
        button = driver.find_element_by_xpath("//input[@value='Record!']")
        button.click()
    driver.quit()
