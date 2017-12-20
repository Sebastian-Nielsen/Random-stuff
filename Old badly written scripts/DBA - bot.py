from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
from time import sleep
import win32com.client, os
browser = webdriver.PhantomJS(executable_path=r'C:\Python36\phantomjs-2.1.1-windows\bin\phantomjs.exe')
print("""
                        .-----.      `------`                                                       #      Author: Sebastian
                        ymmmmmd      -mmmmmm/                                                       #      version: 1.0
                        yNNNNNd      -NmNNNN/                                                       #
                        yNNNNNd      -NmNNNN/                                                       #
                        yNNNNNd      -NmNNNN/                                                       #   For at se understøttede katagorier tryk: 1      #virker ikke endnu
                        yNNNNmd      -NmNNNN/                                                       #
            ``--::-.`   ymmNNNd      -NmNNNN/  ``.-::-.``                  ``.-::-.``   ``````      #   ____¤_VIGTIGT_¤__upload af billeder _________________________________________________
         `/sdmmNmmNmdy+.ymNNNNd      -NmNNNN/-ohmNNNNNNmho-`            `.+ydmNmmmNmhs:`shhhhh/     #   Hvis der skal uploades billeder til din annonce skal du oprette en mappe i billeder,
       `ommmNNNNNNNNNNmmmNNNNNd      -NmNNNNdmNNNNNNNNNNNNNh/`         -ymmmNNNNNNNNmmNdNNNNNN+     #   og derefter putte alle billederne ind i mappen som du ønsker uploaded til din annonce.
      :dNmNNmmmmmmmmmmmNNNNNNNd      -NmNNNNNNmmmmmmmmNNNNNNmy.       omNNNNNNmmmmmmmmNNNNNNNN+     #   Det du kalder mappen skal du skrive når der bliver spurgt om det.
     :mmNmmmmdo:.`.-/ymmNNNNNNd      -NmNNNNmNms:.``-:smmmNNmmd`     smNNNNNmy/-.`.:odmmNNNNNN+     #   ¤¤ Computeren kan dsv. ikke bruges mens billeder uploades, pga. af en bug. ¤¤
    `dmNNNmm/         -hNNNNNNd      -NmNNNNmo`        `sNNNNNNs    /NmNNNmh-         /mNNNNNN+     #   ¤¤ Du skal nok blive advaret når billederne vil blive uploadet.            ¤¤
    :mmNmmm/           `mNNNNNd      -NmNNNNs            yNNNNmm`   ymmNNmm`           /NNNNNN+     #   _____________________________________________________________________________________
    +mNNNNN.            ymNNNNd      -NmNNNN/            +NNNNNN.   dmNNNNh            .NmNNmN+     #
    :NNNNmNo           .mmNNNNd      -NmNNNNy           `hmNNNmm`   ymNNNNm.           +NNNNmN+     #
    `dmNmmNmo`        :dNNNNNmd      -NmNNNNmy.        .ymmNNmNo    :mmNNNmd:        `+mNNNNmN+     #
     -mmNNNmmds/:--:ohmmNNNNNmd      -NmNNNNmmmy+:--:+ymNNNNmmh`     ommNmNNmho/--:/sdmmNNNNmN+     #
      -hmmNmNNmmmmmmNNNNNNNNNmd      -NmNNNNNNNNmmmmmmNNNNmmms`      `+mNmNNNNNmmmmmNNNNNNNNmN+     #
       `+hmmNNNNNNNNNNNddNNNNmd      -NmNNmNhmmNNNNNNNNNNmmy:`         .sdmmNNNNNNNNNmmhmmNNmN+     #
         `-oydmmmmmdhs:..yyyyys      .yyyyyo`.+shdmmmmdhy+.`             ./shdmmmmmdy+-`/yyyyy:     #
            ``.....``                           `......`                    `......``               #
""")
path = 'C:\\Users\\sebastian\\Desktop\\filer\\pictures' # path til mappen "billeder"

