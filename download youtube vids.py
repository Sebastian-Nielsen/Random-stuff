import os
def download_youtube_vids():
    #"""https://www.youtube.com/watch?v=3dXuf1mr8OE
    #https://www.youtube.com/watch?v=w4Mn_kBHqhU
    os.chdir('C:/users/sebastian/downloads/ffmpeg/bin')

    print(os.getcwd())


    links = """https://www.youtube.com/watch?v=nYFCD_p_rfI
https://www.youtube.com/watch?v=XymbLm4wu0w
https://www.youtube.com/watch?v=jHuFFYeyA04
https://www.youtube.com/watch?v=Om0ZPHyc004
https://www.youtube.com/watch?v=HnfoA46HqJA
https://www.youtube.com/watch?v=Nz5FAiksSzY
https://www.youtube.com/watch?v=sCfIbW3TgCA
https://www.youtube.com/watch?v=lP1H4lsPPPI
https://www.youtube.com/watch?v=muFKEEajDNU
https://www.youtube.com/watch?v=LUHts-NK4zE
https://www.youtube.com/watch?v=24JRujMe6WQ
https://www.youtube.com/watch?v=KX0aFGh1xyA
https://www.youtube.com/watch?v=l8wzPeZzmbE
https://www.youtube.com/watch?v=KBr1aeIGDL4
https://www.youtube.com/watch?v=eHrWzKvdsf8"""

    cmd = 'youtube-dl.exe --no-check-certificate '
    for link in links.split('\n'):
        os.system(cmd+link)


download_youtube_vids()
