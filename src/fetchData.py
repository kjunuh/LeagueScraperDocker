import re
from timeit import default_timer as timer
import os

import pandas as pd
import urllib.request
from pprint import pprint
from html_table_parser.parser import HTMLTableParser

folder = "data/"
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


    # with open(folder+username+".csv", "w+", newline='') as f:
    #     writer = csv.writer(f, lineterminator='\n')
    #     writer.writerow(header)
    #     for elem in dataList:
    #         writer.writerows(elem)

tfec = ['elfsuf', 'coolwhip420', 'nraddlygew', 'sekou', 'stealthinator', 'emended', 'xerelic', 'poweredbyrice', 'duckyduckplaysmc', 'meteoryte']
ugglee = ['forlorn64', 'chrismonytf', 'parad0x05', '9wonwon', 'xerelic', 'jonbom', 'junpi', 'aurumrock', 'hipbo', 'theristis', 'cocheese01', 'minibatman', 'nickizer534']
iu = ['CyborgSteve', 'D3f3ctive', 'Kevalon', 'AmericanHussar', 'co1iflower', '10slayer', 'MrLDS', 'YourLocalThicc', 'NiabiIsHere']
