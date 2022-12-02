import tkinter
import customtkinter # type: ignore



from subprocess import call


customtkinter.set_appearance_mode("system")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

app = customtkinter.CTk()
app.geometry("600x500")
app.title("Movilidad Urbana Launcher Simulator")

 
def runMcqueenFile():
    call(["./Entregables/EjecutableMcqueen/TrafficVisualization.exe"])


frame_1 = customtkinter.CTkFrame(master=app)
frame_1.pack(pady=30, padx=30, fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame_1, text="Movilidad Urbana Launcher Simulator", font=("Roboto", 20))
label.pack(pady=10, padx=10)

text_1 = customtkinter.CTkTextbox(master=frame_1, width=204, height=50)
text_1.pack(pady=10, padx=10)
text_1.insert("0.0", " Interfaz Grafica para ejecutar el visualizador.")


text_1 = customtkinter.CTkTextbox(master=frame_1, width=200, height=20)
text_1.pack(pady=10, padx=10)
text_1.insert("0.0", "Run City Simulation")


button_2 = customtkinter.CTkButton(master=frame_1, text="Run Simulation", command=runMcqueenFile)
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