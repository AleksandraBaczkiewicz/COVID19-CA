import numpy as np
import random


class Individual:

    def __init__(self, coordinates, age, ill, **kwargs):
        """ Konstruktor
        :param coordinates: Lista koordynatów osobnika w tablicy stanów [x, y]
        :param age: Wiek osobnika (int)
        :param ill: Wartość odpowiadająca za chorobę osobnika (bool)
        :key res: Wartość odpowiadająca za odporność osobnika (bool)
        :key dead: Wartość odpowiadająca za śmierć osobnika (bool)
        :key days_res: Dni w stanie odporności (int)
        :key days_ill: Dni w stanie choroby (int)
        :key state: Stan osobnika [-1, 1] (int)
        :key direction: Kierunek ruchu osobnika (int):
            - jeżeli 1 to w prawo
            - jeżeli 2 to w lewo
            - jęzeli 3 to w górę
            - jeżeli 4 to w dół
        :key diseases: Choroby współistniejące
        """

        self.coords = coordinates
        self.days = {'rest': kwargs.get('days_res', 0),
                     'ill': kwargs.get('days_ill', 0)}
        self.ill = ill
        self.res = kwargs.get('res', False)
        self.dead = kwargs.get('dead', False)
        self.direction = kwargs.get('direction', np.random.randint(1, 5))
        self.diseases = kwargs.get('diseases', np.random.randint(0, 2))

        if not ill:
            self.state = kwargs.get('state', 1.0)
        else:
            self.state = -1.0
        self.age = age

        # W przypadku gdy osobnika lata mieszczą się w przedziale [5, 35] -> osobnik ma mniejsze prawdopodobieństwo
        # zachorowania, w innym przypadku jest ono większe (wybierane losowo)
        if 35 < age < 5:
            self.p = np.random.uniform(0.5, 0.9)
        else:
            self.p = np.random.uniform(0.01, 0.2)

        self.mortal_age = self.__get_mortal_age(age)

    @staticmethod
    def __get_mortal_age(age):
        if age < 40:
            return 0
        elif 40 <= age < 50:
            return 0.004
        elif 50 <= age < 60:
            return 0.013
        elif 60 <= age < 70:
            return 0.036
        elif 70 <= age < 80:
            return 0.08
        else:
            return 0.148

    def end_res(self):
        """ Metoda kończąca odporność osobnika """

        self.res = False
        self.days['rest'] = 0
        self.state = 1.0

    def end_ill(self):
        """ Metoda kończąca chorobę osobnika"""

        self.ill = False
        self.res = True
        self.days['ill'] = 0
        self.state = 0.7

    def set_ill(self):
        """ Metoda zaczynająca chorobę osobnika """

        self.ill = True
        self.state = -1.0

    def check(self, other):
        """ Metoda sprawdzająca czy osoba jest odporna oraz chora i aktualizująca dni w odporności oraz chorobie"""

        if self.res:
            other.days['rest'] += 1

        if self.ill:
            other.days['ill'] += 1

        # if self.days['ill'] > 3:
        #     other.dead = True
        #     other.state = 0.6

    def get_indices(self):
        """ Metoda zwaracająca krotki indeksów osobnika gdzie:
            x -> (x - 1, x + 1)
            y -> (y - 1, y + 1)
        :return: Dwie krotki indeksów
        """
        x = (self.coords[0] - 1, self.coords[0] + 2)
        y = (self.coords[1] - 1, self.coords[1] + 2)
        return x, y

    def get_environment(self):
        """ Metoda tworząca tablicę koordynatów otoczenia osobnika
        :return: Tablica koordynatów otoczenia osobnika
        """
        environment = np.array([[self.coords[0] - 1, self.coords[1] - 1],
                                [self.coords[0], self.coords[1] - 1],
                                [self.coords[0] + 1, self.coords[1] - 1],
                                [self.coords[0] - 1, self.coords[1]],
                                [self.coords[0], self.coords[1]],
                                [self.coords[0] + 1, self.coords[1]],
                                [self.coords[0] - 1, self.coords[1] + 1],
                                [self.coords[0], self.coords[1] + 1],
                                [self.coords[0] + 1, self.coords[1] + 1]])
        return environment

    def change_direction(self, directions):
        """ Ustawia nowy losowy kierunek przy wykluczeniu listy kierunków directions
        :param directions:
        :return:
        """

        unique = {1, 2, 3, 4}
        directions = set(directions)
        directions = list(unique - directions)

        self.direction = random.choice(directions)

    def predict_coords(self):
        """ Wyznacza koordynaty kolejnego ruchu """

        if self.direction == 1:
            return [self.coords[0] + 1, self.coords[1]]
        if self.direction == 2:
            return [self.coords[0] - 1, self.coords[1]]
        if self.direction == 3:
            return [self.coords[0], self.coords[1] + 1]
        if self.direction == 4:
            return [self.coords[0], self.coords[1] - 1]

    def check_directions(self, size_table):
        """ Zwraca listę niedostępnych dla osobnika kierunków ruchu
        :param size_table: Rozmiar tablicy stanów
        :return:
        """

        directions = []
        if self.coords[0] + 1 == size_table:
            directions.append(1)
        if self.coords[0] - 1 == 0:
            directions.append(2)
        if self.coords[1] + 1 == size_table:
            directions.append(3)
        if self.coords[1] - 1 == 0:
            directions.append(4)

        return directions

    def go(self, x, y):
        """ Metoda zmieniająca koordynaty osobnika """

        self.coords[0] = x
        self.coords[1] = y

    def get_color(self):
        """ Metoda zwracająca kolor osobnika
        :return: Stan osobnika
        """

        return self.state

    def healthy(self):
        """ Metoda zwracająca wartość True gdy osobnik jest zdrowy. W przeciwnym wypadku zwraca wartość False.
        :return: Zdrowotność(?) osobnika
        """

        return not self.res and not self.ill and not self.dead