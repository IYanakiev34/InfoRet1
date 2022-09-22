import json
from pprint import pprint
from urllib.parse import parse_qsl, urlparse, urlsplit

import numpy as np
import PySimpleGUI as sg
from scholarly import ProxyGenerator, scholarly
from serpapi import GoogleSearch

# API_KEY for serp
API_KEY = "9957764bad0f2c57c9cb392221e86f9660eae95920129cef945692d60e3ebd35"


class Utils():
    """
        Extract: title,authors,publication year, and citations
        for each articles in the authors articles and return the data
    """
    @staticmethod
    def get_authors_articles_and_cites(author_name, sort):
        author_id = Utils.get_authors_id_from_name(str(author_name))

        # Preprocess sorting parameter
        if sort == 'Year':
            sort = 'pubdate'
        else:
            sort = ''

        params = {
            "engine": "google_scholar_author",
            "author_id": author_id,
            "api_key": API_KEY,
            "sort": sort,
            "start": 0,
            "num": 100,
        }

        search = GoogleSearch(params)

        profile_is_present = True

        data = []
        # Iterate to find all articles
        while profile_is_present:
            results = search.get_dict()
            articles = results['articles']

            for article in articles:
                row = []
                row.append(article['title'])
                authors = article['authors'].split(',')

                # Remove unneccessary white spaces
                for i in range(len(authors)):
                    authors[i] = authors[i].strip()
                
                row.append(authors)
                row.append(article['year'])
                row.append(article['cited_by']['value'])
                
                data.append(row)

            try:
                if 'next' in results['serpapi_pagination']:
                    search.params_dict.update(
                        dict(parse_qsl(urlsplit(results['pagination']['next']).query)))
                else:
                    profile_is_present = False
            except KeyError:
                profile_is_present = False

        return data

    @staticmethod
    def get_selected_papers_citings(selected_papers,author_name):
        """
            TODO: call the SERP API endpoint for citings
            Get infromation about the citing papers
                Publisher
                Year
                Journal
                    * If authors are collinding self citation
        """
        search_query = scholarly.search_author(author_name)
        author = scholarly.fill(next(search_query),sections=['publications'])
        
        publications = author['publications']
    
        dict_year = {}
        dict_pub = {}
        dict_jour = {}

        data = []

        for index,pub in enumerate(publications):
            if index in selected_papers:
                self_citings = 0
                filled_pub = scholarly.citedby(pub)
                filled_pub = next(filled_pub)
                
                # TODO: self citations based on this not the thing im doing now
                closer_look = scholarly.fill(author['publications'][index])

                #Fill rows of data
                row = []
                row.append(closer_look['bib']['title'])
                row.append(closer_look['bib']['author'])
                row.append(closer_look['bib']['pub_year'])
                row.append(closer_look['num_citations'])

                auths = filled_pub['bib']['author']

                for auth in auths:
                    if auth == author_name:
                        self_citings += 1

                row.append(self_citings)
                row.append(row[3] - self_citings)
                
                data.append(row)
                
                try:
                    year = filled_pub['bib']['pub_year']
                    if year in dict_year:
                        dict_year[year] += 1
                    else:
                        dict_year[year] = 1
                except KeyError:
                    dict_year["None"] = 0


                try:
                    publisher = filled_pub['pub_url']
                    publisher = urlparse(publisher).netloc

                    if publisher in dict_pub:
                        dict_pub[publisher] += 1
                    else:
                        dict_pub[publisher] = 1
                except KeyError:
                    dict_pub["None"] = 0 


                try:
                    journal = filled_pub['bib']['venue']

                    if journal in dict_jour:
                        dict_jour[journal] += 1
                    else:
                        dict_jour[journal] = 1
                except KeyError:
                    dict_jour["None"] = 0


        hist_pub = []
        hist_jour = []
        hist_year = []

        for i in dict_pub:
            row = []
            row.append(i)
            row.append(dict_pub[i])

            hist_pub.append(row)

        for i in dict_jour:
            row = []
            row.append(i)
            row.append(dict_jour[i])

            hist_jour.append(row)

        for i in dict_year:
            row = []
            row.append(i)
            row.append(dict_year[i])

            hist_year.append(row)


        return (hist_year,hist_pub,hist_jour,data)



        # TODO: return(publishers,Years,Journals,self-citations)


    """
        Extract the data needed for the histograms of all the authors
        publications: publications per year, publications by publisher
    """
    @staticmethod
    def get_authors_histograms(author_name):
        search_query = scholarly.search_author(author_name)
        author = scholarly.fill(next(search_query))

        publications = author['publications']

        dict_pub = {}
        dict_year = {}
        # Extract publishers and pubs per year
        for pub in publications:
            filled_pub = scholarly.fill(pub)

            try:
                pub_year = filled_pub['bib']['pub_year']

                if pub_year in dict_year:
                    dict_year[pub_year] += 1
                else:
                    dict_year[pub_year] = 1
            except KeyError:
                dict_year["None"] = 0

            try:
                publisher = filled_pub['pub_url']

                publisher = urlparse(publisher).netloc

                if publisher in dict_pub:
                    dict_pub[publisher] += 1
                else:
                    dict_pub[publisher] = 1
            except KeyError:
                dict_pub["None"] = 1

        hist_year = []
        hist_pub = []

        # Convert dictionary into list
        for i in dict_year:
            row = []
            row.append(i)
            row.append(dict_year[i])

            hist_year.append(row)

        for i in dict_pub:
            row = []
            row.append(i)
            row.append(dict_pub[i])

            hist_pub.append(row)

        return (hist_year, hist_pub)

    """
        Extract the auhtor id given an author name
    """
    @staticmethod
    def get_authors_id_from_name(author_name):
        search_query = scholarly.search_author(author_name)
        author = next(search_query)

        return author['scholar_id']

    @staticmethod
    def get_authors_total_citations(author_name):
        search_query = scholarly.search_author(author_name)
        author = next(search_query)

        return author['citedby']
    
    @staticmethod
    def get_selected_papers(papers):
        papers = papers.strip('[]')
        selected_papers = []

        is_array = False
        data = []
        for i in papers:
            if i == '-':
                is_array = True
                papers = papers.replace(i,' ')

        if is_array:
            papers = papers.split(' ')
            for i in range(int(papers[0]),int(papers[1])+1):
               selected_papers.append(i)
        else:
            papers= papers.split(',')
            for i in papers:
                selected_papers.append(int(i))


        return selected_papers

    
