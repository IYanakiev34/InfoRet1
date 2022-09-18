import PySimpleGUI as sg
from scholarly import ProxyGenerator, scholarly

pg = ProxyGenerator()
success = pg.FreeProxies()
scholarly.use_proxy(pg)


def getAuthorArticles(authorName,sorting):
    if sorting == 'Year':
        sorting = 'year'
    else:
        sorting = 'citedby'

    search_query = scholarly.search_author(authorName)
    author = next(search_query)
    articles = scholarly.fill(
        author, sections=['basics','publications','indices','coauthors','counts'], sortby=sorting)

    # Correct len
    data = []
    citedby = articles['citedby']
    
    for index,pub in enumerate(articles['publications']):
        row = []
        extended_pub = scholarly.fill(pub)

        try:
            row.append(extended_pub['bib']['title'])
        except KeyError:
            row.append('')

        try:
            row.append(extended_pub['bib']['author'])
        except KeyError:
            row.append('')

        try:
            row.append(extended_pub['bib']['pub_year'])
        except KeyError:
            row.append(-1)

        try:
            row.append(pub['num_citations'])
        except KeyError:
            row.append(-1)

        data.append(row)


    return (data, citedby)


def createLayout():
    layout = [
        [sg.Text("GUI for Google Scholar queries")],
        [sg.Text('Enter Author name'), sg.InputText(do_not_clear=False)],
        [sg.Text('Sort terms of'), sg.InputCombo(
            ['Citations', 'Year'], size=(40, 2))],
        [sg.Button('Submit')],
        [sg.Text('List of the authors articles')],
        [sg.Table(values=[], headings=['Title', 'Authors', 'Publication year', 'citations'],
                  auto_size_columns=False,
                  col_widths=[20,20,12,12],
                  max_col_width=80,
                  display_row_numbers=True,
                  justification='center',
                  key='-TABLE-',
                  row_height=30)],
        [sg.Text("Total Citations: 0",key='-CIT-')]
    ]

    return layout


if __name__ == "__main__":
    sg.theme('DarkAmber')

    layout = createLayout()

    window = sg.Window('Part 1', layout, size=(
        1024, 800), element_justification='c')

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Quit':
            break

        if event == 'Submit':
            (data,citedby) = getAuthorArticles(values[0],values[1])
            # Fill Table
            window['-TABLE-'].update(data)
            window['-CIT-'].update("Total Citations: " + str(citedby))

    window.close()
