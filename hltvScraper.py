# !/usr/bin/env python3
# hltv scrapeper
try:
    import sys
    from bs4 import BeautifulSoup
    import urllib.request
    from bs4 import BeautifulSoup, NavigableString, Tag
    from matchAPI import Match
except ImportError:
    print("Could not import modules")
    sys.exit()


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


def main():
    matches_found = True
    multiplier = 0

    while matches_found:
        # get the website link + 0ffset(used for filtering on website) and save to file
        # saved to a file for other uses, can also be stored in an object directly
        # the program will keep on looping until all matches have been scraped
        offset = multiplier * 50
        url = "http://www.hltv.org/?pageid=188&statsfilter=0&offset=" + str(offset)
        file_name = "index.html"
        write_url_to_file(url, file_name)

        # get the div containing the match data
        soup = BeautifulSoup(open("index.html"), "html5lib")
        matches = soup.findAll("div", {"style": "padding-left:5px;padding-top:5px;"})

        # if there are matches on the page
        if matches:

            # loop through matches' text (date, team_1, team_2, map, event)
            match_data = [[''] * 5 for i in range(50)]
            match_url = [[''] * 4 for k in range(50)]
            match_data_index = 0
            match_url_index = 0

            # loop through matches
            for match in matches:

                # loop through attr of match
                match_attr_index = 0
                match_url_attr_index = 0

                # get child of match
                for child in match:

                    # get the text from all the tags in child
                    if isinstance(child, Tag) and child.text:  # if Tag
                        match_data[match_data_index][match_attr_index] = str(child.text).strip()
                        match_attr_index += 1

                    # get the urls from all the tags in child
                    href = child
                    link = []   # urls (match_url, team_1_url, team_2_url, event_url)
                    if isinstance(href, Tag) and str(href)[:2] == "<a":
                        href = str(href)
                        link.append(href[href.find('"') + 1:href.find('&') + 1])
                        href = href[href.find('&') + 5:]
                        link.append(href[:href.find('&')])
                        match_url[match_url_index][match_url_attr_index] = ('http://www.hltv.org' + link[0] + link[1]).strip()
                        match_url_attr_index += 1

                # increment index counters
                match_data_index += 1
                match_url_index += 1
            # increment offset multiplier
            multiplier += 1

            obj_match = Match(match_data[0][0], match_url[0][0], match_data[0][1], match_url[0][1], match_data[0][2],
                              match_url[0][2], match_data[0][3], match_data[0][4], match_url[0][3])

            matches_found = False ##################### just checking first page ######################################

        # if no matches were found
        else:
            matches_found = False


    print('> All matches have been scraped...')
    print('> Quitting...')
    input('Press enter to terminate...')    # wait for input from the user
    sys.exit()


if __name__ == "__main__":
    main()

