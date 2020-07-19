import os

from bs4 import BeautifulSoup

from euroleague_scrapping.utils import simple_get
from urllib.parse import urlparse, parse_qs


class Euroscrapper:
    def __init__(self,league="euroleague",datadir="./data",years=[]):
        if(league not in ["euroleague","eurocup"]):
            print("The only valid options for league are euroleague and eurocup")
        self.league = league
        self.datadir = datadir
        self.years = years

    def start(self):
        base_url = "http://www.euroleague.net"
        if(self.league=="eurocup"): base_url = "https://www.eurocupbasketball.com"

        raw_html = simple_get(base_url+"/main/results")
        if(self.league=="eurocup"): raw_html = simple_get(base_url+"/eurocup/games/results")

        html = BeautifulSoup(raw_html, 'html.parser')
        selects = html.findAll("div",{"class": "game-center-selector"})[0].findAll("div",{"class":"styled-select"})
        yearsList = selects[0]
        base_dir = os.path.join(self.datadir,self.league)

        for year in yearsList.findAll("option"):
            parsed = urlparse(year['value'])
            seasoncode = (parse_qs(parsed.query)['seasoncode'][0])
            seasondir = os.path.join(base_dir,seasoncode)
            season = int(seasoncode[1:])
            if(len(self.years)!=0 and season not in self.years):
                print("Ignoring season",season)
                continue
            if not os.path.exists(seasondir):
                os.makedirs(seasondir)
            yearHtml = BeautifulSoup(simple_get(base_url+(year['value'])), 'html.parser')
            gamesTypeList = yearHtml.findAll("div", {"class": "game-center-selector"})[0].findAll("div", {"class": "styled-select"})[1]
            for gameType in gamesTypeList.findAll("option"):
                parsed = urlparse(gameType['value'])
                phase_text = gameType.text.strip()
                phasetypecode = (parse_qs(parsed.query)['phasetypecode'][0])
                phasetypedir = os.path.join(seasondir,phase_text)
                if not os.path.exists(phasetypedir):
                    os.makedirs(phasetypedir)
                print("Phase",phase_text)
                gameTypeHtml = BeautifulSoup(simple_get(base_url+(gameType['value'])), 'html.parser')
                roundsList = gameTypeHtml.findAll("div", {"class": "game-center-selector"})[0].findAll("div", {"class": "styled-select"})[2]
                for round in roundsList.findAll("option"):

                    not_ready_round = 0

                    round_text = round.text.strip()
                    print("ROUND:",round_text)
                    parsed = urlparse(round['value'])
                    gamenumber = (parse_qs(parsed.query)['gamenumber'][0])
                    roundHtml = BeautifulSoup(simple_get(base_url + (round['value'])), 'html.parser')
                    inputhtml = roundHtml.findAll("div", {"class": "wp-module-asidegames"})[0]
                    games_in_round_html = (inputhtml.findAll("a", {"class": "game-link"}))
                    round_dir = os.path.join(phasetypedir,round_text)
                    if not os.path.exists(phasetypedir):
                        os.makedirs(round_dir)
                    for game in games_in_round_html:
                        parsedGame = urlparse(game['href'])
                        gamecode = (parse_qs(parsedGame.query)['gamecode'][0]).strip()
                        print("GAMECODE:",gamecode)
                        gamedir = os.path.join(round_dir,gamecode)
                        gameHtml = BeautifulSoup(simple_get(base_url + game['href']), 'html.parser')
                        if(len(gameHtml.findAll("div", {"class": "dates"}))==0):
                            print("SKIPPING")
                            continue
                        datesHtml = gameHtml.findAll("div", {"class": "dates"})[0]
                        gameScoresHtml = gameHtml.findAll("div", {"class": "game-score"})[0]
                        if(len(gameHtml.findAll("div",{"id":"boxscore"}))==0):
                            print("NOT READY")
                            not_ready_round += 1
                            continue
                        if not os.path.exists(gamedir):
                            os.makedirs(gamedir)
                        boxscoreHtml = gameHtml.findAll("div",{"id":"boxscore"})[0]
                        with open(gamedir+"/boxscore.html", "w") as text_file:
                            text_file.write(str(boxscoreHtml))
                        with open(gamedir+"/dates.html", "w") as text_file:
                            text_file.write(str(datesHtml))
                        with open(gamedir+"/gamescores.html", "w") as text_file:
                            text_file.write(str(gameScoresHtml))
                        shootingStats = gameHtml.findAll("a",{"href":"#shooting"})
                        if len(shootingStats) != 0:
                            teamLinks = gameScoresHtml.findAll("a")
                            parsed = urlparse(teamLinks[0]['href'])
                            teamOne = (parse_qs(parsed.query)['clubcode'][0])
                            parsed = urlparse(teamLinks[1]['href'])
                            teamTwo = (parse_qs(parsed.query)['clubcode'][0])
                            apicalls = True
                            if(apicalls):
                                apiResp = simple_get("http://live.euroleague.net/api/Points?gamecode="+gamecode+"&seasoncode="+seasoncode+"&disp=")
                                with open(gamedir + "/points.json", "w") as text_file:
                                    text_file.write(apiResp.decode("utf-8"))
                                #print(apiResp)
                                apiResp = simple_get("http://live.euroleague.net/api/ShootingGraphic?gamecode="+gamecode+"&seasoncode="+seasoncode+"&disp=&a="+teamOne+"&b="+teamTwo)
                                with open(gamedir + "/shooting.json", "w") as text_file:
                                    text_file.write(apiResp.decode("utf-8"))

                                apiResp = simple_get(
                                    "http://live.euroleague.net/api/Header?gamecode=" + gamecode + "&seasoncode=" + seasoncode + "&disp=")
                                #print(apiResp)
                                with open(gamedir + "/header.json", "w") as text_file:
                                    text_file.write(apiResp.decode("utf-8"))

                                apiResp = simple_get(
                                    "http://live.euroleague.net/api/Players?gamecode=" + gamecode + "&seasoncode=" + seasoncode + "&disp=&equipo="+teamOne+"&temp="+seasoncode)
                                #print(apiResp)
                                with open(gamedir + "/players_"+teamOne+".json", "w") as text_file:
                                    text_file.write(apiResp.decode("utf-8"))

                                apiResp = simple_get(
                                    "http://live.euroleague.net/api/Players?gamecode=" + gamecode + "&seasoncode=" + seasoncode + "&disp=&equipo=" + teamTwo + "&temp=" + seasoncode)
                                with open(gamedir + "/players_"+teamTwo+".json", "w") as text_file:
                                    text_file.write(apiResp.decode("utf-8"))
                                #print(apiResp)
                        playByPlay = gameHtml.findAll("a",{"href":"#playbyplay"})
                        if len(playByPlay) != 0:
                            apiResp = simple_get(
                                "http://live.euroleague.net/api/PlayByPlay?gamecode=" + gamecode + "&seasoncode=" + seasoncode + "&disp=")
                            with open(gamedir + "/playbyplay.json", "w") as text_file:
                                text_file.write(apiResp.decode("utf-8"))
                    if(not_ready_round == len(games_in_round_html)):
                        print("REACHED THE END OF PLAYED GAMES")
                        os._exit(0)