def login_dba():
    # Get username and password from txt file
    with open("a.txt", 'r') as f:
        data = f.read()
    lst = [x.split(":") for x in data.split("\n")]
    length = len(lst)

    global username, password
    if length == 0:
        print('Der er ingen gemte brugere, indtast email og password til din dba konto.')
        username, password = input('Email: '), input('Password: ')
    elif length > 1:
        print('\nIndtast nummeret på den bruger du ønsker at logge.')
        for i, email in enumerate(lst):
            print(str(i + 1) + '.', email[0])
        nr = input(': ')
        username = lst[nr][0]
        password = lst[nr][1]


    else:
        username = lst[0][0]
        password = lst[0][1]

    print('Logger ind ..')
    loginUrl = 'https://www.dba.dk/log-ind/'
    browser.get(loginUrl)

    email = browser.find_element_by_id('Email')
    email.send_keys(username)

    adgangskode = browser.find_element_by_id('Password')
    adgangskode.send_keys(password)

    browser.find_element_by_id('LoginButton').click()
    sleep(2)

    if browser.current_url == loginUrl:
        print('\n\nDin email eller password var forkert, tjek mappen EmailPaswd.\nVær sikker på at du har skrevet: "DinEmail:DitPassowrd", med et ":" imellem dem.\nDer må højest være et sæt på hver linje.')
        sleep(1)


    print('Succesfully logged in\n')


def mine_annoncer(output = True):

    browser.get('http://www.dba.dk/min-dbadk/')
    sleep(2)
    try:
        browser.find_element_by_link_text('Se alle mine annoncer').click()
    except:
        pass

    annonce_list = browser.find_elements_by_css_selector('td.mainContent > a')

    if output == True:
        annoncer = browser.find_elements_by_css_selector('div.expandable-box.expandable-box-collapsed > a.listingLink')
        dage = browser.find_elements_by_css_selector('tr > td:nth-child(4) span')

        print(' ' * 70, 'Der blev fundet', len(annonce_list), 'annoncer\n' + '_' * 160)
        for x, annonce in enumerate(annoncer):
            dage_left = str(dage[x].text)
            print(str(x + 1) + '.  |' + dage_left + ' tilbage|    ' + annonce.text + '\n________________________\n')

    return annonce_list
def produkt_info():
    # Bestaar af produkt og maerke

    produkt_info = browser.find_element_by_class_name("vip-additional-text").text.splitlines()[0]
    produkt_info = produkt_info.split(", ")
    info_tekst = browser.find_element_by_class_name("vip-additional-text").text.splitlines()[1:]
    pris = browser.find_element_by_class_name("price-tag").text
    pris = ''.join(letter for letter in pris if letter in '0123456789')

    katagori_list = browser.find_elements_by_css_selector('nav>div>ul>li>a>span')
    katagori = katagori_list[-1].text

    print('Information fra annonce samlet ..')
    return produkt_info, info_tekst, pris, katagori
def opret_annonce(produkt_info, info_tekst, pris, katagori):

    # find den rigtige katagori, som annoncen skal oprettes i
    browser.get('http://www.dba.dk/opret-annonce/')
    elem = browser.find_element_by_class_name('input-xlarge')
    elem.send_keys(katagori)
    browser.find_element_by_css_selector('div > ul > li > strong > a').click()
    sleep(6)

    # er nu inde på selve opret siden, indhold variere efter katagori ovenover^^
    if katagori.lower() == 'armbåndsure og lommeure':
        print('tager de rigtige dropdown menues til ' + katagori)

        p, i = produkt_info[0], '666'     #produkt
        choose_dropdown(p, i, price=True)

        p, i = produkt_info[1], '20554'   #marke
        choose_dropdown(p, i)
    elif katagori.lower() == 'tastaturer og mus':
        print('tager de rigtige dropdown menues til ' + katagori)

        p, i = produkt_info[0], '21934'   #produkt
        choose_dropdown(p, i, price=True)

        p, i = produkt_info[1], '21936'   #marke
        choose_dropdown(p, i, text=True)

        p, i = produkt_info[2], '21937'   #model
        choose_dropdown(p, i, text=True)

        p, i = produkt_info[3], '28109'   #stand
        choose_dropdown(p, i)

    # skriver tekst ind, fundet fra produkt_info
    info_felt = browser.find_element_by_xpath('//*[@id="Input_AdditionalText"]')
    for i in info_tekst:
        info_felt.send_keys(i + "\n")

    #upload billeder hvis der svar ikke er "enter"
    if not pic_svar:
        upload_pic(pic_svar)

    # vaelger gratis pakke
    pakke_felt = browser.find_element_by_class_name('bundle-cta-button').click()

    # brugeren kan stille spoergsmål på annoncen - Default er checked;
    browser.find_element_by_class_name('check-box')

    browser.find_element_by_css_selector('.btn.btn-call-to-action.btn-large.trackClicks').click()
    sleep(7)
