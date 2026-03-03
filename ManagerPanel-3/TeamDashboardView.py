from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from TkUtils import TkUtils as ut
from ErrorView import ErrorView
from model.exception.FillException import FillException
from model.exception.InvalidSigningException import InvalidSigningException


class TeamDashboardView:
    def __init__(self, league):
        self.league = league
        self.manager = league.get_logged_in_manager()
        self.team = self.manager.get_team()
        self.window = None
        self.player_tree = None
        self.unsign_btn = None
        self.selected_player = None
        self.jersey_labels = {}
        self.active_players = {}
        self.jersey_size = (40, 40)
        self.sign_btn = None

    def show(self):
        self.window = ut.root()
        self.window.title("Team Dashboard")


        ut.image(self.window, "image/banner.png").pack() #Banner
        self.separator()


        team_name_lbl = ut.label(self.window, str(self.team))
        team_name_lbl.config(font="Arial 12 bold", bg="#d9d9d9")
        team_name_lbl.pack(pady=(0, 5))
        self.separator()


        sign_frame = Frame(self.window, bg="#d9d9d9")
        sign_frame.pack(pady=(5, 10))

        sign_player_lbl = ut.label(sign_frame, "Sign a new player:")
        sign_player_lbl.config(bg="#d9d9d9")
        sign_player_lbl.pack(side=LEFT, padx=(0, 5))

        self.sign_entry = Entry(sign_frame, width=25)
        self.sign_entry.pack(side=LEFT, padx=(0, 10), ipady=3)
        self.sign_entry.bind("<KeyRelease>", self.text_entered)

        self.sign_btn = ut.button(sign_frame, "Sign", callback=self.sign_player)
        self.sign_btn.config(state=DISABLED)
        self.sign_btn.pack(side=LEFT)

        self.window.bind("<Return>", self.enter_clicked)


        main_frame = Frame(self.window, bg="#d9d9d9")
        main_frame.pack(padx=10)

        # Using ttk.Style() to customize the font of the headings and the rows within the treeview
        style = ttk.Style()
        style.configure("Treeview", font="Helvetica 10")
        style.configure("Treeview.Heading", font="Helvetica 10 bold")

        columns = ("Name", "Position")
        self.player_tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=11)
        for column in columns:
            self.player_tree.heading(column, text=column)
            self.player_tree.column("Name", width=180, anchor=CENTER)
            self.player_tree.column("Position", width=100, anchor=CENTER)
        self.player_tree.grid(row=0, column=0, padx=(0, 10))
        self.player_tree.bind("<<TreeviewSelect>>", self.treeview_player_selected)
        self.player_tree.bind("<Button-1>", self.treeview_player_deselected)  # Button-1 represents the left mouse click
        self.populate_players()

        active_team_frame = Frame(main_frame, padx=1, pady=1)
        active_team_frame.grid(row=0, column=1)

        heading = Label(active_team_frame, text="Active Team", fg="#f6a192", bg="#3b3b3b", font="Arial 12 bold")
        heading.pack(expand=True, fill=X)

        grid_frame = Frame(active_team_frame, bg="white")
        grid_frame.pack()

        # list of positions
        positions = ["Fullback", "Wing", "Centre", "Halfback", "Forward"]

        # dict to store the coordinate values for each position
        layout = {
            "Fullback": (0, 1),
            "Wing": (1, 0),
            "Centre": (1, 1),
            "Halfback": (1, 2),
            "Forward": (2, 1)
        }

        for position in positions:
            img = ImageTk.PhotoImage(Image.open("image/none.png").resize(self.jersey_size))
            lbl = Label(grid_frame, image=img, bg="white")
            lbl.image = img
            lbl.grid(row=layout[position][0], column=layout[position][1], padx=10, pady=10)
            lbl.bind("<Button-1>", self.jersey_clicked)
            lbl.bind("<Enter>", self.jersey_hover)
            lbl.bind("<Leave>", self.cursor_left_jersey)
            lbl.position = position
            self.jersey_labels[position] = lbl
            self.active_players[position] = None

        # Bottom buttons
        btn_frame = Frame(self.window)
        self.unsign_btn = ut.button(btn_frame, "Unsign", callback=self.unsign_player)
        self.unsign_btn.config(state=DISABLED)
        self.unsign_btn.pack(side=LEFT, expand=True, fill=X)
        ut.button(btn_frame, "Close", callback=self.close).pack(side=LEFT, expand=True, fill=X)
        btn_frame.pack(fill=X, pady=(5, 0))

        self.window.mainloop()

    def separator(self):
        return ut.separator(self.window).pack(fill=X, pady=(0, 10))

    def text_entered(self, event):
        # If text is entered in the entry box, we set the state=NORMAL, otherwise state=DISABLED
        if self.sign_entry.get().strip():
            self.sign_btn.config(state=NORMAL)
        else:
            self.sign_btn.config(state=DISABLED)

    def sign_player(self):
        name = self.sign_entry.get()
        player = self.league.get_players().player(name)

        if not name:
            return

        if not player:
            ErrorView("Player does not exist within the league").show()
            raise InvalidSigningException("Player does not exist within the league")

        elif player.get_team() == self.team:
            ErrorView(f"{player.get_full_name()} is already signed to your team").show()
            raise InvalidSigningException(f"{player.get_full_name()} is already signed to your team")

        elif player.get_team() and player.get_team() != self.team:
            ErrorView(f"Cannot sign {player.get_full_name()}, player is already signed to {player.get_team()}").show()
            raise InvalidSigningException(f"Cannot sign {player.get_full_name()}, player is already signed to {player.get_team()}")

        player.set_team(self.team)
        self.team.get_all_players().add(player)
        self.populate_players()

    def enter_clicked(self, event):
        self.sign_player()

    def populate_players(self):
        for item in self.player_tree.get_children():
            self.player_tree.delete(item)
        for player in self.team.get_all_players().get_players():
            name = player.get_full_name()
            pos = str(player.get_position())
            self.player_tree.insert("", END, values=(name, pos))

    def treeview_player_selected(self, event):
        selected = self.player_tree.selection()
        if selected:
            self.selected_player = self.player_tree.item(selected[0])["values"][0]
            self.unsign_btn.config(state=NORMAL)
        else:
            self.selected_player = None
            self.unsign_btn.config(state=DISABLED)

    def treeview_player_deselected(self, event):
        item_id = self.player_tree.identify_row(event.y)
        # Here, event.y is the y coordinate of where the mouse was clicked.
        # It is used to by player_tree.identify_row() to find out which row was de-selected.
        if item_id and item_id in self.player_tree.selection():
            self.player_tree.selection_remove(item_id)
            self.selected_player = None
            self.unsign_btn.config(state=DISABLED)
            return "break"
            # return "break" is needed to prevent other default actions from taking place, specifically re-selecting the row

    def set_jersey_image(self, position, path):
        lbl = self.jersey_labels[position]
        img = ImageTk.PhotoImage(Image.open(path).resize(self.jersey_size))
        lbl.config(image=img)
        lbl.image = img

    def unsign_player(self):
        if not self.selected_player or self.team is None:
            return

        player_to_remove = self.league.get_players().player(self.selected_player)
        if not player_to_remove:
            return

        if player_to_remove in self.active_players.values():
            ErrorView(f"Cannot remove {player_to_remove.get_full_name()}, player is in the active team").show()
            raise InvalidSigningException(f"Cannot remove {player_to_remove.get_full_name()}, player is in the active team")

        player_to_remove.set_team(None)
        self.team.get_all_players().remove(player_to_remove)
        self.populate_players()
        self.unsign_btn.config(state=DISABLED)
        self.selected_player = None

    def jersey_clicked(self, event):
        position = event.widget.position
        self.handle_jersey_click(position)

    def handle_jersey_click(self, position):
        if self.active_players.get(position) is not None:
            # Remove from active team
            self.active_players[position] = None
            self.set_jersey_image(position, "image/none.png")
            return

        if not self.selected_player:
            return

        player_obj = self.league.get_players().player(self.selected_player)
        if not player_obj:
            return

        if player_obj in self.active_players.values():
            ErrorView(f"{player_obj.get_full_name()} is already in active playing team").show()
            raise FillException(f"{player_obj.get_full_name()} is already in active playing team")

        team_img = f"image/{self.team.get_team_name().lower()}.png"
        self.set_jersey_image(position, team_img)
        self.active_players[position] = player_obj
        self.jersey_hover()

    def jersey_hover(self, event):
        position = event.widget.position
        player = self.active_players.get(position)
        if player:
            text = player.__str__()
        else:
            text = "Unallocated"
        self.hover_label = Label(self.window, text=text, bg="#3b3b3b", fg="white", font="Arial 8 bold")
        self.hover_label.place(x=event.x_root - self.window.winfo_rootx() - 25,
                               y=event.y_root - self.window.winfo_rooty() + 10)

    def cursor_left_jersey(self, event):
        if self.hover_label:
            self.hover_label.destroy()
            self.hover_label = None

    def close(self):
        self.window.destroy()

