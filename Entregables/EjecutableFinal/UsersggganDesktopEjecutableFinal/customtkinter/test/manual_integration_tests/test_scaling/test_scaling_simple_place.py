import tkinter
import customtkinter  # <- import the CustomTkinter module

customtkinter.ScalingTracker.set_window_scaling(0.5)

customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

app = customtkinter.CTk()  # create CTk window like you do with the Tk window (you can also use normal tkinter.Tk window)
app.geometry("400x600")
app.title("CustomTkinter manual scaling test")

#app.minsize(200, 200)
#app.maxsize(520, 520)
#app.resizable(True, False)


def button_function():
    app.geometry(f"{200}x{200}")
    print("Button click", label_1.text_label.cget("text"))


def slider_function(value):
    customtkinter.set_widget_scaling(value * 2)
    customtkinter.set_window_scaling(value * 2)
    progressbar_1.set(value)


y_padding = 13

frame_1 = customtkinter.CTkFrame(master=app, height=550, width=300)
frame_1.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
label_1 = customtkinter.CTkLabel(master=frame_1, justify=tkinter.LEFT)
label_1.place(relx=0.5, y=50, anchor=tkinter.CENTER)
progressbar_1 = customtkinter.CTkProgressBar(master=frame_1)
progressbar_1.place(relx=0.5, y=100, anchor=tkinter.CENTER)
button_1 = customtkinter.CTkButton(master=frame_1, corner_radius=8, command=button_function)
button_1.place(relx=0.5, y=150, anchor=tkinter.CENTER)
slider_1 = customtkinter.CTkSlider(master=frame_1, command=slider_function, from_=0, to=1)
slider_1.place(relx=0.5, y=200, anchor=tkinter.CENTER)
slider_1.set(0.5)
entry_1 = customtkinter.CTkEntry(master=frame_1, placeholder_text="CTkEntry")
entry_1.place(relx=0.5, y=250, anchor=tkinter.CENTER)
checkbox_1 = customtkinter.CTkCheckBox(master=frame_1)
checkbox_1.place(relx=0.5, y=300, anchor=tkinter.CENTER)
radiobutton_var = tkinter.IntVar(value=1)
radiobutton_1 = customtkinter.CTkRadioButton(master=frame_1, variable=radiobutton_var, value=1)
radiobutton_1.place(relx=0.5, y=350, anchor=tkinter.CENTER)
radiobutton_2 = customtkinter.CTkRadioButton(master=frame_1, variable=radiobutton_var, value=2)
radiobutton_2.place(relx=0.5, y=400, anchor=tkinter.CENTER)
s_var = tkinter.StringVar(value="on")
switch_1 = customtkinter.CTkSwitch(master=frame_1)
switch_1.place(relx=0.5, y=450, anchor=tkinter.CENTER)

app.mainloop()