"""
    Create window modal that will lead to the other windows
    for the assignment. Acts as a gateway
"""
def create_window_modal():
    layout = [
        [sg.Button('Articles By An Author', key='-ART-', size=(60, 2))],
        [sg.Button('Histograms For Author', key='-HIST-', size=(60, 2))],
        [sg.Button('Citing Papers', key='-CITE-', size=(60, 2))],
        [sg.Button('All Articles Info', key='-INFO-', size=(60, 2))],
    ]

    window = sg.Window('Window Modal', layout, size=(
        500, 250), element_justification='c')

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Quit':
            break

        if event == '-ART-':
            create_articles_window()
        elif event == '-HIST-':
            create_window_histograms()
        elif event == '-CITE-':
            create_window_cites()
        elif event == '-INFO-':
            create_window_all_info()

    window.close()


"""
    Method for creating a window to find all articles of an author
"""


def create_articles_window():
    layout = [
        [sg.Text('GIU for Google Scholar queries')],
        [sg.Text('Search Author'), sg.InputText(do_not_clear=True)],
        [sg.Text('Sort by:'), sg.InputCombo(
            ['Citations', 'Year'], size=(40, 2))],
        [sg.Button('Submit')],
        [sg.Text('List of authors\' articles')],
        [sg.Table(values=[], headings=['Title', 'Authors', 'Publication Year', 'Citations'],
                  auto_size_columns=False,
                  col_widths=[20, 20, 12, 12],
                  max_col_width=80,
                  display_row_numbers=True,
                  justification='c',
                  key='-TABLE-',
                  row_height=30)],
        [sg.Text("Total Citations: 0", key='-CIT-')]
    ]

    window = sg.Window('Author Articles', layout=layout,
                       element_justification='c', size=(1024, 800))

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Quit':
            break

        if event == 'Submit':
            # Get author artciles
            articles = Utils.get_authors_articles_and_cites(
                values[0], values[1])
            # Get total citations
            total_citations = Utils.get_authors_total_citations(values[0])

            # Update the GUI
            window['-TABLE-'].update(articles)
            window['-CIT-'].update("Total Citations: " + str(total_citations))

    window.close()


"""
    Method to create window for the histograms
    of all the papers of a selected author
"""