def choose_dropdown(produkt, i, text=False, price=False):

    e = browser.find_element_by_id('matrix-element-' + i)

    if price == True:
        elem = browser.find_element_by_id('PriceId_Price')
        elem.send_keys(pris)

    if text == True:
        e.send_keys(produkt)
    else:
        for option in e.find_elements_by_tag_name('option'):
            if option.text == produkt:
                option.click()
def slet_annonce(nummer):
    sleep(2)
    browser.get('http://www.dba.dk/min-dbadk/')
    sleep(3)
    try:
        browser.find_element_by_link_text('Se alle mine annoncer').click()
    except:
        pass
    sleep(0.75)
    slet_buttons = browser.find_elements_by_link_text('Slet')
    print('Der blev fundet:', len(slet_buttons), 'slet buttons.\nTrykker på nummer:', str(nummer-1))

    slet_buttons[nummer-1].click()

    sleep(2)
    elem = browser.find_elements_by_class_name('radio')
    elem[0].click()

    browser.find_element_by_css_selector('div.modal-footer > button.btn.btn-primary').click()
    sleep(5)
    """"  UNCOMMENT HVIS; Der skal være mulighed for at vælge om varen blev solgt. --DEFAULT er nej--
    svar = input('Blev annonce slettet, skriv "ja" eller "nej": ')
    if svar.lower() == 'ja':
        elem[0].click()
    else:
        elem[1].click()"""
def upload_pic(besked):

    input("Klar til at upload billede, du kan ikke bruge pc'en i omkring 5-20 sek. du kan se når den er færdig.\n Tryk en 'enter' for at fortsætte ..")
    driver = webdriver.Chrome()

    driver.get('https://www.dba.dk/log-ind/?returnUrl=%2F')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'Email'))).send_keys('sebastiangrundet@hotmail.dk')
    driver.find_element_by_id('Password').send_keys('syh47nbj')
    driver.find_element_by_id('LoginButton').click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,'fixed')))
    driver.get('http://www.dba.dk/min-dbadk/')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,'fixed')))

    annonce_list = browser.find_elements_by_css_selector('td.mainContent > a')
    annonce_list[-1].click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT,'Rediger'))).click()

    # Upload billed(er)
    upload = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,'uploadButton')))
    driver.execute_script("window.scrollTo(0, 400)")
    lst = os.listdir(path)   # HER SKAL DER STÅ BEDSKED I STEDET FOR PATH, SÅ DE SELV KAN VÆLGE PATH  VIGTIG ########################################
    for billed_navn in lst:
        picture = path + '\\' + billed_navn
        print('uploader:', picture)
        upload.click()
        sleep(0.75)
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.Sendkeys(picture)
        shell.Sendkeys("~")
        sleep(0.75)

    # Betal ikke, og gem ændringer
    driver.execute_script("window.scrollTo(0,1800)")
    try:
        driver.find_element_by_id('IsOn').click()
    except:
        pass
    driver.find_element_by_xpath('//*[@id="content"]/div[2]/div/div/form/div/button').click()
    sleep(0.5)
    driver.quit()



login_dba()
run = True
while run:

    annonce_list = mine_annoncer()
    y = int(input('Indtast nummeret på den annonce, du ønsker at forny: '))
    pic_svar = input('Hvis der skal billeder til, læs venligst "upload af billeder". Hvis ikke skal du bare trykke enter.\nIndtast navnet på mappen billederne er i: ')
    annonce_list[y - 1].click()

    # Indsaml data fra annoncen; Opret annonce med det fundne data
    produkt_info, info_tekst, pris, katagori = produkt_info()
    opret_annonce(produkt_info, info_tekst, pris, katagori)
    print('~' * 20 + '\nAnnonce oprettet, sletter gamle annonce ..')

    # sletter den gamle annonce, og uploader billedet, hvis valgt
    slet_annonce(y)
    if pic_svar:
        upload_pic(pic_svar)







"""__________noter til forberelser_________________________________
1. Skal gøres hurtigere; skift sleep commands ud, med explicit waits.
2. Output skal forbedres;
3. Add feature - som fornyer alle annoncer.
4. Add flere katagorier
5. Path skal oprettes
"""