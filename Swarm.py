from matplotlib import colors
import matplotlib.pyplot as plt
import pandas as pd
import copy
from Individual import Individual
import numpy as np
import random


class Swarm:

    def __init__(self, size, iterations, days_after_rest, days_resistance, perc_population, show_visualisation=False, **kwargs):
        """ Konstruktor
        :param size: Rozmiar tablicy stanów
        :param iterations: Liczba iteracji
        :param days_after_rest: Dni po których osobnik zdrowieje
        :param days_resistance: Dni przez które osobnik jest odporny
        :param perc_population: Procent populacji w danej tablicy stanów
        :key num_of_cities: Liczba miast w tablicy stanów
        :key size_cities: Rozmiar miast w tablicy stanów
        :key perc_lockdown: Procent liczby populacji potrzebnej dla lockdownu w mieście
        :param lockdown_cities: Lista zamkniętych miast
        :key perc_mask: Procent gęstości maski (im większy procent tym mniej osobników w mieście)
        :key perc_out: Prawdopodobieństwo wyjścia z miasta zamkniętego przez osobnika
        """

        self.size = size
        self.iterations = iterations
        self.days_after_rest = days_after_rest
        self.days_resistance = days_resistance
        self.perc_population = perc_population
        self.show_visualisation = show_visualisation
        self.lockdown_cities = []
        self.num_of_cities = kwargs.get('num_of_cities', 15)
        self.size_cities = kwargs.get('size_cities', 20)
        self.perc_lockdown = kwargs.get('perc_lockdown', 0.4)
        self.perc_mask = kwargs.get('perc_mask', 0.7)
        self.perc_out = kwargs.get('perc_out', 0.3)
        self.random_move = kwargs.get('random_move', 0.7)
        self.move_city = kwargs.get('move_city', 0.3)
        print('Sprawdzenie: ', self.move_city)
        numbers = {"Ill": [],
                   "Rest": [],
                   "Dead": [],
                   "Healthy": []}
        self.df = pd.DataFrame(numbers)
        self.n_of_dead = 0

    def __generate_swarm(self):
        """ Tworzy populację osobników dla zadanego rozmiaru i procentu populacji
        :return: Tablica stanów, lista osobników
        """

        # Tworzenie tablicy dla populacji
        # Wektor -> Przemieszanie -> Zmiana na tablicę
        tab = np.zeros(self.size * self.size, dtype = np.float64)
        tab[:int((self.size * self.size) * self.perc_population)] = 1
        np.random.shuffle(tab)
        tab = tab.reshape((self.size, self.size))
        tab = np.pad(tab, ((1, 1), (1, 1)))

        # Tworzenie miast
        # ind_x, ind_y - losowe koordynaty miast dla zadanych rozmiarów i liczby miast
        self.ind_x = random.sample(range(1, self.size - self.size_cities), self.num_of_cities)
        self.ind_y = random.sample(range(1, self.size - self.size_cities), self.num_of_cities)

        # Tworzenie maski
        # Wektor -> Przemieszanie -> Zmiana na tablicę
        mask = np.ones(self.size_cities * self.size_cities, dtype = np.int32)
        mask[:int((self.size_cities * self.size_cities) * self.perc_mask)] = 0
        np.random.shuffle(mask)
        mask = mask.reshape((self.size_cities, self.size_cities))

        # Nakładanie siatki na miasta - random
        for x, y in zip(self.ind_x, self.ind_y):
            tab[x: x + self.size_cities, y: y + self.size_cities] = mask

            # Tutaj była ranodomowa maska
            # tab[x: x + self.size_cities, y: y + self.size_cities] = 1
            # tab[x: x + self.size_cities, y: y + self.size_cities] -= \
            #     np.random.randint(2, size=(x - x + self.size_cities, y - y + self.size_cities))

        # Zebranie inforamcji gdzie znajdują się osobniki
        coords = (tab > 0).nonzero()
        individuals = []
        for x, y in zip(coords[0], coords[1]):
            ill = bool(np.random.randint(0, 2))
            age = np.random.randint(3, 70)
            individuals.append(Individual([x, y], age, -ill))

        return tab, individuals

    def simulation(self):
        """ Metoda przeprowadzająca symulację automatów komórkowych
        :return: Lista posiadająca liczby zdrowych, uodpornionych oraz chorych dla każdej iteracji w symulacji
        """

        tab, individuals = self.__generate_swarm()

        if self.show_visualisation:
            fig, ax = plt.subplots()
            self.__visualisation(0, tab, fig, ax)

        individuals_copy = copy.deepcopy(individuals)
        tab_copy = copy.deepcopy(tab)

        print('Individuals: ', len(individuals))

        

        #tu tu
        for iteration in range(1, self.iterations+1):
            print("_______________________________________")
            print("Iteration:", str(iteration + 1))
            n_of_ill = 0
            n_of_rest = 0
            n_of_healthy = 0

            ###

            for index_individual, (individual, individual_copy) in enumerate(zip(individuals, individuals_copy)):

                # Wykonanie ruchu
                tab_copy = self.check_environment(individual, individual_copy, tab_copy)

                # Indywidualne rzeczy jednostki
                if individual.days['rest'] >= self.days_after_rest and not individual.dead:
                    individual_copy.end_res()

                if individual.days['ill'] >= self.days_resistance and not individual.dead:
                    individual_copy.end_ill()

                individual.check(individual_copy)

                x, y = individual_copy.get_indices()

                suma = np.sum(tab[x[0]: x[1], y[0]: y[1]]) - tab[individual_copy.coords[0], individual_copy.coords[1]]

                if suma > 0 and individual.healthy() and np.random.rand() < individual.p:
                    individual_copy.set_ill()
                    # tab_copy[individual_copy.coords[0], individual_copy.coords[1]] = 0.3

                tab_copy[individual_copy.coords[0], individual_copy.coords[1]] = individual_copy.state

                tab, tab_copy, individuals, individuals_copy = self.__get_dead(tab, tab_copy, individuals,
                                                                               individuals_copy, individual,
                                                                               index_individual)

                # Grupowe rzeczy jednostki

                # Zliczanie grup
                if individual_copy.ill and not individual_copy.dead:
                    n_of_ill += 1

                if individual_copy.res and not individual_copy.dead:
                    n_of_rest += 1

                if not individual_copy.ill and not individual_copy.res and not individual_copy.dead:
                    n_of_healthy += 1

                # Tutaj można zrobić śmierć
                # individuals_copy.pop(index_individual)
                # x, y = individual.coord
                # tab[x, y] = 0

            # Aktualizacja miast

            # Lockdown
            tab_copy = self.__lockdown(tab_copy)

            # dodac na starcie
            # Dodanie liczb statnów osobników do ramki danych
            #tu bylo
            self.df = self.df.append({"Ill": n_of_ill,
                                      "Rest": n_of_rest,
                                      "Dead": self.n_of_dead,
                                      "Healthy": n_of_healthy}, ignore_index = True)

            tab = copy.deepcopy(tab_copy)
            individuals = copy.deepcopy(individuals_copy)

            if self.show_visualisation:
                self.__visualisation(iteration, tab, fig, ax)

            print("Individuals:" + str(np.count_nonzero((tab > 0.2) | (tab < 0))))
            print('Number of rest: ' + str(n_of_rest))
            print('Number of healthy: ' + str(n_of_healthy))
            print('Number of ill: ' + str(n_of_ill))
            print('Number of dead: ' + str(self.n_of_dead))
            print('Number of lockdown cities: ' + str(len(self.lockdown_cities)))
            print("_______________________________________")

        if self.show_visualisation:
            plt.show()

        return self.df

    def __get_dead(self, tab, tab_copy, individuals, individuals_copy, individual, index_individual):

        sum_mortal = 0
        if individual.diseases:
            sum_mortal += 0.002  # zwiekszenie prawdopodobienstwa smierci z powodu chorob wspolistniejacych
        sum_mortal += 0.0165  # prawdopodobienstwo smierci z powodu komplikacji
        sum_mortal += individual.mortal_age

        if sum_mortal > np.random.rand() and individual.ill:
            x, y = individual.coords
            tab[x, y] = 0
            tab_copy[x, y] = 0
            individuals_copy.pop(index_individual)  # index_individual copy powinien byc - sprawdzic
            individuals.pop(index_individual)
            self.n_of_dead += 1

        return tab, tab_copy, individuals, individuals_copy

    def check_environment(self, individual, individual_copy, tab):
        """ Metoda, dzięki której osobnik wykonuje ruch
        :param individual: Osobnik
        :param individual_copy: Kopia osobnika
        :param tab: Tablica stanów
        :return: Tablica stanów z uaktualnioną pozycją osobnika
        """

        x_individual, y_individual = individual.coords

        # move - czy wykona ruch czy będzie stał
        move_out = True
        # Przechodzimy po indeksach zamkniętych miast
        for coords in self.lockdown_cities:
            x = coords[0]
            y = coords[1]
            # Gdy osobnik znajduje się w zamkniętym mieście to flaga się zmienia i nie wykonuje ruchu
            if x < x_individual <= x + self.size_cities and y < y_individual < y + self.size_cities:
                move_out = False
                break

        # Sprawdzanie czy może wyjść z zamkniętego miasta
        if move_out or random.random() < self.perc_out:
            # Sprawdzanie czy może iść w kierunku jaki ma aktualnie
            directions = individual.check_directions(self.size + 1)

            if individual.direction in directions or random.random() > self.random_move:
                individual.change_direction(directions)

            x_new, y_new = individual.predict_coords()

            move_in = True

            for coords in self.lockdown_cities:
                x = coords[0]
                y = coords[1]
                # Gdy osobnik chce wejść do zamkniętego miasta to flaga się zmienia i nie wykonuje ruchu
                if x == x_new or x + self.size_cities == x_new or y + self.size_cities == y_new or y == y_new:
                    move_in = False
                    break

            if move_in or np.random.random() < self.move_city:

                if tab[x_new, y_new] == 0.2 or tab[x_new, y_new] == 0.0:

                    tab[x_individual, y_individual] = 0
                    individual_copy.go(x_new, y_new)
                    tab[x_new, y_new] = individual.get_color()
        return tab

    def __lockdown(self, tab):
        """ Metoda do lockdownu w miastach od zadanego procentu """

        self.lockdown_cities = []

        # Przechodzimy po indeksach miast - x, y
        for x, y in zip(self.ind_x, self.ind_y):
            illness = 0
            # Przechodzimy po mieście - tab_x, tab_y
            city = tab[x: x + self.size_cities, y: y + self.size_cities]
            for tab_x in range(city.shape[0]):
                for tab_y in range(city.shape[1]):
                    # Dodajemy x oraz y żeby miasto było prawidłowe, ponieważ inaczej byłoby np. tab_x = 0 jako pierwszy
                    # indeks
                    if tab[tab_x + x, tab_y + y] == -1.0:
                        illness += 1
            if illness / self.size_cities > self.perc_lockdown:
                self.lockdown_cities.append((x, y))
                # Ustawianie na kolor żółty komórek pustych gdy jest lockdown
                city_tmp = tab[x: x + self.size_cities, y: y + self.size_cities]
                city_tmp = np.where(city_tmp != 0.0, city_tmp, 0.2)
                tab[x: x + self.size_cities, y: y + self.size_cities] = city_tmp
            else:
                # Ustawianie na kolor biały komórek pustych gdy nie ma lockdownu
                city_tmp = tab[x: x + self.size_cities, y: y + self.size_cities]
                city_tmp = np.where(city_tmp != 0.2, city_tmp, 0.0)
                tab[x: x + self.size_cities, y: y + self.size_cities] = city_tmp

        return tab

    @staticmethod
    def __visualisation(iteration, tab, fig, ax):
        """ Wizualizuje tablicę stanów oraz zapisuje ją do pliku '.png'. Wizualizacja odbywa się według kolorów:
            * [od 0 do 0.2) - biały
            * [od 0.2 do 0.4) - czerwony
            * [od 0.4 do 0.6) - niebieski
            * [od 0.6 do 0.8) - czarny
            * [od 0.8 do 1) - zielony
        :param iteration: Liczba iteracji
        :param tab: Tablica stanu
        """

        cmap = colors.ListedColormap(['red', 'white', 'yellow', 'blue', 'green'])
        bounds = [-1, 0, 0.15, 0.2, 0.8, 1]
        norm = colors.BoundaryNorm(bounds, cmap.N)
        im = ax.imshow(tab, cmap = cmap, norm = norm)
        if iteration == 0:
            fig.colorbar(im, ax = ax)
        ax.set_title('Iteration: ' + str(iteration))
        #plt.savefig('./data/' + str(iteration) + '.png')
        plt.pause(0.001)
        # plt.clf()