
import time
import tkinter as tk
from tkinter import font as tkfont

def slow_print(text):
    for char in text:
        time.sleep(0.025)
        import random


        class EscapeGame:
            BG = "#101522"
            PANEL = "#1a2233"
            TEXT = "#f2f5fc"
            MUTED = "#aab5c8"
            ACCENT = "#62e6c5"

            def __init__(self, root):
                self.root = root
                self.root.title("The Locked Room | Escape Game")
                self.root.geometry("900x620")
                self.root.minsize(760, 540)
                self.root.configure(bg=self.BG)
                self.inventory = []
                self.password = "4729"
                self.show_welcome()

            def show_welcome(self):
                self.welcome = tk.Frame(self.root, bg=self.BG)
                self.welcome.pack(fill="both", expand=True)
                self.canvas = tk.Canvas(self.welcome, bg=self.BG, highlightthickness=0)
                self.canvas.place(relwidth=1, relheight=1)
                self.canvas.bind("<Configure>", self.draw_door)

                card = tk.Frame(self.welcome, bg="#171f30", padx=48, pady=38)
                card.place(relx=.5, rely=.5, anchor="center")
                tk.Label(card, text="🔐", font=("Segoe UI Emoji", 38),
                         bg="#171f30", fg=self.ACCENT).pack(pady=(0, 8))
                tk.Label(card, text="THE LOCKED ROOM", font=("Segoe UI", 27, "bold"),
                         bg="#171f30", fg=self.TEXT).pack()
                tk.Label(card, text="A little mystery. One way out.",
                         font=("Segoe UI", 12), bg="#171f30", fg=self.MUTED).pack(pady=(8, 22))
                tk.Label(card, text="Find the clues, unlock the door, and make your escape.",
                         font=("Segoe UI", 10), bg="#171f30", fg="#d4dbea").pack(pady=(0, 24))
                tk.Button(card, text="ENTER THE GAME   →", command=self.start_animation,
                          font=("Segoe UI", 11, "bold"), bg=self.ACCENT, fg="#10201e",
                          activebackground="#8af2d8", relief="flat", padx=22, pady=12).pack()
                tk.Label(card, text="YOUR ADVENTURE IS WAITING", font=("Segoe UI", 8, "bold"),
                         bg="#171f30", fg="#78869d").pack(pady=(20, 0))
                self.stars = []
                for _ in range(32):
                    x, y = random.randrange(900), random.randrange(620)
                    dot = self.canvas.create_oval(x, y, x + 3, y + 3, fill="#34445b", outline="")
                    self.stars.append(dot)
                self.animate_stars()

            def draw_door(self, event):
                self.canvas.delete("door")
                w, h = event.width, event.height
                self.canvas.create_rectangle(w * .77, h * .2, w * .91, h * .82,
                                             outline="#34445b", width=2, tags="door")
                self.canvas.create_oval(w * .87, h * .49, w * .885, h * .515,
                                        fill=self.ACCENT, outline="", tags="door")

            def animate_stars(self):
                if not self.welcome.winfo_exists():
                    return
                for star in self.stars:
                    self.canvas.move(star, 0, -1)
                    if self.canvas.coords(star)[1] < 0:
                        self.canvas.move(star, 0, self.canvas.winfo_height() + 4)
                self.root.after(70, self.animate_stars)

            def start_animation(self):
                self.welcome.destroy()
                self.scene = tk.Canvas(self.root, bg=self.BG, highlightthickness=0)
                self.scene.pack(fill="both", expand=True)
                self.scene.create_text(450, 62, text="ENTERING THE GAME",
                                       fill=self.ACCENT, font=("Segoe UI", 11, "bold"))
                self.scene.create_text(450, 92, text="The room is waiting...",
                                       fill=self.MUTED, font=("Segoe UI", 14))
                self.frame = 0
                self.animate_entry()

            def animate_entry(self):
                self.scene.delete("room")
                w = max(self.scene.winfo_width(), 760)
                h = max(self.scene.winfo_height(), 540)
                floor = h * .78
                self.scene.create_rectangle(0, floor, w, h, fill="#172131", outline="", tags="room")
                self.scene.create_line(0, floor, w, floor, fill="#37445a", width=2, tags="room")
                self.scene.create_rectangle(w * .7, h * .22, w * .84, floor,
                                            fill="#29364b", outline="#708098", width=3, tags="room")
                swing = min(self.frame / 24, 1)
                self.scene.create_polygon(w * .7, h * .22, w * (.84 - .12 * swing), h * .28,
                                          w * (.84 - .12 * swing), floor - 12, w * .7, floor,
                                          fill="#33445a", outline="#718097", width=2, tags="room")
                x = min(w * .2 + self.frame * 9, w * .78)
                self.scene.create_oval(x - 16, floor - 112, x + 16, floor - 80,
                                       fill=self.ACCENT, outline="", tags="room")
                self.scene.create_line(x, floor - 80, x, floor - 30, fill="#dce6f4", width=8, tags="room")
                self.scene.create_line(x, floor - 62, x - 18, floor - 42, fill="#dce6f4", width=5, tags="room")
                self.scene.create_line(x, floor - 62, x + 18, floor - 42, fill="#dce6f4", width=5, tags="room")
                self.scene.create_line(x, floor - 30, x - 13, floor, fill="#dce6f4", width=6, tags="room")
                self.scene.create_line(x, floor - 30, x + 13, floor, fill="#dce6f4", width=6, tags="room")
                self.frame += 1
                if self.frame < 48:
                    self.root.after(35, self.animate_entry)
                else:
                    self.root.after(250, self.show_game)

            def show_game(self):
                self.scene.destroy()
                self.game = tk.Frame(self.root, bg=self.BG, padx=28, pady=22)
                self.game.pack(fill="both", expand=True)
                header = tk.Frame(self.game, bg=self.BG)
                header.pack(fill="x", pady=(0, 18))
                tk.Label(header, text="🔐  THE LOCKED ROOM", font=("Segoe UI", 18, "bold"),
                         bg=self.BG, fg=self.TEXT).pack(side="left")
                self.inventory_label = tk.Label(header, text="INVENTORY  ·  EMPTY",
                                                font=("Segoe UI", 9, "bold"), bg=self.BG, fg=self.ACCENT)
                self.inventory_label.pack(side="right", pady=8)

                content = tk.Frame(self.game, bg=self.BG)
                content.pack(fill="both", expand=True)
                left = tk.Frame(content, bg=self.PANEL, padx=18, pady=18)
                left.pack(side="left", fill="y", padx=(0, 16))
                tk.Label(left, text="WHAT WILL YOU DO?", font=("Segoe UI", 10, "bold"),
                         bg=self.PANEL, fg=self.MUTED).pack(anchor="w", pady=(0, 12))
                for label, command in (("⌕   Search the room", self.search_room),
                                       ("▤   Inspect the desk", self.inspect_desk),
                                       ("▣   Inspect the door", self.inspect_door),
                                       ("▤   Check inventory", self.check_inventory)):
                    tk.Button(left, text=label, command=command, anchor="w", width=22,
                              font=("Segoe UI", 10), bg="#253147", fg=self.TEXT,
                              activebackground="#34445d", activeforeground=self.TEXT,
                              relief="flat", padx=11, pady=12).pack(fill="x", pady=5)
                tk.Button(left, text="✕   Quit game", command=self.root.destroy, anchor="w",
                          font=("Segoe UI", 10), bg="#352a38", fg="#f1c5cb",
                          activebackground="#493440", relief="flat", padx=11, pady=12).pack(fill="x", pady=(16, 5))

                right = tk.Frame(content, bg=self.PANEL, padx=20, pady=18)
                right.pack(side="left", fill="both", expand=True)
                tk.Label(right, text="YOUR STORY", font=("Segoe UI", 10, "bold"),
                         bg=self.PANEL, fg=self.MUTED).pack(anchor="w")
                self.story = tk.Text(right, wrap="word", font=("Segoe UI", 11), bg=self.PANEL,
                                     fg=self.TEXT, insertbackground=self.TEXT, relief="flat",
                                     borderwidth=0, padx=0, pady=12)
                self.story.pack(fill="both", expand=True)
                self.story.configure(state="disabled")
                self.write_story("You wake up in a mysterious locked room. A heavy door stands across from you. Find a way to escape!")

                tk.Label(right, text="4-DIGIT DOOR CODE", font=("Segoe UI", 9, "bold"),
                         bg=self.PANEL, fg=self.MUTED).pack(anchor="w", pady=(12, 7))
                row = tk.Frame(right, bg=self.PANEL)
                row.pack(fill="x")
                self.code_entry = tk.Entry(row, font=("Segoe UI", 12), show="•", bg="#111827",
                                           fg=self.TEXT, insertbackground=self.TEXT, relief="flat", width=18)
                self.code_entry.pack(side="left", ipady=9, padx=(0, 9))
                tk.Button(row, text="UNLOCK  →", command=self.enter_password,
                          font=("Segoe UI", 9, "bold"), bg=self.ACCENT, fg="#10201e",
                          activebackground="#8af2d8", relief="flat", padx=15, pady=10).pack(side="left")
                self.code_entry.bind("<Return>", lambda _event: self.enter_password())

            def write_story(self, message):
                self.story.configure(state="normal")
                self.story.insert("end", "\n" + message + "\n")
                self.story.see("end")
                self.story.configure(state="disabled")

            def update_inventory(self):
                contents = "  ·  ".join(item.upper() for item in self.inventory) or "EMPTY"
                self.inventory_label.configure(text="INVENTORY  ·  " + contents)

            def search_room(self):
                if "paper" in self.inventory:
                    self.write_story("You have already searched the room. There is nothing else to find.")
                else:
                    self.inventory.append("paper")
                    self.update_inventory()
                    self.write_story("You find a mysterious paper. It contains a strange clue: 4 - 7 - 2 - 9.")

            def inspect_desk(self):
                if "key" in self.inventory:
                    self.write_story("The desk is empty now. You already took the small key.")
                else:
                    self.inventory.append("key")
                    self.update_inventory()
                    self.write_story("You discover a small key inside the desk!")

            def inspect_door(self):
                if "key" in self.inventory:
                    self.write_story("The key unlocks a small box near the door. Inside, you find a keypad.")
                else:
                    self.write_story("The door is locked. You need to find a key.")

            def check_inventory(self):
                items = ", ".join(self.inventory) if self.inventory else "Empty"
                self.write_story("Your inventory: " + items + ".")

            def enter_password(self):
                if "paper" not in self.inventory:
                    self.write_story("You need to find a clue first!")
                    return
                answer = self.code_entry.get().strip()
                self.code_entry.delete(0, "end")
                if answer == self.password:
                    self.write_story("🔓 ACCESS GRANTED! The door opens slowly... Congratulations, you escaped!")
                    self.code_entry.configure(state="disabled")
                else:
                    self.write_story("❌ Wrong password! Try again.")


        if __name__ == "__main__":
            root = tk.Tk()
            EscapeGame(root)
            root.mainloop()

slow_print("Welcome to the Escape Game! Your goal is to find clues and escape the locked room. Good luck!")