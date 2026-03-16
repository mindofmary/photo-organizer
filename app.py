import customtkinter as ctk
from tkinter import filedialog
import threading

from organizer import organize
from stats import gerar_estatisticas

ctk.set_appearance_mode("system")


class App(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.title("Photo Organizer Pro")

        self.geometry("600x420")

        self.origin=""
        self.dest=""

        ctk.CTkLabel(
            self,
            text="Photo Organizer Pro",
            font=("Arial",24)
        ).pack(pady=20)

        ctk.CTkButton(
            self,
            text="Selecionar origem",
            command=self.select_origin
        ).pack(pady=10)

        ctk.CTkButton(
            self,
            text="Selecionar destino",
            command=self.select_dest
        ).pack(pady=10)

        self.progress = ctk.CTkProgressBar(self,width=400)

        self.progress.pack(pady=20)

        ctk.CTkButton(
            self,
            text="Organizar",
            command=self.start
        ).pack(pady=10)

        ctk.CTkButton(
            self,
            text="Ver estatísticas",
            command=self.stats
        ).pack(pady=10)


    def select_origin(self):

        self.origin = filedialog.askdirectory()


    def select_dest(self):

        self.dest = filedialog.askdirectory()


    def update_progress(self,i,total):

        self.progress.set(i/total)


    def start(self):

        threading.Thread(target=self.run).start()


    def run(self):

        organize(
            self.origin,
            self.dest,
            self.update_progress
        )


    def stats(self):

        gerar_estatisticas(self.dest)


app = App()

app.mainloop()