import customtkinter as ctk

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

    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color="transparent"
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

        # ---------- Header ----------

        ctk.CTkLabel(
            self,
            text="Team Builder",
            font=("Arial", 30, "bold")
        ).pack(
            anchor="w",
            padx=35,
            pady=(30, 5)
        )

        ctk.CTkLabel(
            self,
            text="Create teams and manage members for events and projects.",
            font=("Arial", 14)
        ).pack(
            anchor="w",
            padx=35
        )

        # ---------- Controls ----------

        controls = ctk.CTkFrame(
            self,
            fg_color="transparent"
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
            padx=(0, 10)
        )

        ctk.CTkButton(
            controls,
            text="+ Create Team",
            width=140,
            height=40,
            command=self.open_create_team
        ).pack(
            side="left"
        )

        # ---------- Content ----------

        self.content = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
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

            # Student mapping

            self.student_map = {
                f"{student['name']} • {student['college_email']}":
                student["id"]
                for student in self.students
            }

            # Event mapping

            self.event_map = {
                event["title"]: event["id"]
                for event in self.events
            }

            # Team mapping

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

            self.load_team(
                team_id
            )

    # =========================================================
    # LOAD SELECTED TEAM
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
                team
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

    def create_team_header(self, team):

        card = ctk.CTkFrame(
            self.content,
            corner_radius=15
        )

        card.pack(
            fill="x",
            pady=(0, 20)
        )

        ctk.CTkLabel(
            card,
            text=team.get(
                "name",
                "Unnamed Team"
            ),
            font=("Arial", 24, "bold")
        ).pack(
            anchor="w",
            padx=25,
            pady=(22, 5)
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
            font=("Arial", 13),
            wraplength=800,
            justify="left"
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 20)
        )

    # =========================================================
    # MEMBERS SECTION
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
            font=("Arial", 20, "bold")
        ).pack(
            side="left"
        )

        ctk.CTkButton(
            header,
            text="+ Add Member",
            width=130,
            height=38,
            command=lambda:
                self.open_add_member(team_id)
        ).pack(
            side="right"
        )

        if not members:

            empty_card = ctk.CTkFrame(
                self.content,
                corner_radius=12
            )

            empty_card.pack(
                fill="x",
                pady=10
            )

            ctk.CTkLabel(
                empty_card,
                text="No members in this team yet.",
                font=("Arial", 15)
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
            corner_radius=12
        )

        card.pack(
            fill="x",
            pady=5
        )

        student_name = member.get(
            "name",
            member.get(
                "student_name",
                "Student"
            )
        )

        student_email = member.get(
            "college_email",
            ""
        )

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
            font=("Arial", 16, "bold")
        ).pack(
            anchor="w"
        )

        if student_email:

            ctk.CTkLabel(
                info,
                text=student_email,
                font=("Arial", 12)
            ).pack(
                anchor="w",
                pady=(3, 0)
            )

        student_id = member.get(
            "student_id"
        )

        ctk.CTkButton(
            card,
            text="Remove",
            width=90,
            height=35,
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

        modal.title("Create Team")
        modal.geometry("450x520")
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
            font=("Arial", 24, "bold")
        ).pack(
            pady=(30, 20)
        )

        # Team name

        ctk.CTkLabel(
            modal,
            text="Team Name"
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
            text="Description"
        ).pack(
            anchor="w",
            padx=65
        )

        description_entry = ctk.CTkEntry(
            modal,
            width=320,
            height=40,
            placeholder_text="Enter team description"
        )

        description_entry.pack(
            pady=(5, 12)
        )

        # Event

        ctk.CTkLabel(
            modal,
            text="Event"
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
                text="No events available."
            ).pack(
                pady=10
            )

        # Creator

        ctk.CTkLabel(
            modal,
            text="Created By"
        ).pack(
            anchor="w",
            padx=65
        )

        student_names = list(
            self.student_map.keys()
        )

        if student_names:

            creator_dropdown = ctk.CTkComboBox(
                modal,
                width=320,
                height=40,
                values=student_names
            )

            creator_dropdown.pack(
                pady=(5, 15)
            )

            creator_dropdown.set(
                student_names[0]
            )

        else:

            creator_dropdown = None

            ctk.CTkLabel(
                modal,
                text="No students available."
            ).pack(
                pady=10
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

                self.show_error(
                    "Please enter a team name."
                )

                return

            if not creator_dropdown:

                self.show_error(
                    "No student is available to create the team."
                )

                return

            created_by = self.student_map.get(
                creator_dropdown.get()
            )

            event_id = None

            if event_dropdown:

                event_id = self.event_map.get(
                    event_dropdown.get()
                )

            try:

                create_team(
                    name,
                    description,
                    event_id,
                    created_by
                )

                modal.destroy()

                self.load_data()

            except Exception as error:

                self.show_error(
                    f"Unable to create team:\n\n{error}"
                )

        ctk.CTkButton(
            modal,
            text="Create Team",
            width=320,
            height=42,
            command=save_team
        ).pack(
            pady=10
        )

    # =========================================================
    # ADD MEMBER
    # =========================================================

    def open_add_member(self, team_id):

        modal = ctk.CTkToplevel(
            self
        )

        modal.title("Add Team Member")
        modal.geometry("450x300")
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
            font=("Arial", 22, "bold")
        ).pack(
            pady=(30, 20)
        )

        student_names = list(
            self.student_map.keys()
        )

        if not student_names:

            ctk.CTkLabel(
                modal,
                text="No students available."
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

                self.show_error(
                    f"Unable to add member:\n\n{error}"
                )

        ctk.CTkButton(
            modal,
            text="Add Member",
            width=320,
            height=42,
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
    # EMPTY STATE
    # =========================================================

    def show_no_team(self):

        card = ctk.CTkFrame(
            self.content,
            corner_radius=15
        )

        card.pack(
            fill="x",
            pady=30
        )

        ctk.CTkLabel(
            card,
            text="No teams created yet.",
            font=("Arial", 20, "bold")
        ).pack(
            pady=(35, 5)
        )

        ctk.CTkLabel(
            card,
            text="Create a team to start collaborating.",
            font=("Arial", 13)
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

        window.title("Team Builder")
        window.geometry("450x250")
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
            font=("Arial", 14)
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