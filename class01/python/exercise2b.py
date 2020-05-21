from exercise2a import read_dictionary, DIC_NAME, quick_sort_string, consider_qu, choose_answer
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
    count = 100

    while (count > 0) :
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
                el = elem.text
                input_string += elem.text.lower()
            # anagramの候補
            anaglams = counting_solution(input_string, dic)
            # 一番得点が高いものを選ぶ
            answer = choose_answer(anaglams)
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

        count -= 1