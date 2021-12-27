import PySimpleGUI as sg


def start():
    layout = [[sg.Text("Melyik szezon legyen konvertálva?")], [sg.Input(key='-INPUT-')],
        [sg.Button('Lekérdezések'), sg.Button('Táblázatok'), sg.Button('Team Stat'), sg.Button('Quit')],[sg.Output(size=(60,15),key='-OUTPUT-')]]
    window = sg.Window('Window Title', layout)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Lekérdezések':
            import data_handler_files.requester_files.all_request
            window['-OUTPUT-'].update(
                "Minden meccs lekérve az Understat.com szerveréről.")
        if event == sg.WINDOW_CLOSED or event == 'Táblázatok':
            info = values['-INPUT-']
            from data_handler_files.converter_files.main_result_writer import create_team_csv as csv
            csv(info)
            window['-OUTPUT-'].update("Táblázatok elkészítve.")
        if event == sg.WINDOW_CLOSED or event == 'Team Stat':
            from data_handler_files.converter_files.team_stat import last_10 as stat
            stat()
            window['-OUTPUT-'].update("Csapatok statisztikája kész.")
        if event == sg.WINDOW_CLOSED or event == 'Quit':
            break
    window.close()


start()
