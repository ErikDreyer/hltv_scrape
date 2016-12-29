# !/usr/bin/env python3
"""Module to that will act as a type of API for the website www.htlv.org"""

import urllib.request
import sys
from collections import OrderedDict


class Match:
    """
    Main
    An instance of match will take all the parameters of a match
    """

    def __init__(self, match_date, match_date_url, team_1_name, team_1_url, team_2_name, team_2_url, map_name,
                 event_name, event_url):
        """
        Initialize an instance of Match with all of its attributes
        :param match_date: date of the match
        :param match_date_url: url of the date of the match
        :param team_1_name: name of team_1 of the match
        :param team_1_url: url of team_1 of the match
        :param team_2_name: name of team_2 of the match
        :param team_2_url: url of team_2 of the match
        :param map_name: map name of the match
        :param event_name: event name of the match
        :param event_url: url of the event of the match
        """

        self.match_date = match_date
        self.match_date_url = match_date_url
        self.team_1_name = team_1_name
        self.team_1_url = team_1_url
        self.team_2_name = team_2_name
        self.team_2_url = team_2_url
        self.map_name = map_name
        self.event_name = event_name
        self.event_url = event_url

    def get_match_data(self):
        """return the data of the match, as received when creating an instance of the class"""
        match_data = OrderedDict()
        match_data['match_date'] = self.match_date
        match_data['match_date_url'] = self.match_date_url
        match_data['team_1_name'] = self.team_1_name
        match_data['team_1_url'] = self.team_1_url
        match_data['team_2_name'] = self.team_2_name
        match_data['team_2_url'] = self.team_2_url
        match_data['map'] = self.map_name
        match_data['event'] = self.event_name
        match_data['event_url'] = self.event_url
        return match_data.items()


def write_url_to_file(url, file_name):
    """
    Function for getting the plain html source from a webpage
    :param url: the url of the desired page
    :param file_name: the file that you want to store it in
    :return: returns nothing
    """
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
