import PySimpleGUI as sg


def start():
    # Define the window's contents
    layout = [[sg.Text("Melyik szezon legyen konvertálva?")],
              [sg.Input(key='-INPUT-')],
              [sg.Text(size=(40, 1), key='-OUTPUT-')],
              [sg.Button('Lekérdezések'),sg.Button('Táblázatok'), sg.Button('Quit')]]

    # Create the window
    window = sg.Window('Window Title', layout)

    # Display and interact with the Window using an Event Loop
    while True:
        event, values = window.read()
        # See if user wants to quit or window was closed
        if event == sg.WINDOW_CLOSED or event == 'Táblázatok':
            info = values['-INPUT-']
            from data_handler_files.converter_files.main_result_writer import create_team_csv as csv
            csv(info)
        if event == sg.WINDOW_CLOSED or event == 'Lekérdezések':
            from data_handler_files.requester_files import all_request as request
            request()
        # Output a message to the window
        window['-OUTPUT-'].update("Táblázatok elkészítve.")
        if event == sg.WINDOW_CLOSED or event == 'Quit':
            break

    # Finish up by removing from the screen
    window.close()


start()
