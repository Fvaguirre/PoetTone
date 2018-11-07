import tkinter as tk
import threading
import Audio
import Loader
import os

DEF_X = 1200
DEF_Y = 700
DEF_L = DEF_X - 150
TEXT_FONT = "Baskerville old face"
TEXT_SIZE = 15
POEMFOLDER = "Poems/"

class PoemThread(threading.Thread):
    _stopevent = None
    poem = None

    def __init__(self, poem):
        self._stopevent = threading.Event()
        self.poem = poem
        super(PoemThread, self).__init__()

    def run(self):
        if not self._stopevent.isSet():
            Loader.poemLoader(self.poem)

    def join(self, timeout=None):
        Audio.endPoemMusic()
        self._stopevent.set()
        threading.Thread.join(self, timeout)

class App(tk.Frame):
    cur_line = 0
    thread = None

    def __init__(self, root=None):
        poems = {}
        # Initialize poem dictionary
        def Poems():
            for file in os.listdir(POEMFOLDER):
                if file.endswith(".txt"):
                    f = open(POEMFOLDER + file, "r", encoding="UTF-8")
                    poems[file.split(".")[0]] = f.read()
                    f.close()

        # Initialization
        tk.Frame.__init__(self, root)
        Poems()
        root.winfo_toplevel().title("PoetTone")

        # Entire left side of window
        left_frame = tk.Frame(root, bg="gray", width=DEF_L, height=DEF_Y)
        left_frame.pack_propagate(False)

        # Table (paper bg)
        tableIMG = tk.PhotoImage(file="table.png")
        table = tk.Label(left_frame, image=tableIMG)
        table.image = tableIMG
        table.pack(fill=tk.BOTH, anchor=tk.CENTER)

        # Paper (text + scroll)
        paper = tk.Frame(table)
        paper.pack(fill=tk.NONE, anchor=tk.CENTER)

        text = tk.Text(paper, height=30, width=50, font=(TEXT_FONT, TEXT_SIZE), borderwidth=3)
        text.tag_configure("center-highlight", justify="center", background="yellow")
        text.tag_configure("center", justify="center")
        text.tag_add("center", 1.0, "end")

        text.grid(row=0, column=0, sticky=tk.NSEW)
        text.insert(tk.END, "Select a poem on the right.", "center")

        scroll = tk.Scrollbar(paper, borderwidth=3, command=text.yview)
        scroll.grid(row=0, column=1, sticky=tk.NSEW)
        text.config(yscrollcommand=scroll.set, state=tk.DISABLED)

        # Entire right side of window
        right_frame = tk.Frame(root, bg="white", width=150, height=DEF_Y)
        right_frame.pack_propagate(False)

        # Logo
        ico = tk.PhotoImage(file="icon.png")
        logo = tk.Label(right_frame, width=150, height=150, image=ico)
        logo.image = ico
        logo.pack(fill=tk.NONE, anchor=tk.N)

        # Dropdown
        ddLabel = tk.Label(right_frame, text="Now reading:", font=("High Tower Text", 17), bg="white")
        ddLabel.pack(fill=tk.NONE, anchor=tk.N, pady=(20, 0))

        var = tk.StringVar(root)
        var.set("Select a poem!")
        dropdown = tk.OptionMenu(right_frame, var, *list(poems.keys()))
        dropdown.config(bg="white", height=2, font=("High Tower Text", 14), indicatoron=False, wraplength=100)
        dropdown.pack(fill=tk.X, anchor=tk.N, pady=20)

        # Inserts text with highlighted index in poem
        def setText(poem):
            text.insert(tk.END, poem, "center")
            # TODO: MULTITHREADED HIGHLIGHTING
            # p = poem.split("\n")
            # for i in range(0, len(p)):
            #     if i == ind:
            #         text.insert(tk.END, p[i]+"\n", "center-highlight")
            #     else:
            #         text.insert(tk.END, p[i]+"\n", "center")

        # Change poem
        def changePoem(reset_cur_line = True):
            if reset_cur_line:
                self.cur_line = 0

            if var.get() in poems:
                # Set text
                text.config(state=tk.NORMAL)
                text.delete(1.0, tk.END)
                # setText(poems[var.get()], ind)
                setText(poems[var.get()])
                text.config(state=tk.DISABLED)

                # Kill old thread and spawn new
                if not self.thread is None:
                    self.thread.join()
                self.thread = PoemThread(poems[var.get()])
                self.thread.start()

        ddButton = tk.Button(right_frame, text="Change Poem", font=("High Tower Text", 14),
                             command=changePoem, bg="white", height=2)
        ddButton.pack(fill=tk.X, anchor=tk.N, pady=(0, 20))

        resetPoems = tk.Button(right_frame, text="Reset Poems", font=("High Tower Text", 14),
                             command=Poems, bg="white", height=2)
        resetPoems.pack(fill=tk.X, anchor=tk.N, pady=(0, 20))

        # Set up window
        left_frame.grid(row=0, column=0, sticky=tk.NW)
        right_frame.grid(row=0, column=1, sticky=tk.NE)

        # Main loop
        self.mainloop()

def main():
    # Main window
    window = tk.Tk()
    window.resizable(False, False)
    window.geometry(str(DEF_X)+"x"+str(DEF_Y))
    window.grid_rowconfigure(0, minsize=DEF_Y, weight=1)
    window.grid_columnconfigure(0, minsize=DEF_L)
    window.grid_columnconfigure(1, weight=1)

    a = App(window)

if __name__ == "__main__":
    main()