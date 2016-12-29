# !/usr/bin/env python3
"""Scrape match data from the website hltv.org"""

from match import *
from bs4 import BeautifulSoup
import urllib.request
from bs4 import BeautifulSoup, NavigableString, Tag


def main():
    matches_found = True
    filter_offset = 50  # each page has an offset of 50
    filter_multiplier = 0   # multiplier used to increase the offset of the filter
    file_name = 'index.html'

    write_url_to_file('http://www.hltv.org/?pageid=188&statsfilter=0&offset=' + str(filter_offset * filter_multiplier),
                      file_name)

    # get the div containing the match data
    soup = BeautifulSoup(open("index.html"), "html5lib")
    # the div with all the match data in has a certain and unique styling
    match_raw_text = soup.findAll("div", {"style": "padding-left:5px;padding-top:5px;"})

    # if there are matches on the page, NOT the last page on the site
    if match_raw_text:
        # loop through matches' text (date, team_1, team_2, map, event)
        match_data = [[''] * 5 for i in range(50)]  # nested array
        match_url = [[''] * 4 for k in range(50)]  # nested array
        match_data_index = 0
        match_url_index = 0

        # loop through matches
        for match_raw_data in match_raw_text:

            # loop through match_raw_data of match_raw_text
            match_attr_index = 0
            match_url_attr_index = 0

            # get match of match_raw_data
            for match in match_raw_data:

                # get the text from all the tags in match
                if isinstance(match, Tag) and match.text:  # if Tag
                    match_data[match_data_index][match_attr_index] = str(match.text).strip()
                    match_attr_index += 1

                # get the urls from all the tags in child
                href = match
                link = []  # urls (match_url, team_1_url, team_2_url, event_url)
                if isinstance(href, Tag) and str(href)[:2] == "<a":
                    href = str(href)
                    link.append(href[href.find('"') + 1:href.find('&') + 1])
                    href = href[href.find('&') + 5:]
                    link.append(href[:href.find('&')])
                    match_url[match_url_index][match_url_attr_index] = (
                    'http://www.hltv.org' + link[0] + link[1]).strip()
                    match_url_attr_index += 1

            obj_match = Match(match_data[match_data_index][0], match_url[match_data_index][0],
                              match_data[match_data_index][1], match_url[match_data_index][1],
                              match_data[match_data_index][2], match_url[match_data_index][2],
                              match_data[match_data_index][3], match_data[match_data_index][4],
                              match_url[match_data_index][3])

            print(obj_match.get_match_data())

            # increment index counters
            match_data_index += 1
            match_url_index += 1

        # increment offset multiplier
        filter_multiplier += 1

        matches_found = False  ##################### just checking first page ######################################

        # if no matches were found
    else:
        matches_found = False

    print('> All matches have been scraped...')
    print('> Quitting...')
    # input('Press enter to terminate...')  # wait for input from the user
    sys.exit()


if __name__ == "__main__":
    main()