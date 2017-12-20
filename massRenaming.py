import os, sys, re

os.chdir('C:/users/sebastian/desktop/ved vejen 3/')

number = 36
for i in os.listdir():
	os.rename(i, f'{number}.mp3')
	number += 1