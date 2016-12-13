# !/usr/bin/env python3
import sys
from bs4 import BeautifulSoup
import urllib.request
from bs4 import BeautifulSoup, NavigableString, Tag



class Match:
    """Class to take the values of the data of a match from www.hltv.org"""

    def __init__(self, match_date, match_date_url, team_1, team_1_url, team_2, team_2_url, map, event, event_url):
        self.match_date = match_date
        self.match_date_url = match_date_url
        self.team_1 = team_1
        self.team_1_url = team_1_url
        self.team_2 = team_2
        self.team_2_url = team_2_url
        self.map = map
        self.event = event
        self.event_url = event_url

    def get_match_info(self):
        """get the data from the match page"""
        write_url_to_file(self.match_date_url, "match_info.html")

        soup = BeautifulSoup(open("match_info.html"), "html5lib")
        group_data = soup.findAll("div", {"class": "covGroupBoxContent"})

        # set current box to match data
        current_box = 'MATCH_DATA'

        # save match data with keys and values: (played, map, event_name, game_score, team_Rating, first_kill, clutches)
        match_data_attrs = {}

        # save player data with a key and array of values: player_data_attrs[key] = [player_name, player_score]
        player_data_attrs = {}

        for group_items in group_data:
            item_count = 1  # count items in the groupbox
            for item in group_items:
                if isinstance(item, Tag) and item.text:
                    for info in item.findAll("div", {"style": "padding-left:5px;padding-top:5px;"}):
                        for match_info in info:
                            if isinstance(match_info, Tag):

                                # if MATCH_DATA
                                if current_box == 'MATCH_DATA' and match_info.text:

                                    # check to see if it is heading or a value
                                    # every second value is a key
                                    # every other value is a value
                                    if item_count % 2 == 0 and item_count < 16:
                                        value = match_info.text.strip()     # if value set as value
                                        match_data_attrs[key] = value   # save the key with a the value
                                    item_count += 1
                                    key = match_info.text.strip() # if heading set a key

                                # if PLAYER_DATA
                                elif current_box == 'PLAYER_DATA' and match_info.text:
                                    # every third value is a key
                                    # every other value is a value
                                    # other values come in pairs, player_name and player_score,
                                    # this is stored in an array

                                    # key value
                                    if item_count == 1:
                                        key = match_info.text.strip()
                                        item_count += 1
                                    # player name
                                    elif item_count == 2:
                                        player_name = match_info.text.strip()
                                        item_count += 1
                                    # player score
                                    elif item_count == 3:
                                        player_score = match_info.text.strip()

                                    # received all 3 values
                                        player_data_attrs[key] = [player_name, player_score]
                                        item_count = 1

            current_box = 'PLAYER_DATA'     # change the current box in use
            item_count = 1  # reset the item count that it can be used for PLAYER_DATA


    def get_team_1_info(self):
        """get the data from the team_1 page"""
        write_url_to_file(self.team_1_url, "team_1_info.html")

    def get_team_2_info(self):
        """get the data from the team_2 page"""
        write_url_to_file(self.team_2_url, "team_2_info.html")

    def get_event_info(self):
        """get the data from the event page"""
        write_url_to_file(self.event_url, "event_info.html")

    def __getattr__(self, attr):
        return self.data[attr]

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s" % (self.match_date, self.match_date_url, self.team_1, self.team_1_url, self.team_2, self.team_2_url, self.map, self.event, self.event_url)


def write_url_to_file(url, file_name):
    """method to fetch html from a web url and write it to a text file"""
    try:
        html_file = open(file_name, "w+")
        user_agent = "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7"
        headers = {'User-Agent': user_agent, }
        request = urllib.request.Request(url, None, headers)  # The assembled request
        response = urllib.request.urlopen(request)
        data = response.read()
        html_file.write(data.decode("utf-8"))
        html_file.close()
    except UnicodeError:
        print('Error: ' + str(UnicodeError))
        sys.exit()


