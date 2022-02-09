from flask import Flask, jsonify, render_template, request
import connexion

# fetchData
import re
from timeit import default_timer as timer
import os
import pandas as pd
import urllib.request
from pprint import pprint
from html_table_parser.parser import HTMLTableParser

# graph
import pandas as pd
from matplotlib.colors import Colormap
import matplotlib.pyplot as plt
import io
from flask import Response
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


# Create the application instance
app = connexion.App(__name__, specification_dir="./")

# Read the yaml file to configure the endpoints
app.add_api("master.yml")

# create a URL route in our application for "/"
@app.route("/")
def home():
    return render_template("test.html", mimetype = 'text/html')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text'].lower()
    if not os.path.exists(f'src/data/{text}.h5'):
        makeData(text)
    return plotChamps(text)
    # return render_template("test.html", user_image = plotChamps(text), mimetype = 'text/html')


folder = "src/data/"
def getSeason(summID=53840413, seasonID=17, username='xerelic', debug=False):

    sTrans = {1:1, 2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 11:8, 13:9, 15:10, 17:11, 19:12}
    if debug: print(f'fetching {username} season', sTrans[seasonID])
    link = 'https://na.op.gg/summoner/champions/ajax/champions.rank/summonerId='+str(summID)+'&season='+str(seasonID)
    # print(link)
    req = urllib.request.Request(url=link)

    f = urllib.request.urlopen(req)
    raw = f.read().decode('utf-8')
    # print(raw)
    p = HTMLTableParser()
    p.feed(raw)
    
    if not p.tables:
        return None
            # 0            1                2       3          4        5       6       7           8       9       10
        # ["Season", "Champion", "Games Played", "Wins", "Losses", "Winrate", "Kills", "Deaths", "Assists", "Gold", "CS/m"]
    # '#','Champion','Played','KDA','Gold','CS','Max Kills', 'Max Deaths','Average Damage Dealt','Average Damage Taken','Double Kill','Triple Kill','Quadra Kill','Penta Kill'
    clean = []
    for elem in p.tables[0][1:]:
        app = [""]*10
        wl = elem[3].split()
        app[0] = elem[1]
        if len(wl) == 2:
            if wl[-1] == '0%':
                app[1] = int(wl[0].strip("L")) # games played
                app[2] = 0 # wins
                app[3] = int(wl[0].strip("L")) # losses
                app[4] = 0 # winrate
            elif wl[-1] == '100%':
                app[1] = int(wl[0].strip("W")) # games played
                app[2] = int(wl[0].strip("W")) # wins
                app[3] = 0 # losses
                app[4] = 1 # winrate
            else:
                print('100%/0% WR ERROR')
        elif len(wl) == 3:
            app[1] = int(wl[0].strip("W"))+int(wl[1].strip("L"))
            app[2] = int(wl[0].strip("W")) # wins
            app[3] = int(wl[1].strip("L"))
            app[4] = round(int(wl[0].strip("W"))/app[1], 3)
        else:
            print('len WL wrong')
        app[5], app[6], app[7] = [float(x) for x in elem[4].split("  ")[0].split(" / ")]
        app[8] = int(elem[5].replace(",", ""))
        app[9] = float(elem[6].split('(')[1].strip(')'))
        app.insert(0,sTrans[seasonID])
        # print(app)
        # print(elem)
        clean.append(app)
    # print(clean)
    df = pd.DataFrame(clean,columns=["Season", "Champion", "Games Played", "Wins", "Losses", "Winrate", "Kills", "Deaths", "Assists", "Gold", "CS/m"])
    # return clean
    # print(df)
    return df

def getSummId(username):
    link = 'https://na.op.gg/summoner/userName='+username
    req = urllib.request.Request(url=link)

    f = urllib.request.urlopen(req)
    raw = f.read().decode('utf-8')

    match = re.search('(?<=summonerId).[0-9]+', raw)
    if match:
        # print(match.group(0))
        return int(match.group(0).strip('='))

def makeData(username):
    global folder
    # print(f"fetching data for {username}")

    start = timer()
    seasonIDs = [1,2,3,4,5,6,7,11,13,15,17,19]
    # header = ["Season", "Champion", "Games Played", "Wins", "Losses", "Winrate", "Kills", "Deaths", "Assists", "Gold", "CS/m"]
    summID = getSummId(username)
    m = []
    
    for season in seasonIDs:
        m.append(getSeason(summID, season, username))

    fdf = pd.concat(m)
    fdf.to_hdf("src/data/"+username+'.h5', key='df')
    end = timer()
    # print(f"{username} complete, {round(end-start, 2)} seconds elapsed")
    return(f"Fetched {username} data, visit vm-148-12.ise.luddy.indiana.edu:11000/plotChamps/{username} to see graph")

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
