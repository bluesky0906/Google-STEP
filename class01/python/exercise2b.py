from exercise2a import read_dictionary, DIC_NAME, quick_sort_string, consider_qu, choose_answer
from webdriver import get_input, send_answer, record_score
from selenium import webdriver

# run_length
def run_length(string):
    stirng_count = {}
    for s in string :
        if s in stirng_count :
            stirng_count[s] += 1
        else :
            stirng_count[s] = 1
    return stirng_count

# (辞書単語数)*(単語文字数) ?
def counting_solution(trg, dic):
    anaglams = []
    counted_trg = run_length(trg)
    for d in dic:
        isAna = True
        counted_d = run_length(d)
        for t in counted_d:
            if (t not in counted_trg) or (counted_d[t] > counted_trg[t]):
                isAna = False
                break
        if isAna :
            anaglams.append(d)
    considerd_anagrmas = consider_qu(trg, anaglams)
    return considerd_anagrmas

if __name__ == '__main__':
    # 辞書の読み込み
    dic = read_dictionary(DIC_NAME)

    driver = webdriver.Chrome()
    driver.get('https://icanhazwordz.appspot.com/')

    try_count = 0
    score = 0
    while (try_count < 10):
        input_string = get_input(driver)

        # anagramの候補
        anaglams = counting_solution(input_string, dic)

        # 一番得点が高いものを選ぶ
        answer = choose_answer(anaglams)
        score += answer[1]

        send_answer(driver, answer[0])

        try_count += 1
    
    # 記録するかどうか
    print(score)
    if score > 1900 :
        record_score(driver)

        #count -= 1

    driver.quit()