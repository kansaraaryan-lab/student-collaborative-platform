import customtkinter as ctk

from api_client import (
    get_rooms,
    create_room,
    update_room,
    delete_room
)


class RoomsPage(ctk.CTkFrame):

    # =========================================================
    # DESIGN SYSTEM
    # =========================================================

    BG = "#0B0D10"

    CARD = "#111418"
    CARD_HOVER = "#161A20"
    INPUT = "#0D1014"

    BORDER = "#242932"

    TEXT_PRIMARY = "#F5F7FA"
    TEXT_SECONDARY = "#9AA3B2"
    TEXT_MUTED = "#687180"

    ACCENT = "#7C3AED"
    ACCENT_HOVER = "#6D28D9"

    DANGER = "#EF4444"
    DANGER_HOVER = "#DC2626"

    SUCCESS = "#22C55E"

    # =========================================================
    # INITIALIZATION
    # =========================================================

    def __init__(self, parent):

        super().__init__(
            parent,
            fg_color=self.BG
        )

        self.grid_columnconfigure(
            0,
            weight=1
        )

        self.grid_rowconfigure(
            2,
            weight=1
        )

        self.build_ui()
        self.load_rooms()

    # =========================================================
    # MAIN UI
    # =========================================================

    def build_ui(self):

        # -----------------------------------------------------
        # HEADER
        # -----------------------------------------------------

        header = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=36,
            pady=(32, 0)
        )

        header.grid_columnconfigure(
            0,
            weight=1
        )

        title_area = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )

        title_area.grid(
            row=0,
            column=0,
            sticky="w"
        )

        ctk.CTkLabel(
            title_area,
            text="Rooms",
            font=("Segoe UI", 30, "bold"),
            text_color=self.TEXT_PRIMARY
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            title_area,
            text="Manage classrooms and student divisions.",
            font=("Segoe UI", 14),
            text_color=self.TEXT_SECONDARY
        ).pack(
            anchor="w",
            pady=(5, 0)
        )

        # -----------------------------------------------------
        # ADD BUTTON
        # -----------------------------------------------------

        ctk.CTkButton(
            header,
            text="+  Add Room",
            width=135,
            height=40,
            corner_radius=9,
            fg_color=self.ACCENT,
            hover_color=self.ACCENT_HOVER,
            font=("Segoe UI", 13, "bold"),
            command=self.open_add_room
        ).grid(
            row=0,
            column=1,
            sticky="e",
            pady=(4, 0)
        )

        # -----------------------------------------------------
        # ROOM LIST
        # -----------------------------------------------------

        self.room_list = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color=self.BORDER,
            scrollbar_button_hover_color="#343A46"
        )

        self.room_list.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=36,
            pady=(28, 28)
        )

    # =========================================================
    # LOAD ROOMS
    # =========================================================

    def load_rooms(self):

        for widget in self.room_list.winfo_children():
            widget.destroy()

        try:

            rooms = get_rooms()

            if not rooms:

                self.show_empty_state()

                return

            for room in rooms:

                self.create_room_card(
                    room
                )

        except Exception as error:

            self.show_error_state(
                str(error)
            )

    # =========================================================
    # ROOM CARD
    # =========================================================

    def create_room_card(
        self,
        room
    ):

        card = ctk.CTkFrame(
            self.room_list,
            fg_color=self.CARD,
            border_width=1,
            border_color=self.BORDER,
            corner_radius=14
        )

        card.pack(
            fill="x",
            pady=7
        )

        content = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        content.pack(
            fill="x",
            padx=22,
            pady=18
        )

        # -----------------------------------------------------
        # ROOM INFORMATION
        # -----------------------------------------------------

        info = ctk.CTkFrame(
            content,
            fg_color="transparent"
        )

        info.pack(
            side="left",
            fill="x",
            expand=True
        )

        room_id = room.get(
            "id",
            "-"
        )

        year = room.get(
            "year",
            "-"
        )

        branch = room.get(
            "branch",
            "-"
        )

        division = room.get(
            "division",
            "-"
        )

        ctk.CTkLabel(
            info,
            text=f"{branch}  •  Division {division}",
            font=("Segoe UI", 18, "bold"),
            text_color=self.TEXT_PRIMARY
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            info,
            text=f"Year {year}   •   Room ID {room_id}",
            font=("Segoe UI", 12),
            text_color=self.TEXT_SECONDARY
        ).pack(
            anchor="w",
            pady=(6, 0)
        )

        # -----------------------------------------------------
        # ROOM BADGE
        # -----------------------------------------------------

        badge = ctk.CTkLabel(
            content,
            text=f"  {branch}  ",
            height=26,
            corner_radius=7,
            fg_color="#7C3AED22",
            text_color="#A78BFA",
            font=("Segoe UI", 11, "bold")
        )

        badge.pack(
            side="left",
            padx=(15, 20)
        )

        # -----------------------------------------------------
        # ACTIONS
        # -----------------------------------------------------

        actions = ctk.CTkFrame(
            content,
            fg_color="transparent"
        )

        actions.pack(
            side="right"
        )

        ctk.CTkButton(
            actions,
            text="Edit",
            width=76,
            height=34,
            corner_radius=8,
            fg_color=self.CARD_HOVER,
            hover_color="#20252D",
            border_width=1,
            border_color=self.BORDER,
            text_color=self.TEXT_PRIMARY,
            font=("Segoe UI", 12, "bold"),
            command=lambda r=room: self.open_edit_room(r)
        ).pack(
            side="left",
            padx=4
        )

        ctk.CTkButton(
            actions,
            text="Delete",
            width=76,
            height=34,
            corner_radius=8,
            fg_color="#2A1518",
            hover_color="#3A1B20",
            text_color="#F87171",
            font=("Segoe UI", 12, "bold"),
            command=lambda rid=room_id: self.confirm_delete(rid)
        ).pack(
            side="left",
            padx=4
        )

    # =========================================================
    # EMPTY STATE
    # =========================================================

    def show_empty_state(self):

        card = ctk.CTkFrame(
            self.room_list,
            fg_color=self.CARD,
            border_width=1,
            border_color=self.BORDER,
            corner_radius=14
        )

        card.pack(
            fill="x",
            pady=30
        )

        ctk.CTkLabel(
            card,
            text="No rooms found",
            font=("Segoe UI", 20, "bold"),
            text_color=self.TEXT_PRIMARY
        ).pack(
            pady=(45, 7)
        )

        ctk.CTkLabel(
            card,
            text="Create your first classroom using the Add Room button.",
            font=("Segoe UI", 13),
            text_color=self.TEXT_SECONDARY
        ).pack(
            pady=(0, 45)
        )

    # =========================================================
    # ERROR STATE
    # =========================================================

    def show_error_state(
        self,
        error
    ):

        card = ctk.CTkFrame(
            self.room_list,
            fg_color=self.CARD,
            border_width=1,
            border_color="#3A2024",
            corner_radius=14
        )

        card.pack(
            fill="x",
            pady=30
        )

        ctk.CTkLabel(
            card,
            text="Unable to load rooms",
            font=("Segoe UI", 20, "bold"),
            text_color=self.TEXT_PRIMARY
        ).pack(
            pady=(35, 10)
        )

        ctk.CTkLabel(
            card,
            text=str(error),
            font=("Segoe UI", 13),
            text_color=self.TEXT_SECONDARY,
            wraplength=750,
            justify="center"
        ).pack(
            padx=30,
            pady=(0, 35)
        )

    # =========================================================
    # ADD / EDIT
    # =========================================================

    def open_add_room(self):

        self.open_room_dialog()

    def open_edit_room(
        self,
        room
    ):

        self.open_room_dialog(
            room
        )

    # =========================================================
    # ROOM DIALOG
    # =========================================================

    def open_room_dialog(
        self,
        room=None
    ):

        editing = room is not None

        dialog = ctk.CTkToplevel(
            self
        )

        dialog.title(
            "Edit Room"
            if editing
            else "Add Room"
        )

        dialog.geometry(
            "480x500"
        )

        dialog.resizable(
            False,
            False
        )

        dialog.configure(
            fg_color=self.BG
        )

        dialog.transient(
            self.winfo_toplevel()
        )

        dialog.grab_set()

        # -----------------------------------------------------
        # HEADER
        # -----------------------------------------------------

        ctk.CTkLabel(
            dialog,
            text="Edit Room" if editing else "Add Room",
            font=("Segoe UI", 24, "bold"),
            text_color=self.TEXT_PRIMARY
        ).pack(
            anchor="w",
            padx=32,
            pady=(30, 5)
        )

        ctk.CTkLabel(
            dialog,
            text="Enter classroom information.",
            font=("Segoe UI", 13),
            text_color=self.TEXT_SECONDARY
        ).pack(
            anchor="w",
            padx=32,
            pady=(0, 25)
        )

        # -----------------------------------------------------
        # YEAR
        # -----------------------------------------------------

        self.create_dialog_label(
            dialog,
            "Year"
        )

        year_entry = self.create_dialog_entry(
            dialog,
            "e.g. 2"
        )

        # -----------------------------------------------------
        # BRANCH
        # -----------------------------------------------------

        self.create_dialog_label(
            dialog,
            "Branch"
        )

        branch_entry = self.create_dialog_entry(
            dialog,
            "e.g. Computer Engineering"
        )

        # -----------------------------------------------------
        # DIVISION
        # -----------------------------------------------------

        self.create_dialog_label(
            dialog,
            "Division"
        )

        division_entry = self.create_dialog_entry(
            dialog,
            "e.g. A"
        )

        # -----------------------------------------------------
        # EXISTING VALUES
        # -----------------------------------------------------

        if editing:

            year_entry.insert(
                0,
                str(room.get("year", ""))
            )

            branch_entry.insert(
                0,
                str(room.get("branch", ""))
            )

            division_entry.insert(
                0,
                str(room.get("division", ""))
            )

        # -----------------------------------------------------
        # STATUS
        # -----------------------------------------------------

        status_label = ctk.CTkLabel(
            dialog,
            text="",
            font=("Segoe UI", 12),
            text_color=self.DANGER
        )

        status_label.pack(
            pady=(3, 4)
        )

        # -----------------------------------------------------
        # SUBMIT
        # -----------------------------------------------------

        def submit():

            year = year_entry.get().strip()
            branch = branch_entry.get().strip()
            division = division_entry.get().strip()

            if not year or not branch or not division:

                status_label.configure(
                    text="Please fill in all fields."
                )

                return

            try:

                year = int(year)

                if editing:

                    update_room(
                        room["id"],
                        year,
                        branch,
                        division
                    )

                else:

                    create_room(
                        year,
                        branch,
                        division
                    )

                dialog.destroy()

                self.load_rooms()

            except ValueError:

                status_label.configure(
                    text="Year must be a number."
                )

            except Exception as error:

                status_label.configure(
                    text=f"Operation failed: {error}"
                )

        ctk.CTkButton(
            dialog,
            text="Save Changes"
            if editing
            else "Add Room",
            height=42,
            corner_radius=9,
            fg_color=self.ACCENT,
            hover_color=self.ACCENT_HOVER,
            font=("Segoe UI", 13, "bold"),
            command=submit
        ).pack(
            fill="x",
            padx=32,
            pady=(12, 9)
        )

        # -----------------------------------------------------
        # CANCEL
        # -----------------------------------------------------

        ctk.CTkButton(
            dialog,
            text="Cancel",
            height=40,
            corner_radius=9,
            fg_color="transparent",
            hover_color=self.CARD_HOVER,
            border_width=1,
            border_color=self.BORDER,
            text_color=self.TEXT_SECONDARY,
            command=dialog.destroy
        ).pack(
            fill="x",
            padx=32
        )

    # =========================================================
    # DIALOG LABEL
    # =========================================================

    def create_dialog_label(
        self,
        parent,
        text
    ):

        ctk.CTkLabel(
            parent,
            text=text,
            font=("Segoe UI", 11, "bold"),
            text_color=self.TEXT_SECONDARY
        ).pack(
            anchor="w",
            padx=32,
            pady=(0, 5)
        )

    # =========================================================
    # DIALOG ENTRY
    # =========================================================

    def create_dialog_entry(
        self,
        parent,
        placeholder
    ):

        entry = ctk.CTkEntry(
            parent,
            height=42,
            corner_radius=9,
            fg_color=self.INPUT,
            border_color=self.BORDER,
            border_width=1,
            text_color=self.TEXT_PRIMARY,
            placeholder_text=placeholder,
            placeholder_text_color=self.TEXT_MUTED,
            font=("Segoe UI", 13)
        )

        entry.pack(
            fill="x",
            padx=32,
            pady=(0, 14)
        )

        return entry

    # =========================================================
    # DELETE CONFIRMATION
    # =========================================================

    def confirm_delete(
        self,
        room_id
    ):

        dialog = ctk.CTkToplevel(
            self
        )

        dialog.title(
            "Delete Room"
        )

        dialog.geometry(
            "420x240"
        )

        dialog.resizable(
            False,
            False
        )

        dialog.configure(
            fg_color=self.BG
        )

        dialog.transient(
            self.winfo_toplevel()
        )

        dialog.grab_set()

        # -----------------------------------------------------
        # WARNING
        # -----------------------------------------------------

        ctk.CTkLabel(
            dialog,
            text="Delete this room?",
            font=("Segoe UI", 22, "bold"),
            text_color=self.TEXT_PRIMARY
        ).pack(
            pady=(35, 8)
        )

        ctk.CTkLabel(
            dialog,
            text="This action cannot be undone.",
            font=("Segoe UI", 13),
            text_color=self.TEXT_SECONDARY
        ).pack()

        # -----------------------------------------------------
        # BUTTONS
        # -----------------------------------------------------

        buttons = ctk.CTkFrame(
            dialog,
            fg_color="transparent"
        )

        buttons.pack(
            pady=30
        )

        def remove():

            try:

                delete_room(
                    room_id
                )

                dialog.destroy()

                self.load_rooms()

            except Exception as error:

                dialog.destroy()

                self.show_delete_error(
                    error
                )

        ctk.CTkButton(
            buttons,
            text="Delete",
            width=110,
            height=38,
            corner_radius=8,
            fg_color=self.DANGER,
            hover_color=self.DANGER_HOVER,
            font=("Segoe UI", 12, "bold"),
            command=remove
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            buttons,
            text="Cancel",
            width=110,
            height=38,
            corner_radius=8,
            fg_color=self.CARD_HOVER,
            hover_color="#20252D",
            border_width=1,
            border_color=self.BORDER,
            text_color=self.TEXT_PRIMARY,
            command=dialog.destroy
        ).pack(
            side="left",
            padx=5
        )

    # =========================================================
    # DELETE ERROR
    # =========================================================

    def show_delete_error(
        self,
        error
    ):

        dialog = ctk.CTkToplevel(
            self
        )

        dialog.title(
            "Error"
        )

        dialog.geometry(
            "430x220"
        )

        dialog.resizable(
            False,
            False
        )

        dialog.configure(
            fg_color=self.BG
        )

        dialog.transient(
            self.winfo_toplevel()
        )

        ctk.CTkLabel(
            dialog,
            text="Could not delete room",
            font=("Segoe UI", 20, "bold"),
            text_color=self.TEXT_PRIMARY
        ).pack(
            pady=(30, 10)
        )

        ctk.CTkLabel(
            dialog,
            text=str(error),
            font=("Segoe UI", 13),
            text_color=self.TEXT_SECONDARY,
            wraplength=360,
            justify="center"
        ).pack(
            padx=25,
            pady=(0, 20)
        )

        ctk.CTkButton(
            dialog,
            text="OK",
            width=100,
            height=36,
            corner_radius=8,
            fg_color=self.ACCENT,
            hover_color=self.ACCENT_HOVER,
            command=dialog.destroy
        ).pack()