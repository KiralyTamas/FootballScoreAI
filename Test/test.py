import PySimpleGUI as sg

layout=[
    [sg.Text("Ez az első ablakom")],
    [sg.Button("Ablak Bezárás")]
]

window=sg.Window("Demo",layout)

while True:
    event, value=window.read()
    if event=="Ablak Bezárás" or event==sg.WIN_CLOSED:
        break

window.close()