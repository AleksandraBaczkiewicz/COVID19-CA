import matplotlib.pyplot as plt
from Swarm import Swarm
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

    Ill_list = []
    Rest_list = []
    Dead_list = []
    Healthy_list = []
    labele_list = []

    for iteration in [100]: #50
        #for size_cities in [10, 15, 20]:
        #for size_cities in [20]:
        size_cities = 20
        #for percent_out in [0.2, 0.4, 0.6, 0.8]:
        #for percent_mask in [0.2, 0.4, 0.6, 0.8]:
        #for percent_mask in [0.5]:
        #for movecity in [0.2, 0.4, 0.6, 0.8]:
        for rm in [0.2, 0.4, 0.6, 0.8]:

            #tu zmieniamy
            params = {
                'num_of_cities': 15,
                'size_cities': size_cities,
                'perc_lockdown': 0.4, #Kuba
                'perc_mask': 0.7,#percent_mask,#percent_mask, #Ola 0.7
                'perc_out': 0.5,#percent_out, ##prawdopodobienstwo wyjscia z zamknietego miasta #Ola 0.5
                'random_move': rm, #Kuba0.7
                'move_city':0.3#movecity#0.3 #Ola
            }

            automat = Swarm(m, iteration, aa, bb, pop, show_visualisation=False, **params) #True
            numbers = automat.simulation()
            print(numbers)
            Ill_list.append(numbers.iloc[:, 0])
            Rest_list.append(numbers.iloc[:, 1])
            Dead_list.append(numbers.iloc[:, 2])
            Healthy_list.append(numbers.iloc[:, 3])


            #labele_list.append(str(params['perc_out']))
            #labele_list.append(str(params['perc_mask']))
            #labele_list.append(str(params['move_city']))
            labele_list.append(str(params['random_move']))
            visualize_simulation(numbers, iteration, 'iter_' + str(iteration) + '_size_cities_' + str(size_cities))

    #Ill
    for i in range(len(Ill_list)):
        plt.plot(Ill_list[i], label = labele_list[i])
    plt.xlabel('Iterations', fontsize=16)
    plt.ylabel('Individuals', fontsize=16)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.legend(fontsize=14)
    #plt.title('Ill' + ' perc_out = ' + str(params['perc_out']))
    plt.title('Ill', fontsize=16)
    plt.show()

    #Rest
    for i in range(len(Rest_list)):
        plt.plot(Rest_list[i], label = labele_list[i])
    plt.xlabel('Iterations', fontsize=16)
    plt.ylabel('Individuals', fontsize=16)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.legend(fontsize=14)
    #plt.title('Rest' + ' perc_out = ' + str(params['perc_out']))
    plt.title('Rest', fontsize=16)
    plt.show()

    for i in range(len(Dead_list)):
        plt.plot(Dead_list[i], label = labele_list[i])
    plt.xlabel('Iterations', fontsize=16)
    plt.ylabel('Individuals', fontsize=16)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.legend(fontsize=14)
    #plt.title('Dead' + ' perc_out = ' + str(params['perc_out']))
    plt.title('Dead', fontsize=16)
    plt.show()

    for i in range(len(Healthy_list)):
        plt.plot(Healthy_list[i], label = labele_list[i])
    plt.xlabel('Iterations', fontsize=16)
    plt.ylabel('Individuals', fontsize=16)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.legend(fontsize=14)
    #plt.title('Healthy' + ' perc_out = ' + str(params['perc_out']))
    plt.title('Healthy', fontsize=16)
    plt.show()
