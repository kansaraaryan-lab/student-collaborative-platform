import customtkinter as ctk
from tkinter import messagebox

from api_client import (
    get_students,
    get_events,
    get_teams,
    create_team,
    get_team_members,
    add_team_member,
    remove_team_member,
)


class TeamBuilderPage(ctk.CTkFrame):

    BG = "#0B0D10"
    CARD = "#111418"
    CARD_HOVER = "#161A20"
    BORDER = "#242932"

    TEXT_PRIMARY = "#F5F7FA"
    TEXT_SECONDARY = "#9AA3B2"
    TEXT_MUTED = "#687180"

    ACCENT = "#7C3AED"
    ACCENT_HOVER = "#6D28D9"

    DANGER = "#EF4444"
    INFO = "#3B82F6"

    def __init__(self, parent):

        super().__init__(
            parent,
            fg_color=self.BG
        )

        self.students = []
        self.events = []
        self.teams = []

        self.student_map = {}
        self.event_map = {}
        self.team_map = {}

        self.create_ui()
        self.load_data()

    # =========================================================
    # UI
    # =========================================================

    def create_ui(self):

        header = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        header.pack(
            fill="x",
            padx=35,
            pady=(30, 0)
        )

        title_row = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )

        title_row.pack(
            fill="x"
        )

        title_section = ctk.CTkFrame(
            title_row,
            fg_color="transparent"
        )

        title_section.pack(
            side="left",
            fill="x",
            expand=True
        )

        ctk.CTkLabel(
            title_section,
            text="Team Builder",
            font=("Segoe UI", 30, "bold"),
            text_color=self.TEXT_PRIMARY
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            title_section,
            text="Create teams and manage members for events and projects.",
            font=("Segoe UI", 14),
            text_color=self.TEXT_SECONDARY
        ).pack(
            anchor="w",
            pady=(5, 0)
        )

        ctk.CTkButton(
            title_row,
            text="+ Create Team",
            width=140,
            height=40,
            corner_radius=9,
            fg_color=self.ACCENT,
            hover_color=self.ACCENT_HOVER,
            font=("Segoe UI", 13, "bold"),
            command=self.open_create_team
        ).pack(
            side="right"
        )

        controls = ctk.CTkFrame(
            self,
            fg_color=self.CARD,
            border_width=1,
            border_color=self.BORDER,
            corner_radius=12
        )

        controls.pack(
            fill="x",
            padx=35,
            pady=25
        )

        self.team_dropdown = ctk.CTkComboBox(
            controls,
            width=350,
            height=40,
            values=["Loading teams..."],
            command=self.team_selected
        )

        self.team_dropdown.pack(
            side="left",
            padx=12,
            pady=12
        )

        self.content = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color=self.BORDER,
            scrollbar_button_hover_color="#343A46"
        )

        self.content.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=(0, 25)
        )

    # =========================================================
    # LOAD DATA
    # =========================================================

    def load_data(self):

        try:

            self.students = get_students()
            self.events = get_events()
            self.teams = get_teams()

            self.student_map = {
                f"{student['name']} • {student['college_email']}":
                student["id"]
                for student in self.students
            }

            self.event_map = {
                event["title"]: event["id"]
                for event in self.events
            }

            self.team_map = {
                team["name"]: team["id"]
                for team in self.teams
            }

            team_names = list(
                self.team_map.keys()
            )

            if team_names:

                self.team_dropdown.configure(
                    values=team_names
                )

                self.team_dropdown.set(
                    team_names[0]
                )

                self.load_team(
                    self.team_map[team_names[0]]
                )

            else:

                self.team_dropdown.configure(
                    values=["No teams created"]
                )

                self.team_dropdown.set(
                    "No teams created"
                )

                self.show_no_team()

        except Exception as error:

            self.show_error(
                f"Unable to load team data:\n\n{error}"
            )

    # =========================================================
    # TEAM SELECTION
    # =========================================================

    def team_selected(self, team_name):

        team_id = self.team_map.get(
            team_name
        )

        if team_id:
            self.load_team(team_id)

    # =========================================================
    # LOAD TEAM
    # =========================================================

    def load_team(self, team_id):

        for widget in self.content.winfo_children():
            widget.destroy()

        try:

            members = get_team_members(
                team_id
            )

            team = next(
                (
                    team
                    for team in self.teams
                    if team["id"] == team_id
                ),
                None
            )

            if not team:
                return

            self.create_team_header(
                team,
                members
            )

            self.create_members_section(
                team_id,
                members
            )

        except Exception as error:

            self.show_error(
                f"Unable to load team:\n\n{error}"
            )

    # =========================================================
    # TEAM HEADER
    # =========================================================

    def create_team_header(
        self,
        team,
        members
    ):

        card = ctk.CTkFrame(
            self.content,
            fg_color=self.CARD,
            border_width=1,
            border_color=self.BORDER,
            corner_radius=15
        )

        card.pack(
            fill="x",
            pady=(0, 20)
        )

        top = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        top.pack(
            fill="x",
            padx=25,
            pady=(22, 5)
        )

        ctk.CTkLabel(
            top,
            text=team.get(
                "name",
                "Unnamed Team"
            ),
            font=("Segoe UI", 24, "bold"),
            text_color=self.TEXT_PRIMARY
        ).pack(
            side="left"
        )

        status = team.get(
            "status",
            "active"
        )

        ctk.CTkLabel(
            top,
            text=f" {status.upper()} ",
            font=("Segoe UI", 10, "bold"),
            text_color="#22C55E",
            fg_color="#22C55E22",
            corner_radius=7
        ).pack(
            side="right"
        )

        description = team.get(
            "description",
            ""
        )

        if not description:
            description = "No description provided."

        ctk.CTkLabel(
            card,
            text=description,
            font=("Segoe UI", 13),
            text_color=self.TEXT_SECONDARY,
            wraplength=850,
            justify="left"
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 12)
        )

        max_members = team.get(
            "max_members",
            "-"
        )

        member_count = len(
            members
        )

        ctk.CTkLabel(
            card,
            text=f"Members: {member_count} / {max_members}",
            font=("Segoe UI", 12),
            text_color=self.TEXT_MUTED
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 20)
        )

    # =========================================================
    # MEMBERS
    # =========================================================

    def create_members_section(
        self,
        team_id,
        members
    ):

        header = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        header.pack(
            fill="x",
            pady=(0, 10)
        )

        ctk.CTkLabel(
            header,
            text="Team Members",
            font=("Segoe UI", 20, "bold"),
            text_color=self.TEXT_PRIMARY
        ).pack(
            side="left"
        )

        ctk.CTkButton(
            header,
            text="+ Add Member",
            width=130,
            height=38,
            corner_radius=8,
            fg_color=self.ACCENT,
            hover_color=self.ACCENT_HOVER,
            command=lambda:
                self.open_add_member(team_id)
        ).pack(
            side="right"
        )

        if not members:

            empty_card = ctk.CTkFrame(
                self.content,
                fg_color=self.CARD,
                border_width=1,
                border_color=self.BORDER,
                corner_radius=12
            )

            empty_card.pack(
                fill="x",
                pady=10
            )

            ctk.CTkLabel(
                empty_card,
                text="No members in this team yet.",
                font=("Segoe UI", 15),
                text_color=self.TEXT_SECONDARY
            ).pack(
                pady=30
            )

            return

        for member in members:

            self.create_member_card(
                team_id,
                member
            )

    # =========================================================
    # MEMBER CARD
    # =========================================================

    def create_member_card(
        self,
        team_id,
        member
    ):

        card = ctk.CTkFrame(
            self.content,
            fg_color=self.CARD,
            border_width=1,
            border_color=self.BORDER,
            corner_radius=12
        )

        card.pack(
            fill="x",
            pady=5
        )

        student_id = member.get(
            "student_id"
        )

        student = next(
            (
                student
                for student in self.students
                if student["id"] == student_id
            ),
            None
        )

        if student:

            student_name = student.get(
                "name",
                "Student"
            )

            student_email = student.get(
                "college_email",
                ""
            )

        else:

            student_name = f"Student #{student_id}"
            student_email = ""

        info = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        info.pack(
            side="left",
            padx=20,
            pady=15
        )

        ctk.CTkLabel(
            info,
            text=student_name,
            font=("Segoe UI", 16, "bold"),
            text_color=self.TEXT_PRIMARY
        ).pack(
            anchor="w"
        )

        if student_email:

            ctk.CTkLabel(
                info,
                text=student_email,
                font=("Segoe UI", 12),
                text_color=self.TEXT_SECONDARY
            ).pack(
                anchor="w",
                pady=(3, 0)
            )

        ctk.CTkButton(
            card,
            text="Remove",
            width=90,
            height=35,
            corner_radius=7,
            fg_color=self.DANGER,
            hover_color="#DC2626",
            command=lambda:
                self.remove_member(
                    team_id,
                    student_id
                )
        ).pack(
            side="right",
            padx=20
        )

    # =========================================================
    # CREATE TEAM
    # =========================================================

    def open_create_team(self):

        modal = ctk.CTkToplevel(
            self
        )

        modal.title(
            "Create Team"
        )

        modal.geometry(
            "470x550"
        )

        modal.resizable(
            False,
            False
        )

        modal.transient(
            self.winfo_toplevel()
        )

        modal.grab_set()

        ctk.CTkLabel(
            modal,
            text="Create Team",
            font=("Segoe UI", 24, "bold")
        ).pack(
            pady=(25, 20)
        )

        # Team name

        ctk.CTkLabel(
            modal,
            text="Team Name",
            font=("Segoe UI", 12, "bold")
        ).pack(
            anchor="w",
            padx=65
        )

        name_entry = ctk.CTkEntry(
            modal,
            width=320,
            height=40,
            placeholder_text="Enter team name"
        )

        name_entry.pack(
            pady=(5, 12)
        )

        # Description

        ctk.CTkLabel(
            modal,
            text="Description",
            font=("Segoe UI", 12, "bold")
        ).pack(
            anchor="w",
            padx=65
        )

        description_entry = ctk.CTkEntry(
            modal,
            width=320,
            height=40,
            placeholder_text="Enter description"
        )

        description_entry.pack(
            pady=(5, 12)
        )

        # Event

        ctk.CTkLabel(
            modal,
            text="Event",
            font=("Segoe UI", 12, "bold")
        ).pack(
            anchor="w",
            padx=65
        )

        event_names = list(
            self.event_map.keys()
        )

        if event_names:

            event_dropdown = ctk.CTkComboBox(
                modal,
                width=320,
                height=40,
                values=event_names
            )

            event_dropdown.pack(
                pady=(5, 12)
            )

            event_dropdown.set(
                event_names[0]
            )

        else:

            event_dropdown = None

            ctk.CTkLabel(
                modal,
                text="No events available.",
                text_color=self.TEXT_SECONDARY
            ).pack(
                pady=10
            )

        # Max members

        ctk.CTkLabel(
            modal,
            text="Maximum Members",
            font=("Segoe UI", 12, "bold")
        ).pack(
            anchor="w",
            padx=65
        )

        max_members_dropdown = ctk.CTkComboBox(
            modal,
            width=320,
            height=40,
            values=[
                str(number)
                for number in range(2, 21)
            ]
        )

        max_members_dropdown.pack(
            pady=(5, 20)
        )

        max_members_dropdown.set(
            "4"
        )

        # Save

        def save_team():

            name = name_entry.get().strip()

            description = (
                description_entry
                .get()
                .strip()
            )

            if not name:

                messagebox.showerror(
                    "Validation Error",
                    "Please enter a team name.",
                    parent=modal
                )

                return

            event_id = None

            if event_dropdown:

                event_id = self.event_map.get(
                    event_dropdown.get()
                )

            try:

                max_members = int(
                    max_members_dropdown.get()
                )

            except ValueError:

                messagebox.showerror(
                    "Validation Error",
                    "Maximum members must be a number.",
                    parent=modal
                )

                return

            if max_members < 2 or max_members > 20:

                messagebox.showerror(
                    "Validation Error",
                    "Maximum members must be between 2 and 20.",
                    parent=modal
                )

                return

            try:

                create_team(
                    name,
                    description,
                    event_id,
                    max_members
                )

                modal.destroy()

                self.load_data()

            except Exception as error:

                messagebox.showerror(
                    "API Error",
                    str(error),
                    parent=modal
                )

        ctk.CTkButton(
            modal,
            text="Create Team",
            width=320,
            height=42,
            corner_radius=8,
            fg_color=self.ACCENT,
            hover_color=self.ACCENT_HOVER,
            command=save_team
        ).pack()

    # =========================================================
    # ADD MEMBER
    # =========================================================

    def open_add_member(self, team_id):

        modal = ctk.CTkToplevel(
            self
        )

        modal.title(
            "Add Team Member"
        )

        modal.geometry(
            "450x300"
        )

        modal.resizable(
            False,
            False
        )

        modal.transient(
            self.winfo_toplevel()
        )

        modal.grab_set()

        ctk.CTkLabel(
            modal,
            text="Add Team Member",
            font=("Segoe UI", 22, "bold")
        ).pack(
            pady=(30, 20)
        )

        student_names = list(
            self.student_map.keys()
        )

        if not student_names:

            ctk.CTkLabel(
                modal,
                text="No students available.",
                text_color=self.TEXT_SECONDARY
            ).pack(
                pady=30
            )

            return

        student_dropdown = ctk.CTkComboBox(
            modal,
            width=320,
            height=40,
            values=student_names
        )

        student_dropdown.pack(
            pady=10
        )

        student_dropdown.set(
            student_names[0]
        )

        def add_member():

            student_id = self.student_map.get(
                student_dropdown.get()
            )

            if not student_id:
                return

            try:

                add_team_member(
                    team_id,
                    student_id
                )

                modal.destroy()

                self.load_team(
                    team_id
                )

            except Exception as error:

                messagebox.showerror(
                    "API Error",
                    str(error),
                    parent=modal
                )

        ctk.CTkButton(
            modal,
            text="Add Member",
            width=320,
            height=42,
            corner_radius=8,
            fg_color=self.ACCENT,
            hover_color=self.ACCENT_HOVER,
            command=add_member
        ).pack(
            pady=25
        )

    # =========================================================
    # REMOVE MEMBER
    # =========================================================

    def remove_member(
        self,
        team_id,
        student_id
    ):

        if not student_id:
            return

        confirmed = messagebox.askyesno(
            "Remove Member",
            "Are you sure you want to remove this member?"
        )

        if not confirmed:
            return

        try:

            remove_team_member(
                team_id,
                student_id
            )

            self.load_team(
                team_id
            )

        except Exception as error:

            self.show_error(
                f"Unable to remove member:\n\n{error}"
            )

    # =========================================================
    # EMPTY
    # =========================================================

    def show_no_team(self):

        card = ctk.CTkFrame(
            self.content,
            fg_color=self.CARD,
            border_width=1,
            border_color=self.BORDER,
            corner_radius=15
        )

        card.pack(
            fill="x",
            pady=30
        )

        ctk.CTkLabel(
            card,
            text="No teams created yet.",
            font=("Segoe UI", 20, "bold"),
            text_color=self.TEXT_PRIMARY
        ).pack(
            pady=(35, 5)
        )

        ctk.CTkLabel(
            card,
            text="Create a team to start collaborating.",
            font=("Segoe UI", 13),
            text_color=self.TEXT_SECONDARY
        ).pack(
            pady=(0, 35)
        )

    # =========================================================
    # ERROR
    # =========================================================

    def show_error(self, message):

        window = ctk.CTkToplevel(
            self
        )

        window.title(
            "Team Builder"
        )

        window.geometry(
            "450x250"
        )

        window.resizable(
            False,
            False
        )

        window.transient(
            self.winfo_toplevel()
        )

        ctk.CTkLabel(
            window,
            text=message,
            wraplength=380,
            font=("Segoe UI", 14),
            text_color=self.TEXT_PRIMARY
        ).pack(
            padx=25,
            pady=(50, 25)
        )

        ctk.CTkButton(
            window,
            text="OK",
            width=100,
            command=window.destroy
        ).pack()