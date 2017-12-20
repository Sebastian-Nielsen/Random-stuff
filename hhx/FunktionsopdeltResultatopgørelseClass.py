from settings import *
import time
import openpyxl



class Funktionsopdelt_ResultatopgørelseClass():
    def __init__(self, FileToLoad, SaveLocation, saldobalance, StartSaldoRow, EndSaldoRow):

        #variables
        self.SaveLocation = SaveLocation
        self.saldobalance = saldobalance
        self.StartSaldoRow = StartSaldoRow
        self.EndSaldoRow = EndSaldoRow

        # Data
        self.wb = openpyxl.load_workbook(FileToLoad)
        self.debet, self.kredit = self.GetDataFromWB()

        # Lav skabelon og add data til skabelon
        self.CreateFROskabelon()
        self.AddDataToFROskabalon()

    def TimeIt_decorator(function):
        """Decorator to time functions"""

        def wrapper(*args, **kwargs):
            T = time.time()
            x = function(*args, **kwargs)
            print('Running: {}\nTime taken: {}'.format(function.__name__, time.time() - T))
            return x
        return wrapper

    @TimeIt_decorator
    def GetDataFromWB(self):
        """Gets data from workbook - saldobalance"""
        saldo = self.wb.get_sheet_by_name(self.saldobalance)

        kredit = []
        debet = []

        for i in range(self.StartSaldoRow, self.EndSaldoRow):
            if saldo['C' + str(i)].value == None:
                kredit.append([saldo['A' + str(i)].value,
                               saldo['B' + str(i)].value,
                               saldo['D' + str(i)].value,
                               saldo['D' + str(i)].coordinate])
            else:
                debet.append([saldo['A' + str(i)].value,
                              saldo['B' + str(i)].value,
                              saldo['C' + str(i)].value,
                              saldo['C' + str(i)].coordinate])

        return debet, kredit


    def CreateFROskabelon(self, row=3, title='Funktionsopd. Resultatopgørelse'):
        """row= placering af resultatopgørelsen i det ny sheet"""
        headlines = ['Nettoomsætning', 'Produktionsomkostninger', 'Bruttofortjeneste',
                     'Distributionsomkostninger', 'Administrationsomkostninger',
                     'Resultat før primær drift', 'Finansielle indtægter', 'Finansielle omkostninger',
                     'Resultat før skat', 'Skat', 'Årets resultat']
        noter = ['Produktionsomkostninger',
                 'Distributionsomkostninger',
                 'Administartionsomkostninger']

        # Lav ny "sheet" og gå ind på den
        self.wb.create_sheet(title=title, index=0)
        self.doc = self.wb.get_sheet_by_name(title)

        # Overskrift
        self.doc['A1'] = 'Funktionsopdelt Resultatsopgørelse'
        self.doc['A1'].font = bold22Font

        self.Ialt = []
        L = len(headlines)  # 11

        # Lav resultatopgørelse skabelon
        for i in range(0, L):
            self.doc['A' + str(row + i)] = headlines[i]

            if headlines[i] in ['Bruttofortjeneste',
                                'Resultat før primær drift',
                                'Resultat før skat',
                                'Årets resultat']:
                self.doc['A' + str(row + i)].font = bold10
            else:
                temp = 'C' + str(row + i)

                if i == 1:
                    self.doc[temp] = 1
                elif i == 3:
                    self.doc[temp] = 2
                elif i == 4:
                    self.doc[temp] = 3

        # Add mellemrum
        self.doc['A' + str(row + L)] = ''
        self.doc['B' + str(row + L)] = ''

        # Været igennem alle 11 fra headlines, vi startede fra row 3.    14
        # + 1 da vi addede et mellemrum.   Derfor: 15
        currentIndex = L + row + 1
        startIndex = L + row + 2

        self.PrintKontis()
        note = 0
        while True:

            self.doc['A' + str(currentIndex)] = 'Note {} - {}'.format(note + 1, noter[note])
            self.doc['A' + str(currentIndex)].font = bold10

            # Append til note 1
            if note == 0:
                for konto in self.debet:
                    if 2000 <= konto[0] < 3000:
                        currentIndex += 1
                        self.doc.append([konto[1], konto[2]])

            elif note == 1:
                for konto in self.debet:
                    if 3000 <= konto[0] < 4000:
                        currentIndex += 1
                        self.doc.append([konto[1], konto[2]])

            elif note == 2:
                for konto in self.debet:
                    if 4000 <= konto[0] < 5000:
                        currentIndex += 1
                        self.doc.append([konto[1], konto[2]])

            # add sum af alle tal i noten
            currentIndex += 1
            print(currentIndex, startIndex)
            self.doc['A' + str(currentIndex)] = noter[note] + ' i alt'
            self.doc['B' + str(currentIndex)] = '=SUM(B{}:B{})'.format(startIndex, currentIndex - 1)

            # add underline under sum af note
            self.doc['A' + str(currentIndex)].font = underline10
            self.doc['B' + str(currentIndex)].font = underline10

            # TEST FARVE - når internet igen
            # testFont = Font(color='red')
            # doc['C3:D8'].font = testFont

            self.Ialt.append(currentIndex)

            print('self.ialt:', self.Ialt)
            note += 1
            startIndex = currentIndex + 2
            currentIndex += 1

            if note == 3:
                return

    def AddDataToFROskabalon(self, row=3):

        # formel for "netto omsætning"
        formula = '='
        for konto in self.kredit:
            if konto[0] < 1200:
                formula += '+' + self.saldobalance + '!' + konto[3]

        print(formula)
        self.doc['B' + str(row)] = formula

        # Add til "produktionsomkostninger
        row += 1
        self.doc['B' + str(row)] = "=B{}".format(self.Ialt[0])
        # Bruttofortjeneste
        row += 1
        self.doc['B' + str(row)] = "=B{}-B{}".format(row - 2, row - 1)
        # Distributionsomkostninger
        row += 1
        self.doc['B' + str(row)] = "=B{}".format(self.Ialt[1])
        # Administrationsomkostninger
        row += 1
        self.doc['B' + str(row)] = "=B{}".format(self.Ialt[2])
        # Resultat før primær drift
        row += 1
        self.doc['B' + str(row)] = "=B{}-B{}-B{}".format(row - 3, row - 2, row - 1)
        # Finansielle indtægter
        row += 1
        formula = '='

        for konto in self.kredit:
            if 5999 < konto[0] < 7000:
                formula += '+' + self.saldobalance + '!' + konto[3]

        if formula == '=':
            self.doc['B' + str(row)] = 0
        else:
            self.doc['B' + str(row)] = formula

        # Finansielle omkostninger
        row += 1
        formula = '='

        for konto in self.debet:
            if 6999 < konto[0] < 8000:
                formula += '+' + self.saldobalance + '!' + konto[3]

        if formula == '=':
            self.doc['B' + str(row)] = 0
        else:
            self.doc['B' + str(row)] = formula

        # Resultat før skat
        row += 1
        self.doc['B' + str(row)] = "=B{}+B{}-B{}".format(row - 3, row - 2, row - 1)

        # Skat
        row += 1
        formula = '='

        for konto in self.debet:
            if 7999 < konto[0] < 9000:
                formula += '+' + self.saldobalance + '!' + konto[3]

        if formula == '=':
            self.doc['B' + str(row)] = 0
        else:
            self.doc['B' + str(row)] = formula

        # Årets resultat
        row += 1
        self.doc['B' + str(row)] = "=B{}-B{}".format(row - 2, row - 1)

        self.doc.column_dimensions['A'].width = 40
        self.wb.save(SaveLocation)

    def PrintKontis(self):
        """Prints the data collected from: Debet and Kredit"""
        line = '_' * 30

        print(line)
        for i in self.debet:
            print('Debet:', i)
        print(line)
        for i in self.kredit:
            print('Kredit:', i)
        print(line)




if __name__ == '__main__':

    # arguments is taken from settings.py

    from Funktionsopdelt_resultatopgørelse import *


    status = Funktionsopdelt_resultatopgørelse(
        FileToLoad=FileToLoad, SaveLocation=SaveLocation, saldobalance=saldobalance,
        StartSaldoRow=StartSaldoRow, EndSaldoRow=EndSaldoRow)

    print('_'*25)
    if status:
        print('seems like an error had accured:')
        print(status)
    else:
        print('no error status was:', status)


def Varesalg():
    for rowOfCellObjects in tuple(saldo['B6:D8']):
        for cellObj in rowOfCellObjects:

            if list(cellObj.coordinate)[0] != 'C':
                print(cellObj.value)
        print()