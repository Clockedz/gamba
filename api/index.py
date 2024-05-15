from flask import Flask, request, jsonify
from mwrogue.esports_client import EsportsClient
import pandas as pd
import datetime as dt

app = Flask(__name__)

@app.route("/api/python")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/api/win", methods=['GET'])
def winning():
    site = EsportsClient("lol")
    current_date = dt.date.today()
    player = request.args.get('player')
    current_date_str = current_date.strftime('%Y-%m-%d')
    date = (current_date - dt.timedelta(days=30)).strftime('%Y-%m-%d')


    response = site.cargo_client.query(
    tables="ScoreboardGames=SG, ScoreboardPlayers=SP, Tournaments=T, MatchSchedule=MS",
    join_on="SG.GameId=SP.GameId, SG.OverviewPage=T.OverviewPage, T.OverviewPage=MS.OverviewPage",
    fields="T.Name=Tournament, SG.DateTime_UTC, SG.Team1, SG.Team2, SG.Winner, SP.Team, SP.Champion, SP.Kills, SP.Deaths, SP.Assists, SP.CS, SP.SummonerSpells, SP.KeystoneMastery, SP.KeystoneRune, SP.Role, SP.GameId, SP.Side",
    where='SG.DateTime_UTC >= "' + date + ' 00:00:00" AND SG.DateTime_UTC <= "' + current_date_str + ' 23:59:59" AND SP.Name="%s"' % player,
    limit="500",
    group_by="SG.DateTime_UTC",
)
    pd.set_option('display.max_rows', None)
    df = pd.DataFrame(response)
    wins = []
    for i in df.index:
        win_team = df['Team'+str(df['Winner'][i])][i]
        if win_team == str(df['Team'][i]):
            wins.append(df.loc[i])
    wins_df = pd.DataFrame(wins)
    pd.set_option('display.max_rows', None)
    fantasy_points = fPoints(wins_df)
    kills = kill(wins_df)
    deaths = death(wins_df)
    assists = assist(wins_df)
    return jsonify({"fpoints": fantasy_points, "kills":kills,"deaths":deaths, "assists":assists})


@app.route("/api/neutral", methods=['GET'])
def neutral():
    site = EsportsClient("lol")
    current_date = dt.date.today()
    player = request.args.get('player')
    current_date_str = current_date.strftime('%Y-%m-%d')
    date = (current_date - dt.timedelta(days=30)).strftime('%Y-%m-%d')

    response = site.cargo_client.query(
    tables="ScoreboardGames=SG, ScoreboardPlayers=SP, Tournaments=T, MatchSchedule=MS",
    join_on="SG.GameId=SP.GameId, SG.OverviewPage=T.OverviewPage, T.OverviewPage=MS.OverviewPage",
    fields="T.Name=Tournament, SG.DateTime_UTC, SG.Team1, SG.Team2, SG.Winner, SP.Team, SP.Champion, SP.Kills, SP.Deaths, SP.Assists, SP.CS, SP.SummonerSpells, SP.KeystoneMastery, SP.KeystoneRune, SP.Role, SP.GameId, SP.Side",
    where='SG.DateTime_UTC >= "' + date + ' 00:00:00" AND SG.DateTime_UTC <= "' + current_date_str + ' 23:59:59" AND SP.Name="%s"' % player,
    limit="500",
    group_by="SG.DateTime_UTC",
)
    pd.set_option('display.max_rows', None)
    df = pd.DataFrame(response)
    pd.set_option('display.max_rows', None)
    fantasy_points = fPoints(df)
    kills = kill(df)
    deaths = death(df)
    assists = assist(df)
    return jsonify({"fpoints": fantasy_points, "kills":kills,"deaths":deaths, "assists":assists})

@app.route("/api/lose", methods=['GET'])
def losing():
    site = EsportsClient("lol")
    current_date = dt.date.today()
    player = request.args.get('player')
    current_date_str = current_date.strftime('%Y-%m-%d')
    date = (current_date - dt.timedelta(days=30)).strftime('%Y-%m-%d')


    response = site.cargo_client.query(
    tables="ScoreboardGames=SG, ScoreboardPlayers=SP, Tournaments=T, MatchSchedule=MS",
    join_on="SG.GameId=SP.GameId, SG.OverviewPage=T.OverviewPage, T.OverviewPage=MS.OverviewPage",
    fields="T.Name=Tournament, SG.DateTime_UTC, SG.Team1, SG.Team2, SG.Winner, SP.Team, SP.Champion, SP.Kills, SP.Deaths, SP.Assists, SP.CS, SP.SummonerSpells, SP.KeystoneMastery, SP.KeystoneRune, SP.Role, SP.GameId, SP.Side",
    where='SG.DateTime_UTC >= "' + date + ' 00:00:00" AND SG.DateTime_UTC <= "' + current_date_str + ' 23:59:59" AND SP.Name="%s"' % player,
    limit="500",
    group_by="SG.DateTime_UTC",
)
    pd.set_option('display.max_rows', None)
    df = pd.DataFrame(response)
    loss = []
    for i in df.index:
        win_team = df['Team'+str(df['Winner'][i])][i]
        if win_team != str(df['Team'][i]):
            loss.append(df.loc[i])
    lose_df = pd.DataFrame(loss)
    pd.set_option('display.max_rows', None)
    fantasy_points = fPoints(lose_df)
    kills = kill(lose_df)
    deaths = death(lose_df)
    assists = assist(lose_df)
    return jsonify({"fpoints": fantasy_points, "kills":kills,"deaths":deaths, "assists":assists})

def fPoints(df):
    kills_data = df['Kills'].tolist()
    kills_data_int = [int(kill) for kill in kills_data]
    deaths_data = df['Deaths'].tolist()
    deaths_data_int = [int(death) for death in deaths_data]
    assists_data = df['Assists'].tolist()
    assists_data_int = [int(assist) for assist in assists_data]
    CS_data = df['CS'].tolist()
    CS_data_int = [int(cs) for cs in CS_data]
    kills = sum(kills_data_int)/len(kills_data) * 3
    deaths = sum(deaths_data_int)/len(deaths_data) * -1
    assists = sum(assists_data_int)/len(assists_data) * 2
    cs = sum(CS_data_int)/len(CS_data) * 0.02
    points = kills + deaths + assists + cs
    return round(points,2)

def kill(df):
    kills_data = df['Kills'].tolist()
    kills_data_int = [int(kill) for kill in kills_data]
    kills = sum(kills_data_int)/len(kills_data)
    return round(kills,2)

def death(df):
    deaths_data = df['Deaths'].tolist()
    deaths_data_int = [int(death) for death in deaths_data]
    deaths = sum(deaths_data_int)/len(deaths_data)
    return round(deaths,2)

def assist(df):
    assists_data = df['Assists'].tolist()
    assists_data_int = [int(assist) for assist in assists_data]
    assists = sum(assists_data_int)/len(assists_data)
    return round(assists,2)






