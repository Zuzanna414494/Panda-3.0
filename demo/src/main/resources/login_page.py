from tkinter import *
from PIL import Image, ImageTk


root = Tk()
root.title('Panda 3.0')
root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")

logo_font = ("Freestyle Script", 100, "bold")
jasny = '#E4D1FF'
ciemny = '#AE6FFF'


frame_ciemny = Frame(root, bg=ciemny)
frame_ciemny.pack(anchor=N, fill=BOTH)

frame_1 = Frame(frame_ciemny, bg=ciemny)
frame_1.pack(anchor=N)

frame_panda = Frame(frame_1, bg=ciemny, bd=0)
frame_panda.pack(anchor=NW, side=LEFT)

panda = Canvas(frame_panda, width=200, height=200, bg=ciemny, bd=0)
panda.pack(anchor=NW, side=LEFT)
panda_png = (Image.open("panda_ciemny.png"))
resized_image = panda_png.resize((200, 200))
new_image = ImageTk.PhotoImage(resized_image)
panda.create_image(10, 10, anchor=NW, image=new_image)

welcome = Label(frame_1, text="  Welcome to ", font=("Helvetica", 50), bg=ciemny, cursor='xterm')
welcome.pack(side=LEFT)

logo = Label(frame_1, text="Panda 3.0", font=logo_font, bg=ciemny)
logo.pack(side=LEFT)

frame_opis = Frame(root, bg=ciemny)
frame_opis.pack(anchor=N, side=RIGHT, fill=BOTH)

opis = Label(frame_opis, text="Dear student,\nThis is your modern class register, in which:\n > you can check your grades,\n > you can see your grade's average,\n > you can check your lesson plan and scheduled tests,\n > you can see a notice board,\n > you can compare your grades with others by rankings,\n > you can see some informations about your teachers,\n > we can navigate you to your school buildings!\n\n\n", wraplength=550, font=("Arial", 20, "italic"), bg=ciemny, cursor='xterm', bd=10)
opis.pack(anchor=W)

druczek = Label(frame_opis, text="If you don't have an account, you have to ask your teacher to make you one", wraplength=550, font=("Arial", 10, "italic"), bg=ciemny, cursor='xterm', bd=10)
druczek.pack(anchor=S)

frame_jasny = Frame(root, bg=jasny)
frame_jasny.pack(anchor=N, fill=BOTH, expand=True)

frame_log_req = Frame(frame_jasny, bg=jasny, bd=50)
frame_log_req.pack()

log_req = Label(frame_log_req, text="\nLog in to continue", font=("Helvetica", 33), bg=jasny, cursor='xterm')
log_req.pack()

frame_2 = Frame(frame_jasny, bg=jasny, bd=20)
frame_2.pack(anchor=N)

user_name = Label(frame_2, text="Username   ", font=("Helvetica", 30), bg=jasny, cursor='xterm')
user_name.pack(side=LEFT)

user_name_input_area = Entry(frame_2, width=30, font=("Helvetica", 20), bd=5)
user_name_input_area.pack(side=LEFT)


frame_3 = Frame(frame_jasny, bg=jasny, bd=20)
frame_3.pack(anchor=N)

user_password = Label(frame_3, text="Password   ", font=("Helvetica", 30), bg=jasny, cursor='xterm')
user_password.pack(side=LEFT)

user_password_entry_area = Entry(frame_3, width=30, font=("Helvetica", 20), bd=5)
user_password_entry_area.pack(side=LEFT)


newline = Label(frame_jasny, text="\n", bg=jasny)
newline.pack()

submit_button = Button(frame_jasny, text="Submit", font=("Helvetica", 20), bd=10, cursor='hand2')



root.mainloop()
