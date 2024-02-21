import PySimpleGUI as sg
import json
import serial
import os; os.system('clear')
import random
import string
from datetime import datetime
import serial.tools.list_ports



def random_hash(length=6):
    pool = string.ascii_lowercase
    return ''.join(random.choice(pool) for i in range(length))


# Marcadores por defecto. Se pueden modificar en el archivo config.json
with open('config.json', 'r') as f:
    marcadores_config = json.load(f)

# Cambiar keys a minisculas
marcadores_config = {key.lower(): value for key, value in marcadores_config.items()}

# Tema de la interfaz
sg.theme("DarkBlue3")
sg.set_options(font=("Courier New", 20, 'bold'))

# Marcadores en botonera
marcadores = []
temp = []
for key , value in marcadores_config.items():
    temp.append(sg.Button(f"{key} {value}", size=(14, 2), key=key))

    if len(temp) == 4:
        marcadores.append(temp)
        temp=[]
if len(temp) !=0:
    marcadores.append(temp)


# Layout de la interfaz
layout = [
    [sg.Listbox(serial.tools.list_ports.comports(),size=(30,2), enable_events=False, key='puertos' ) , 
     sg.Button("Conectar a BIS", size=(15, 1), key='connect')],
    marcadores,
]
window = sg.Window('Marcadores para BIS y Carescape B650', layout, use_default_focus=True, finalize=True)



# Binding key event
for key , value in marcadores_config.items():
    window.bind(f"<{key}>", key)
    window[key].Widget.configure(underline=0, takefocus=0)


while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        ser.close()
        break
    elif event == 'connect':
        if values['puertos'] == []:
            sg.popup("No se ha seleccionado puerto")
            continue
        try:
            # Valores de acuerdo al manual de BIS
            nombre_puerto = values['puertos'][0].split(' ')[0].strip()
            ser = serial.Serial(nombre_puerto, 
                                baudrate = 9600,
                                parity=serial.PARITY_NONE,
                                stopbits=serial.STOPBITS_ONE,
                                bytesize=serial.EIGHTBITS,
                                timeout=2
                                )
        except:
            sg.popup("No se ha podido conectar")
            continue
        window['connect'].update("Connectado!", disabled=True)
        window['puertos'].update(disabled=True)

    elif event in marcadores_config.keys():

        text = f"{marcadores_config[event.lower()]}--{random_hash()}"
        command = f"# {text} \r\n".encode()
        ser.write(command)

        # Guardar marcadores con su respectivo tiempo
        with open("output.txt", "a") as f:
            line = f"{datetime.now()}--{text}"
            f.write(line+"\n")
            print(line)

window.close()