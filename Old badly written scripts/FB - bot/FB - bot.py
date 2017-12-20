from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
from time import sleep
import re
browser = webdriver.Chrome()
with open("UserPaswdHere ", 'r') as f:
    data = f.read()

lst = [x.split(":") for x in data.split("\n")]
maxcount = int(lst[1][0])  # input('Type the maxcount. (This is how many times the bot should scroll down on the liked pages of the profiles. Until it hits the "loading more liked pages of the user", it takes 3 sec for every scroll.)')
print("If you want several keywords. Seperate them by a '+' sign. Remember it's case sensitive!")
pattern = [pattern for pattern in input('Type the keyword(s) to search through the comments with here: ').strip().split('+')]
keyword = [keyword for keyword in input('Type the keyword(s) to search through the liked pages with here:').strip().split('+')]
print('You got the following keyword(s):', pattern)
browser.get('https://www.facebook.com/login')
WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'email'))).send_keys(lst[0][0])
browser.find_element_by_id('pass').send_keys(lst[0][1])
browser.find_element_by_id('loginbutton').click()
sleep(1.5)
loadMore = input('load more')
comment = input('')


load = browser.find_element_by_css_selector(loadMore)
while True:
    try:
        load.click()
        sleep(0.75)
    except:
        break

elemt = browser.find_elements_by_css_selector(comment + ' > div')

a = browser.find_elements_by_css_selector(comment+ ' > div > div > div > div > div > div > div > div > div > span > a')


for i in elemt:
    if re.search(r'^[0-9]+\s(answer|svar)', i.text):
        elemt.remove(i)


print('______')
highlight = []
dic = {}
for i, t in enumerate(elemt):

    for p in pattern:
        if re.search(p, t.text):
            if i not in highlight:
                highlight.append(i)
            dic[i] = t.text

lst = []
for i, link in enumerate(a):
    temp = link.get_attribute("href")
    if not re.search(r'https:\/\/www\.facebook\.com\/[0-9]+\/photos\/a', temp):
        lst.append(temp)

if len(elemt) > len(lst): # Hvis overskudne links til comments, slet de de links i overskud. To avoid possible error
    overskud = len(elemt) - len(lst)
    elemt = elemt[:-overskud]



print('Data collected, opening tabs ..')
TabCounter = 0
IndexCounter = -1
NoLikedPages, highlightPages = [], []
for index in highlight:

    IndexCounter += 1
    TabCounter += 1  # flytter til den næste tab, increaser med en.

    print('______________________\nCurrently at',index,'in', highlight)
    browser.execute_script("window.open('" + lst[index] + "','_blank');")
    browser.switch_to_window(browser.window_handles[TabCounter])
    sleep(2)


    url = browser.current_url  # går ind på profilens "liked pages", og scroller til bunden
    base = re.search(r'https:\/\/www\.facebook\.com\/[0-9A-Za-z.]+', url)
    url_to_liked_pages = base.group() + '/likes'
    browser.get(url_to_liked_pages)
    sleep(4)
    def ScrollPage():
        lenOfPage = browser.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        match = False
        count = 0
        while (match == False):
            lastCount = lenOfPage
            sleep(2.80)
            lenOfPage = browser.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            count += 1
            if lastCount == lenOfPage or count == maxcount:
                match = True
    ScrollPage()



    try:  # Finder liked pages på siden, hvis der ikke er nogen. har profilen ingen liked pages.
        selector = 'div>div>div>div>div>div>div>div>div>div>div>div>div>div._5h60._30f'
        browser.find_element_by_css_selector(selector)
        ulGroups = browser.find_elements_by_css_selector(selector + ' > ul > li')
        sleep(4)
        print(browser.current_url, url_to_liked_pages)
        assert browser.current_url == url_to_liked_pages
    except:  # Slet profilens index fra highlight, siden han ikke havde nogen "liked pages".
        print('This profile has no "liked pages", skipping her.')
        #del highlightPages[IndexCounter]  # Slet den tomme list, som profilens "liked pages" oprindeligt skulle være lagt i.
        NoLikedPages.append(index)   # Lægger index til profilen i en list. Med hensigt i at slette den index fra highlight når loopet er færdigt.
        IndexCounter -= 1            # Neutraliser Indexcounter, da vi ikke ønsker at få den til at stige med en,
        continue                     # siden vi ikke add'ede en til list til highlightPages. Da profilen ikke havde nogen "likedpages"

    highlightPages.append([])   # appender en tom list til at putte profilens "liked pages" i


    LikedPages = [] # Alle profilens liked pages
    for i in ulGroups:
        LikedPages.append(i.text.split('\n')[0])


    for i in LikedPages: # Add'er liked page til "highlightPages, hvis den indeholder keyword, og ikke allerede er i listen.
        for k in keyword:
            if re.search(k, i) and i not in highlightPages[IndexCounter]:
                highlightPages[IndexCounter].append(i)


# highlight består nu kun af profiler, der har nogle "likedpages". Hvis ikke, bliver de tager fra.
highlight = [i for i in highlight if i not in NoLikedPages]

if highlight == []:
    print('There was no comments, with the keyword(s). Who also had liked pages with the following keyword.')
else:  # hvis ikke empty

    # Skriver data til b.txt
    TextFile = open('b.txt', 'w')
    for i in range(len(highlight)):

        pages = '\n'.join(highlightPages[i])
        print('writing the result of:', i, LikedPages)
        ProfileName = re.search(r'^[A-Z0-9a-z]+\s[A-Za-z0-9]+', dic[highlight[i]]).group()
        TextFile.write(ProfileName + '- Likes pages such as:\n' + pages)

TextFile.close()