def create_window_histograms():
    layout = [
        [sg.Text('GIU for Google Scholar queries')],
        [sg.Text('Search Author'), sg.InputText(do_not_clear=True)],
        [sg.Button('Submit')],
        [sg.Text('Histograms for all publications by an author.')],
        [sg.Table(values=[], headings=['Publication Year', 'Quantity'],
                  auto_size_columns=False,
                  col_widths=[20, 20],
                  max_col_width=80,
                  display_row_numbers=True,
                  justification='c',
                  key='-YEAR-',
                  row_height=30)],
        [sg.Table(values=[], headings=['Publisher', 'Quantity'],
                  auto_size_columns=False,
                  col_widths=[20, 20],
                  max_col_width=80,
                  display_row_numbers=True,
                  justification='c',
                  key='-PUB-',
                  row_height=30)],
    ]

    window = sg.Window('Author Histograms', layout=layout,
                       element_justification='c', size=(1200, 1000))

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Quit':
            break

        if event == 'Submit':
            # Get papers per year and papers per publisher
            (hist_year, hist_pub) = Utils.get_authors_histograms(values[0])
            # Update the GUI
            window['-YEAR-'].update(hist_year)
            window['-PUB-'].update(hist_pub)

    window.close()


"""
   Window to show the quantity of papers citing the authors
   selected papers in 3 categories:Source,Publisher,Publication Year
"""


def create_window_cites():
    layout = [
        [sg.Text('GIU for Google Scholar queries')],
        [sg.Text('Search Author'), sg.InputText(do_not_clear=True)],
        [sg.Text('Selected Papers'), sg.InputText(do_not_clear=True)],
        [sg.Button('Submit')],
        [sg.Text('Histograms for all papers citing the authors selected papers.')],
        [sg.Table(values=[], headings=['Source(Journal/Conference)', 'Quantity'],
                  auto_size_columns=False,
                  col_widths=[25, 20],
                  max_col_width=80,
                  display_row_numbers=True,
                  justification='c',
                  key='-JOUR-',
                  row_height=30)],
        [sg.Table(values=[], headings=['Publication Year', 'Quantity'],
                  auto_size_columns=False,
                  col_widths=[25, 20],
                  max_col_width=80,
                  display_row_numbers=True,
                  justification='c',
                  key='-YEAR-',
                  row_height=30)],
        [sg.Table(values=[], headings=['Publisher', 'Quantity'],
                  auto_size_columns=False,
                  col_widths=[25, 20],
                  max_col_width=80,
                  display_row_numbers=True,
                  justification='c',
                  key='-PUB-',
                  row_height=30)],
    ]

    window = sg.Window('Citings of Papers', layout=layout,
                       element_justification='c', size=(1200, 1000))

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Quit':
            break

        if event == 'Submit':
            selected_papers = Utils.get_selected_papers(values[1])
            
            (hist_year,hist_pub,hist_jour,data) = Utils.get_selected_papers_citings(selected_papers,values[0])
            """
                Get citing information only first page
                Per Source
                Per Year
                Per Publisher
                Get self-citations:
                    The amount of time that both autors names collide: 
                        * At least one author common in 2 papers
            """
            window['-JOUR-'].update(hist_jour)
            window['-YEAR-'].update(hist_year)
            window['-PUB-'].update(hist_pub)
            # Update the GUI

    window.close()


"""
    Window for displaying all information on selected papers on an author
    Displayed informaiton: Title,Authors,Publication year,Citations,Self-citations,Non-self-citations
"""
def create_window_all_info():
    layout = [
        [sg.Text('GIU for Google Scholar queries')],
        [sg.Text('Search Author'), sg.InputText(do_not_clear=True)],
        [sg.Text('Selected Papers'), sg.InputText(do_not_clear=True)],
        [sg.Button('Submit')],
        [sg.Text('List of authors\'s articles')],
        [sg.Table(values=[], headings=['Title', 'Authors', 'Publication year', 'Citations', 'Self-citations', 'Non-self-citations'],
                  auto_size_columns=False,
                  col_widths=[15, 15, 12, 12, 12],
                  max_col_width=80,
                  display_row_numbers=True,
                  justification='c',
                  key='-INFO-',
                  row_height=30)],
    ]

    window = sg.Window('All info on papers', layout=layout,
                       element_justification='c', size=(1024, 780))

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Quit':
            break

        if event == 'Submit':
            selected_papers = Utils.get_selected_papers(values[1])
            
            (hist_year,hist_pub,hist_jour,data) = Utils.get_selected_papers_citings(selected_papers,values[0])
            window['-INFO-'].update(data)
            # Update the GUI
            pass

    window.close()


if __name__ == "__main__":
    sg.theme('DarkAmber')
    create_window_modal()
