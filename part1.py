import json
from urllib.parse import parse_qsl, urlsplit

import PySimpleGUI as sg
from scholarly import ProxyGenerator, scholarly
from serpapi import GoogleSearch

API_KEY = "5f6b35250a77810b11e6d8a918abeb62e6f37fc18dd836f9ca17ebcb7d4269e6"

pg = ProxyGenerator()
success = pg.FreeProxies()
scholarly.use_proxy(pg)


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
    while True:
        res = search.get_dict()
        for article in res.get("articles", []):
            row = []
            row.append(article.get("title", ''))
            row.append(article.get("authors", ''))
            row.append(article.get("year", -1))
            row.append(article.get("cited_by").get("value"))

            data.append(row)

        if "next" in res.get("serpapi_pagination", []):
            search.params_dict.update(
                dict(parse_qsl(urlsplit(res.get("serpapi_pagination").get("next")).query)))
        else:
            break

    return (data, citedby)


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
            (data, citedby) = getAuthorArticles(values[0], values[1])
            # Fill Table
            window['-TABLE-'].update(data)
            window['-CIT-'].update("Total Citations: " + str(citedby))

    window.close()

if __name__ == "__main__":
    sg.theme('DarkAmber')
    windowArt()
