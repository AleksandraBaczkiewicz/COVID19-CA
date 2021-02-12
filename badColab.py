import matplotlib.pyplot as plt
from Swarm import Swarm
import numpy as np
# import os

# dorobić osobnika zabitego i tylko zarażającego
# zdrowienie zależne od wieku
# dodać choroby współistniejące


def visualize_simulation(numbers, T, name='wykres'):

    plt.style.use('seaborn')

    for column in numbers.columns:

        plt.plot(numbers[column], label = column)

    plt.xlim(1, T)
    plt.xlabel('Iterations', fontsize=16)
    plt.ylabel('Individuals', fontsize=16)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.legend(fontsize=16, loc='center right')
    plt.title('Individuals by number of iteration', fontsize=16)
    plt.savefig(name + '.pdf')
    plt.show()


if __name__ == '__main__':
    aa = 360 #odpornosc - dni w stanie odpornosci
    bb = 10 #zdrowienie - dni w stanie choroby
    T = 20
    m = 100
    #pop = 0.005
    pop = 0.005

    params = {
        'num_of_cities': 20,
        'size_cities': 20,
        'perc_lockdown': 0.4, #0.4
        'perc_mask': 0.7,
        'perc_out': 0.9, #
        'random_move': 0.7, 
        'move_city': 0.3 #ku
    }

    # os.mkdir('./data')

    num = 100
    tablica = np.zeros((num, 4))

    
    for iters in range(num):
        size_cities = 20
        #for percent_out in [0.2, 0.4, 0.6, 0.8]:
        #for percent_mask in [0.2, 0.4, 0.6, 0.8]:
        for col, perclockdown in enumerate([0.2, 0.4, 0.6, 0.8]):
            #powtarzamy w automacie

            #tu zmieniamy
            params = {
                'num_of_cities': 15,
                'size_cities': size_cities,
                'perc_lockdown': perclockdown, #Kuba
                'perc_mask': 0.7,#percent_mask,#percent_mask, #Ola 0.7
                'perc_out': 0.5,#percent_out, ##prawdopodobienstwo wyjscia z zamknietego miasta #Ola 0.5
                'random_move': 0.7, #Kuba
                'move_city': 0.3#movecity#movecity#0.3 #Ola
            }

            automat = Swarm(m, 100, aa, bb, pop, show_visualisation=False, **params) #True
            numbers = automat.simulation()
            print(numbers)
            tablica[iters, col] = numbers.iloc[-1, 3]

    np.savetxt('perlockdown.txt', tablica)
            
