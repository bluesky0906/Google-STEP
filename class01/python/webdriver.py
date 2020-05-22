from selenium import webdriver

def get_input(driver):
    elem1 = driver.find_elements_by_css_selector('.letter.p1')
    elem2 = driver.find_elements_by_css_selector('.letter.p2')
    elem3 = driver.find_elements_by_css_selector('.letter.p3')

    elems = elem1 + elem2 + elem3

    input_string = ''
    for elem in elems :
        el = elem.text
        input_string += elem.text.lower()
    
    return input_string

def send_answer(driver, answer):
    # 入力
    form = driver.find_element_by_id('MoveField')
    form.send_keys(answer)
    # Submitボタン
    button = driver.find_element_by_xpath("//input[@value='Submit']")
    button.click()

def record_score(driver):
    nick_name = driver.find_element_by_name('NickName')
    nick_name.send_keys('sora')
    name = driver.find_element_by_name('Name')
    name.send_keys('Sora Tagami')
    email = driver.find_element_by_name('Email')
    email.send_keys('bluesky0906.design@gmail.com')
    button = driver.find_element_by_xpath("//input[@value='Record!']")
    button.click()