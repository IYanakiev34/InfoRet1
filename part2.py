import json
from urllib.parse import parse_qsl, urlsplit

import PySimpleGUI as sg
from scholarly import ProxyGenerator, scholarly
from serpapi import GoogleSearch

# API_KEY for serp 
API_KEY = "5f6b35250a77810b11e6d8a918abeb62e6f37fc18dd836f9ca17ebcb7d4269e6"

# Creating proxie for schoalry in order to use the citedby query
pg = ProxyGenerator()
success = pg.FreeProxies()
scholarly.use_proxy(pg)


"""
 This method gets all the articles by an author
 Return => (articles by author,total citations)
"""

def getAuthorArticles(authorName, sorting):
    if sorting == 'Year':
        sorting = 'pubdate'
    else:
        sorting = ''

    search_query = scholarly.search_author(authorName)
    author = next(search_query)

    citedby = author['citedby']
    author_id = author['scholar_id']

    params = {
        "engine": "google_scholar_author",
        "author_id": author_id,
        "api_key": API_KEY,
        "sort": sorting,
        "hl": "en",
        "start": 0,
        "num": 100
    }

    search = GoogleSearch(params)
    results = search.get_dict()


    data = []
    publishers = []
    while True:
        res = search.get_dict()
        for article in res.get("articles", []):

            row = []
            row.append(article.get("title", ''))
            row.append(article.get("authors", ''))
            row.append(article.get("year", -1))
            row.append(article.get("cited_by").get("value"))
            
            curr_pub = article.get("publication",'')
            curr_pub = curr_pub.split(' ')[0]
            publishers.append(curr_pub)

            data.append(row)

        if "next" in res.get("serpapi_pagination", []):
            search.params_dict.update(
                dict(parse_qsl(urlsplit(res.get("serpapi_pagination").get("next")).query)))
        else:
            break

    return (data, citedby,publishers)


"""
    Method to find how many articles has an author
    written in an year for all years
"""

def articlesByYear(data):
    
    res = {}
    
    for i in data:
        if i[2].isnumeric():
            if i[2] in res:
                res[i[2]] += 1
            else:
                res[i[2]] = 1
    
    result = []

    for i in res:
        row = [i,res[i]]
        result.append(row)

    return result
  
"""
    Method to how many articles has each publisher
    published for a given authors papers
"""

def articlesByPublisher(publishers):
    
    d = {}
    for publisher in publishers:
        if publisher in d:
            d[publisher] += 1
        else:
            d[publisher] = 1

    result = []
    for i in d:
        row = [i,d[i]]
        result.append(row)

    return result

"""
    Method for creating a window Modal
    that allows navigation to the otherwindows
"""

def windowModal():
    layout = [
        [sg.Button('Authors articles', key='-ART-',
                   auto_size_button=False, size=(60, 2))],
        [sg.Button('Authors histogram', key='-HIST-',
                   auto_size_button=False, size=(60, 2))],
        [sg.Button('Cited papers histogram', key='-CITE-',
                   auto_size_button=False, size=(60, 2))]
    ]

    window = sg.Window('Window Modal', layout, size=(
        300, 200), element_justification='c')

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Quit':
            break

        if event == '-ART-':
            windowArt()
        elif event == '-HIST-':
            windowHist()
        elif event == '-CITE-':
            pass
    window.close()

"""
    Method for creating the window of for the articles
    of a given author and sort them by pubdate or citations
"""

def windowArt():
    layout = [
        [sg.Text("GUI for Google Scholar queries")],
        [sg.Text('Enter Author name'), sg.InputText(do_not_clear=False)],
        [sg.Text('Sort terms of'), sg.InputCombo(
            ['Citations', 'Year'], size=(40, 2))],
        [sg.Button('Submit')],
        [sg.Text('List of the authors articles')],
        [sg.Table(values=[], headings=['Title', 'Authors', 'Publication year', 'citations'],
                  auto_size_columns=False,
                  col_widths=[20, 20, 12, 12],
                  max_col_width=80,
                  display_row_numbers=True,
                  justification='center',
                  key='-TABLE-',
                  row_height=30)],
        [sg.Text("Total Citations: 0", key='-CIT-')]
    ]

    window = sg.Window('Authors Papers', layout, size=(
        1024, 800), element_justification='c')

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Quit':
            break

        if event == 'Submit':
            (data, citedby,publishers) = getAuthorArticles(values[0], values[1])
            # Fill Table
            window['-TABLE-'].update(data)
            window['-CIT-'].update("Total Citations: " + str(citedby))

    window.close()

"""
    Method for creating the window for the Histograms
    of the authors papers
"""

def windowHist():
    layout = [
        [sg.Text("GUI for Google Scholar queries")],
        [sg.Text("Search Author"), sg.InputText(do_not_clear=False)],
        [sg.Button("Submit")],
        [sg.Text("Histogram of all author's papers")],
        [sg.Table(values=[], headings=[ 'Publication Year', 'Quantity'], auto_size_columns=False,
                  col_widths=[20, 10],
                  max_col_width=40,
                  display_row_numbers=True,
                  justification='center',
                  key='-HIST1-',
                  row_height=30)],
        [sg.Table(values=[], headings=[ 'Publisher', 'Qunatity'], auto_size_columns=False,
                  col_widths=[20, 10],
                  max_col_width=40,
                  display_row_numbers=True,
                  justification='center',
                  key='-HIST2-',
                  row_height=30)]
    ]

    window = sg.Window('Authors Histograms', layout, size=(
        1024, 800), element_justification='c')

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Quit':
            break

        if event == 'Submit':
            # Get articles and then get the histrogram
            (data,citedby,publishers) = getAuthorArticles(values[0], 'Year')
                
            print("\n Data:{0}\n \nCitedby:{1}\n \nPublishers:{2}\n" .format(data,citedby,publishers))
            byYear = articlesByYear(data)
            byPublisher = articlesByPublisher(publishers) 

            # Update the data in the table
            window['-HIST1-'].update(byYear)
            window['-HIST2-'].update(byPublisher)

if __name__ == "__main__":
    sg.theme('DarkAmber')
    windowModal()
