import tkinter
import customtkinter # type: ignore

from mesaServer import runMesa
# from server_flask import runFlask

from subprocess import call


customtkinter.set_appearance_mode("system")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

app = customtkinter.CTk()
app.geometry("400x780")
app.title("Movilidad Urbana Launcher Tools")


def runMesaFile():
    runMesa(int(combobox_1.get()))


def runFlaskFile():
    call(["python", "./Entregables/EjecutableMesa/server_flask.py"])
    


frame_1 = customtkinter.CTkFrame(master=app)
frame_1.pack(pady=20, padx=60, fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame_1, text="Movilidad Urbana Launcher", font=("Roboto", 20))
label.pack(pady=10, padx=10)

text_1 = customtkinter.CTkTextbox(master=frame_1, width=204, height=100)
text_1.pack(pady=10, padx=10)
text_1.insert("0.0", " Interfaz Grafica para ejecutar Mesa Server y Flask Server.\n\n Para cambiar entre flask y mesa cerrar y volver a abrir la aplicacion")

text_1 = customtkinter.CTkTextbox(master=frame_1, width=200, height=50)
text_1.pack(pady=10, padx=10)
text_1.insert("0.0", "Mesa Server \n Elige Número de Agentes:")


combobox_1 = customtkinter.CTkComboBox(frame_1, values=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", 
                                                        "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"])
combobox_1.pack(pady=10, padx=10)


button_1 = customtkinter.CTkButton(master=frame_1, text="Run Mesa Server", command=runMesaFile)
button_1.pack(pady=10, padx=10)

text_1 = customtkinter.CTkTextbox(master=frame_1, width=200, height=50)
text_1.pack(pady=10, padx=10)
text_1.insert("0.0", "Server Flask")


button_2 = customtkinter.CTkButton(master=frame_1, text="Run Flask Server", command=runFlaskFile)
button_2.pack(pady=10, padx=10)



tabview_1 = customtkinter.CTkTabview(master=frame_1, width=200, height=70)
tabview_1.pack(pady=20, padx=20)
tabview_1.add("About")
tabview_1.set("About")
tabview_1.add("Developers")

text_About = customtkinter.CTkTextbox(tabview_1.tab("About"), width=200, height=100)
text_About.pack(pady=10, padx=10)
text_About.insert("0.0", "Tecnologico de Monterrey\n\n")

text_About = customtkinter.CTkTextbox(tabview_1.tab("Developers"), width=210, height=100)
text_About.pack(pady=10, padx=10)
text_About.insert("0.0",
                  "Sergio Gonzalez Vargas\n Gilberto Andre Garcia Gaytan\n Ricardo Condado")






app.mainloop()