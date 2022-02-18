import pandas as pd
from matplotlib.colors import Colormap
import matplotlib.pyplot as plt
import io
from flask import Response
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

graphFolder = "src/data/"
def plotChamps(username):
    global graphFolder
    try: data = pd.read_hdf(graphFolder+username+'.h5', 'df')
    except FileNotFoundError: 
        return f"{username} not found in database, visitvm-148-12.ise.luddy.indiana.edu:11000/fetchData/{username} and wait for confirmation"
    dic = {}
    nGames = []

    # fig, ax = plt.subplots()

    fig = Figure(figsize=((20,10)))
    ax = fig.add_subplot(1,1,1)
    # for champ in data['Champion'].unique():
    #     nGames.append([nGames[champ], df.loc[df['Champion'] == 'Xerath']['Games Played'].sum()])
    # print(nGames)
    # dfGames = pd.DataFrame(nGames)
    for champ in data.loc[data['Games Played'] >= 15]['Champion'].unique():
        # x,y = [],[]
        d = data.loc[data['Champion'] == champ]
        # print(champ)
        try: len(dic[champ])
        except: dic[champ] = []
        for i in sorted(data['Season'].unique()):
            # x.append(i)
            if d.loc[d['Season'] == i].empty:
                dic[champ].append(0)
            else:
                dic[champ].append(d.loc[d['Season'] == i]['Games Played'].values[0])
        # print(champ)

    # tGames = [[],[]]
    seasons = []
    for i in data['Season'].unique():
        seasons.append(i)
    #     dic['Total Games'] = data.loc[data['Season'] == i]['Games Played'].sum()
        
    # ax.stackplot(tGames[0],tGames[1], label='Total Games', alpha=.5, linewidth=3)
    # print(seasons, dic)
    ax.stackplot(seasons, dic.values(), labels=dic.keys(), alpha=0.8)
    ax.legend(loc='upper left')
    ax.set_title(username+' Champion Games per Season')
    ax.set_xlabel('Season')
    ax.set_ylabel('Ranked Games Played')

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    plt.savefig(graphFolder+username+'.pdf')
    return Response(output.getvalue(), mimetype='image/png')

def plotGames(userList):
    global graphFolder
    for user in userList:
        tGames = [[],[]]
        data = pd.read_hdf(graphFolder+user+'.h5', 'df')
        for i in data['Season'].unique():
            tGames[0].append(i)
            tGames[1].append(data.loc[data['Season'] == i]['Games Played'].sum())
        plt.plot(tGames[0],tGames[1], label=user, alpha=.5, linewidth=3)

    plt.xlabel('Season')
    plt.ylabel('Ranked Games Played')
    plt.legend(loc='best')
    plt.show()

def plotCS(username):
    global graphFolder
    data = pd.read_hdf(graphFolder+username+'.h5', 'df')
    for champ in data.loc[data['Games Played'] >= 10]['Champion'].unique():
        d = data.loc[data['Champion'] == champ]
        plt.plot(d['Season'].values,d['CS/m'].values, label=champ, alpha=.5, linewidth=3)

    plt.xlabel('Season')
    plt.ylabel('CS/M')
    plt.legend(loc='best')
    plt.show()

iu = ['CyborgSteve', 'D3f3ctive', 'Kevalon', 'AmericanHussar', 'co1iflower', '10slayer', 'MrLDS', 'YourLocalThicc', 'NiabiIsHere', 'Wulfph']
ugglee = ['forlorn64', 'chrismonytf', 'parad0x05', '9wonwon', 'jonbom', 'junpi', 'aurumrock', 'hipbo', 'theristis', 'cocheese01', 'minibatman', 'nickizer534', ]
tfec = ['elfsuf','coolwhip420', 'nraddlygew', 'sekou', 'stealthinator', 'emended', 'xerelic', 'poweredbyrice', 'duckyduckplaysmc', 'meteoryte']