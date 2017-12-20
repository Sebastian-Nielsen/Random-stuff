

def remove_spaces(fname):
    with open(fname, 'r+', encoding='utf-8') as file:
        file_str = file.read()
        file_str = re.sub(r'\n{2,}', '\n', file_str)
        print(file_str)

from random import randint
def add_random_spaces(fname):
    NEW = []

    with open(fname, 'r+', encoding='utf-8') as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            list_line = list(line)



            matches = list(re.finditer(r'self\.\w+\s*=', line))[::-1]
            for m in matches:
                print(m)
                list_line.insert(m.end(),   ' '*randint(4, 21))
                print(''.join(list_line), type(list_line))
                list_line.insert(m.end()-1, ' '*randint(4,9))
                print(''.join(list_line))

                line = ''.join(list_line)

            exit()
            matches = list(re.finditer(r'= Label\(', line))[::-1]
            for m in matches:
                list_line.insert(m.end(), ' '*randint(4,5))

                line = ''.join(list_line)
            NEW.append(line)
            continue

            matches = list(re.finditer(r'def \w+\(', line))[::-1]
            for m in matches:
                list_line.insert(m.end()-1,   ' '*randint(2,6))
                list_line.insert(m.end(),     ' '*randint(3,7))

                list_line.insert(m.start()+3,   ' '*randint(4,6))
                line = ''.join(list_line)

            matches = list(re.finditer(r'for\s*\w+,\s*\w+\s*in', line))[::-1]
            for m in matches:
                list_line.insert(m.end(),   ' '*randint(5,9))
                list_line.insert(m.end()-3, ' '*randint(3,6))
                line = ''.join(list_line)


            matches = list(re.finditer(r'if \(?(\')?(\")?\w+\1\2\s*==\s*(\')?(\")?\w+\3\4\)?:', line))[::-1]
            for m in matches:
                list_line.insert(m.start()+2, ' '*randint(3,9))
                list_line.insert(m.end(),     ' '*randint(3,4))
                line = ''.join(list_line)


            matches = list(re.finditer(r'if \(?(\')?(\")?\w+\1\2\s*==', line))[::-1]
            for m in matches:
                list_line.insert(m.end(), ' '*randint(5,9))
                list_line.insert(m.end()-2, ' '*randint(5,9))
                line = ''.join(list_line)


            matches = list(re.finditer(r'if \(?(\')?(\")?\w+\1\2\s*[><]', line))[::-1]
            for m in matches:
                list_line.insert(m.end(), ' '*randint(5,9))
                list_line.insert(m.end()-1, ' '*randint(5,9))
                list_line.insert(m.start()+2, ' '*randint(5,9))
                line = ''.join(list_line)


            matches = list(re.finditer(r'(\')?\w+\1\s*:', line))[::-1]
            for m in matches:
                list_line.insert(m.end(), ' '*randint(12,14))
                list_line.insert(m.end()-1, ' '*randint(12,14))
                line = ''.join(list_line)


            matches = list(re.finditer(r'\.grid\(\s*row=\w+,', line))[::-1]
            for m in matches:
                list_line.insert(m.end(), ' '*randint(2,14))
                list_line.insert(m.end()-1, ' '*randint(4,5))
                line = ''.join(list_line)

            #matches = re.finditer(r'\.grid\(row=', line)
            #for m in matches:
            #    list_line.insert(m.end(), ' '*randint(2,14))
            #    list_line.insert(m.end()-1, ' '*randint(2,14))
            #    list_line.insert(m.end()-4, ' '*randint(2,14))
            #    line = ''.join(list_line)


            matches = list(re.finditer(r'if \w+', line))[::-1]
            for m in matches:
                list_line.insert(m.end(), ' '*randint(4,7))
                list_line.insert(m.start()+2, ' '*randint(4,5))
                line = ''.join(list_line)



            matches = list(re.finditer(r'= Label\(', line))[::-1]
            for m in matches:
                list_line.insert(m.end()-7, ' '*randint(4,5))
                line = ''.join(list_line)

            #matches = re.finditer(r'\w+\s*= self\.', line)
            #for m in matches:
            #    list_line.insert(m.end(), ' '*randint(4,5))
            #    list_line.insert(m.end()-6, ' '*randint(4,5))
            #    list_line.insert(m.end()-7, ' '*randint(4,6))
            #    line = ''.join(list_line)

            NEW.append(line)



        file.seek(0)
        file.write(''.join(NEW))
        file.close()



#do_file('mainProgram.txt')
#remove_spaces('mainProgram.txt')
add_random_spaces('mainProgram.txt')



exit()
# Copy to desktop
from shutil import copyfile
copyfile('C:\\Users\\sebastian\\PycharmProjects\\xlsxBot\\mainProgram.txt',
         'C:\\Users\\sebastian\\desktop\\mainProgram.py')













