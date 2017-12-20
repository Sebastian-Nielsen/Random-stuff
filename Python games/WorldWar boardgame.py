row = list(range(16))
info = 'A0 B1 C2 D3 E4 F5 G6 H7 I8 J9 K10 L11 M12 N13 O14 P15'
col = '   0 1  2 3  4 5  6 7  8 9  0 1  2 3  4 5 '
col2 = '   0 1  2 3  4 5  6 7  8 9  0 1  2 3  4 5 '
letters = '   A B  C D  E F  G H  I J  K L  M N  O P'
bogstaver = ['A','B','C','D','E','F','G','H','J','K','L','M','N','O','P']
pieceInfo = {
    'worker': "Worker(B/D)  -  cost: 50\nmove: 1 felt i hver retning\nSpecial: Kan skaffe guld",
    'soldier': "Soldier(x/o)  -  cost: 75\nmove: 1 felt i hver retning",
    'officer': "Officer(2/4)  -  cost:  100\nmove: 1 felt lodret alle vandret"
          }
bricks = '♛♕♛♙♟♚♔♖♜♗♝♘♞🀩🖽🀆⚄🂼☠♢♡♤♣'
pieces = {
    'worker': '♟', 'blackworker': '♙',
    'soldier': '🀩', 'blacksoldier': '🂼',
    'officer': '♡', 'blackofficer': '♣',
    'tårn': '♜', 'blacktårn': '♖'
    }


class Game():
    def __init__(self):
        self.grid = [['▢']*16 for i in range(16)]
        self.turn = True
        self.gold1 = 200
        self.gold2 = 200

        self.CreateTerrain()

    def Info(self, piece='Default'):
        """Prints information about the different pieces"""
        line = '_'*30
        print(line)

        if piece =='Default':
            for key in pieceInfo:
                print(pieceInfo[key])
                print(line)
        else:
            try:
                if turn:
                    print(pieceInfo[piece])
                else:
                    print(pieceInfo['black'+piece])
            except:
                print('No such piece')

    def PrintBoard(self):
        """Prints the board"""
        print(col)
        for j,k in zip(row, self.grid):
            if j < 10:
                print(j, ' ' + ' '.join(k), j)
            else:
                print(j, ' '.join(k), j)
        print(col)

    def CreateTerrain(self):
        """Builds the terrain on the board"""
        terrain = []
        bricks = [
            '◾','◽','▦','▩','▨','▧','▦','▥',\
            '▤','▣','▭','▮','▯','▢' ]

        brick = '▦'
        gold  = '♨'
        spawn = '◼'
        print(16*16)

        # 2 vandret vægge row: 5 & 10
        for i in range(1,2):
            terrain.append([5,i+13, brick])
            terrain.append([10,i, brick])

        # 2 lodret vægge col: 3 & 1
        for i in range(3,5):
            terrain.append([i,10, brick])
            terrain.append([i+8,5, brick])

        # Base-Guldminer row: 3 & 12
        for i in range(2,5):
            terrain.append([11,i, gold])
            terrain.append([4, i+9, gold])
        # Små-Guldminger
        terrain.append([2,0, gold])
        terrain.append([13,15, gold])

        # Main Spawn
        for i in range(0,6):
            terrain.append([15,i, spawn])
            terrain.append([0,i+10, spawn])
        for i in range(0,5):
            terrain.append([14,i, spawn])
            terrain.append([1,i+11, spawn])
        # Secondary Spawn
        """for j in range(2,4):
            for k in range(3,5):
                terrain.append([j,k, spawn])
                terrain.append([j+10,k+8, spawn])"""

        # Places the bricks on the board
        for i in terrain:
            del self.grid[i[0]][i[1]]
            self.grid[i[0]].insert(i[1], i[2])

    def PrintTurn(self):
        if self.turn:
            print(" ¤¤ It's white's turn ¤¤ ")
            print('|/' + '~'*22 + '\|')
        else:
            print(" ¤¤ It's black's turn ¤¤ ")
            print('|/' + '~' * 22 + '\|')

    def SpawnPiece(self):
        """Spawns pieces"""
        self.PrintBoard()
        game1.Info()
        self.PrintTurn()


        # try:
        piece = input('Type the piece you want to spawn: ').lower()

        spawn1, spawn2 = map(int, input('Type the coordinates: ').split(' '))
        punkt = self.grid[spawn1][spawn2]

        if self.turn:  # If white's turn
            if punkt == '◼' and spawn1 > 6:
                del self.grid[spawn1][spawn2]
                self.grid[spawn1].insert(spawn2, pieces[piece])
                self.turn = False

        else:  # If black's turn
            if punkt == '◼' and spawn1 < 6:
                del self.grid[spawn1][spawn2]
                self.grid[spawn1].insert(spawn2, pieces['black' + piece])
                self.turn = True

            #except:




        """
        if piece == '?':
            Info()
        elif piece == 'worker':pass

        """
        self.PrintBoard()

    def MovePiece(self):
        """Moves a piece"""
        self.PrintTurn()
        self.Info()




game1 = Game()

while True:
    game1.SpawnPiece()
    game1.SpawnPiece()
    game1.MovePiece()
    game1.MovePiece()
