import PySimpleGUI as sg

layout = [ [sg.Text("Bem-vindo ao Vector Race!")],
           [sg.Text("Introduza o nome do circuito"), sg.InputText()],
           [sg.Button("Confirmar"), sg.Button("Cancelar")]
            ]

window = sg.Window('Vector Race', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancelar': # if user closes window or clicks cancel
        break
    print('You entered ', values[0])

window.close()