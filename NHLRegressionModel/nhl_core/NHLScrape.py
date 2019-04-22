import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


def NHLStandings(year):
    """
    Scrapes NHL standings into a dataframe format from hockey-reference.com
    Takes a year as an argument to return the standings for that year
    """
    url = 'https://www.hockey-reference.com/leagues/NHL_' + str(year) + '_standings.html'
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')
    standings_table = soup.find('table', {'id': 'standings'})
    standing_data = [td.text for td in standings_table.find_all('td')]
    ranks = [rank.text for rank in standings_table.find_all('th')[22::]]
    teams = standing_data[::21]
    teams = list(map(lambda x: x.rstrip('*'), teams))

    url = 'https://www.hockey-reference.com/leagues/NHL_' + str(year) + '.html'
    comm = re.compile("<!--|-->")
    res = requests.get(url)
    soup = BeautifulSoup(comm.sub("", res.text), 'lxml')
    stats_table = soup.find('table', {'id': 'stats'})
    stats_data = [td.text for td in stats_table.find_all('td')]

    adv_stats_table = soup.find('table', {'id': 'stats_adv'})
    adv_stats_data = [td.text for td in adv_stats_table.find_all('td')]
    axDiff = adv_stats_data[11::22]
    axDiff = list(map(lambda x: x.lstrip('+'), axDiff))

    d = {"Rank": ranks, "Team": teams, "Average Age": stats_data[1::32][:-1],
         "GP": stats_data[2::32][:-1], "W": stats_data[3::32][:-1],
         "L": stats_data[4::32][:-1], "OL": stats_data[5::32][:-1],
         "PTS": stats_data[6::32][:-1], "PTS%": stats_data[7::32][:-1],
         "GF": stats_data[8::32][:-1], "GA": stats_data[9::32][:-1],
         "SOW": stats_data[10::32][:-1], "SOL": stats_data[11::32][:-1],
         "SRS": stats_data[12::32][:-1], "SOS": stats_data[13::32][:-1],
         "TG/G": stats_data[14::32][:-1], "EVGF": stats_data[15::32][:-1],
         "EVGA": stats_data[16::32][:-1], "PP": stats_data[17::32][-1],
         "PPO": stats_data[18::32][:-1], "PP%": stats_data[19::32][:-1],
         "PPA": stats_data[20::32][:-1], "PPOA": stats_data[21::32][:-1],
         "PK%": stats_data[22::32][:-1], "SH": stats_data[23::32][:-1],
         "SHA": stats_data[24::32][:-1], "PIM/G": stats_data[25::32][:-1],
         "oPIM/G": stats_data[26::32][:-1], "S": stats_data[27::32][:-1],
         "S%": stats_data[28::32][:-1], "SA": stats_data[29::32][:-1],
         "SV%": stats_data[30::32][:-1], "SO": stats_data[31::32][:-1],
         "5v5 S%": adv_stats_data[1::22], "5v5 SV%": adv_stats_data[2::22],
         "PDO": adv_stats_data[3::22], "CF": adv_stats_data[4::22],
         "CA": adv_stats_data[5::22], "CF%": adv_stats_data[6::22],
         "xGF": adv_stats_data[7::22], "xGA": adv_stats_data[8::22],
         "aGF": adv_stats_data[9::22], "aGA": adv_stats_data[10::22],
         "axDiff": axDiff, "SCF": adv_stats_data[12::22],
         "SCA": adv_stats_data[13::22], "SCF%": adv_stats_data[14::22],
         "HDF": adv_stats_data[15::22], "HDA": adv_stats_data[16::22],
         "HDF%": adv_stats_data[17::22], "HDGF": adv_stats_data[18::22],
         "HDC%": adv_stats_data[19::22], "HDGA": adv_stats_data[20::22],
         "HDCO%": adv_stats_data[21::22]}
    df = pd.DataFrame(d).set_index('Team')
    return df


def NHLGames(year):
    """
    Scrapes NHL Games into a dataframe format from hockey-reference.com
    Takes a year as an argument to return the standings for that year
    """
    url = 'https://www.hockey-reference.com/leagues/NHL_' + str(year) + '_games.html'
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')
    games_table = soup.find('table', {'class': 'sortable stats_table'})
    games_data = [td.text for td in games_table.find_all('td')]

    d = {'Date': [date.text for date in games_table.find_all('th')][9::],
         'Home': games_data[2::8], 'Home Goals': games_data[3::8],
         "Visitor": games_data[0::8], "Visitor Goals": games_data[1::8]}
    df = pd.DataFrame(d)
    df['HomeWin'] = df['Home Goals'] > df['Visitor Goals']
    df = df.dropna()
    return df
