import time
from random import randint
from time import sleep


class BoardExeptions(Exception):
    pass

class BoardOutException(BoardExeptions):
    def __str__(self):
        return 'Вы ходите за пределы поля!'

class RepeatTurnExeption(BoardExeptions):
    def __str__(self):
        return 'Вы уже ходили в эту точку!'

class BoardWrongShipException(BoardExeptions):
    pass



class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'({self.x}, {self.y})'


class Ship:
    def __init__(self, lens, dot, rotate):
        self.lens = lens
        self.dot = dot
        self.rotate = rotate
        self.live = lens

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.lens):
            current_x = self.dot.x
            current_y = self.dot.y

            if self.rotate == 0:
                current_x += i

            elif self.rotate == 1:
                current_y += i

            ship_dots.append(Dot(current_x, current_y))
        return ship_dots



class Board:

    def __init__(self, hid=False):
        self.hid = hid

        self.count = 0
        self.board = [['0' for i in range(6)] for i in range(6)]

        self.ships = []
        self.alive = []

    def add_ship(self, ship):
        for d in ship.dots:
            if self.out(d) or d in self.alive:
                raise BoardWrongShipException

        for d in ship.dots:
            self.board[d.x][d.y] = "■"
            self.alive.append(d)

        self.ships.append(ship)
        self.contur(ship)

    def contur(self, ship, cntr=False):
        near = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]

        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and not cur in self.alive:
                    if cntr:
                        self.board[cur.x][cur.y] = '-'
                    self.alive.append(cur)

    def __str__(self):
        pole = ' | '.join([str(1 * n) for n in range(0, 7)]) + " |"
        for i, e in enumerate(self.board):
            pole += f"\n{i +1} | " + " | ".join(e) + " |"
        return pole

        if self.hid:
            pole = pole.replace('■', '0')
        return pole

    def out(self, d):
        return not ((0 <= d.x < 6) and (0 <= d.y < 6))

    def shot(self, d):
        if self.out(d):
            raise BoardOutException

        if d in self.alive:
            raise RepeatTurnExeption

        self.alive.append(d)

        for ship in self.ships:
            if d in ship.dots:
                ship.live -= 1
                self.board[d.x][d.y] = 'X'
                if ship.live == 0:
                    self.count += 1
                    self.contur(ship, cntr=True)
                    print('Уничтожен!')
                    return True
                else:
                    print('Ранен!')
                    return True

        self.board[d.x][d.y] = '-'
        print('Промазал!')
        return False

    def begin(self):
        self.alive = []

class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        pass

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardExeptions as e:
                print(e)

class AI(Player):
    def ask(self):
        d = Dot(randint(0,5), randint(0,5))
        print(f'AI ходит: {d.x+1} {d.y+1}')
        return d


class User(Player):
    def ask(self):
        while True:
            result = input('Введите координаты выстрела (строка столбец): ').split()
            if len(result) < 2:
                print('Введите через пробел!')
                continue

            if not ''.join(result).isdigit():
                print('Используйте только цифры!')
                continue

            x = int(result[0]) - 1
            y = int(result[1]) - 1
            return Dot(x, y)

class Game:
    def __init__(self):
        user = self.board_gen()
        ai = self.board_gen()
        ai.hid = True

        self.ai = AI(ai, user)
        self.user = User(user, ai)


    def board_gen(self):
        ships = [3, 2, 2, 1, 1, 1]
        board = Board()
        for l in ships:
            while True:
                ship = Ship(l, Dot(randint(0, 5), randint(0, 5)), randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def greet(self):
        print('Это мини версия игры морской бой!')
        print('Ходить нужно в формате x, y')
        print('где x - строка')
        print('а у - столбец')

    def process(self):
        turn = 0
        while True:
            print('Поле игрока: ')
            print(self.user.board)
            time.sleep(2)
            print('Поле ИИ:')
            print(self.ai.board)
            time.sleep(2)
            if turn % 2 == 0:
                print('Ходит игрок: ')
                repeat = self.user.move()
                time.sleep(2)
            else:
                print('Ходит ИИ: ')
                repeat = self.ai.move()
                time.sleep(2)
            if repeat:
                turn -= 1

            if self.user.board.count == 6:
                print('Игрок проиграл! Победа ИИ!')
                print('Поле игрока:')
                print(self.user.board)
                self.ai.board.hid = False
                print('Поле ИИ:')
                print(self.ai.board)
                break

            if self.ai.board.count == 6:
                print('Игрок выиграл ИИ!')
                print('Поле игрока:')
                print(self.user.board)
                self.ai.board.hid = False
                print('Поле ИИ:')
                print(self.ai.board)
                break
            turn += 1

    def start(self):
        self.greet()
        self.process()



g = Game()
g.start()
