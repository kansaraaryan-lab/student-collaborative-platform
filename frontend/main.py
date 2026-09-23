import customtkinter as ctk

from api_client import (
    get_students,
    get_rooms,
    get_skills,
)

from screens.students import StudentsPage
from screens.rooms import RoomsPage
from screens.skills import SkillsPage
from screens.student_skills import StudentSkillsPage
from screens.profile import ProfilePage
from screens.events import EventsPage
from screens.team_builder import TeamBuilderPage


class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("StudentHub")
        self.geometry("1200x750")
        self.minsize(1000, 650)

        ctk.set_appearance_mode("dark")

        self.configure(
            fg_color="#0F1117"
        )

        self.current_page = None
        self.nav_buttons = {}

        self.build_layout()

        # Start on Dashboard
        self.navigation_clicked("⌂   Dashboard")

    # =========================================================
    # LAYOUT
    # =========================================================

    def build_layout(self):

        self.sidebar = ctk.CTkFrame(
            self,
            width=235,
            corner_radius=0,
            fg_color="#13161D"
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        self.sidebar.pack_propagate(False)

        self.main_area = ctk.CTkFrame(
            self,
            fg_color="#0F1117",
            corner_radius=0
        )

        self.main_area.pack(
            side="right",
            fill="both",
            expand=True
        )

        self.create_sidebar()

    # =========================================================
    # SIDEBAR
    # =========================================================

    def create_sidebar(self):

        logo_frame = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )

        logo_frame.pack(
            fill="x",
            padx=20,
            pady=(25, 30)
        )

        ctk.CTkLabel(
            logo_frame,
            text="StudentHub",
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            ),
            text_color="#F4F4F5"
        ).pack(anchor="w")

        ctk.CTkLabel(
            logo_frame,
            text="Student Collaboration Platform",
            font=ctk.CTkFont(size=10),
            text_color="#6B7280"
        ).pack(
            anchor="w",
            pady=(3, 0)
        )

        nav_frame = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )

        nav_frame.pack(
            fill="x",
            padx=12
        )

        self.create_nav_button(
            nav_frame,
            "⌂   Dashboard"
        )

        self.create_nav_button(
            nav_frame,
            "👥   Students"
        )

        self.create_nav_button(
            nav_frame,
            "▣   Rooms"
        )

        self.create_nav_button(
            nav_frame,
            "◉   Profile"
        )

        self.create_nav_button(
            nav_frame,
            "◆   Skills"
        )

        self.create_nav_button(
            nav_frame,
            "★   Student Skills"
        )

        self.create_nav_button(
            nav_frame,
            "◈   Events"
        )

        self.create_nav_button(
            nav_frame,
            "⚡   Team Builder"
        )

        # Bottom navigation

        bottom_frame = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )

        bottom_frame.pack(
            side="bottom",
            fill="x",
            padx=12,
            pady=20
        )

        ctk.CTkFrame(
            bottom_frame,
            height=1,
            fg_color="#282D38"
        ).pack(
            fill="x",
            pady=(0, 12)
        )

        self.create_bottom_button(
            bottom_frame,
            "⚙   Settings",
            self.show_settings
        )

        self.create_bottom_button(
            bottom_frame,
            "⇥   Logout",
            self.logout
        )

    # =========================================================
    # SIDEBAR BUTTON
    # =========================================================

    def create_nav_button(self, parent, text):

        button = ctk.CTkButton(
            parent,
            text=text,
            height=42,
            anchor="w",
            fg_color="transparent",
            hover_color="#1D212B",
            text_color="#A1A1AA",
            font=ctk.CTkFont(size=13),
            corner_radius=8,
            command=lambda p=text: self.navigation_clicked(p)
        )

        button.pack(
            fill="x",
            pady=3
        )

        self.nav_buttons[text] = button

    def create_bottom_button(
        self,
        parent,
        text,
        command
    ):

        button = ctk.CTkButton(
            parent,
            text=text,
            height=40,
            anchor="w",
            fg_color="transparent",
            hover_color="#1D212B",
            text_color="#9CA3AF",
            font=ctk.CTkFont(size=13),
            corner_radius=8,
            command=command
        )

        button.pack(
            fill="x",
            pady=2
        )

    # =========================================================
    # NAVIGATION
    # =========================================================

    def navigation_clicked(self, page):

        # Update active sidebar button
        self.set_active_nav(page)

        # Remove current page
        self.clear_page()

        # IMPORTANT:
        # Each condition creates a completely different page.

        if page == "⌂   Dashboard":

            self.show_dashboard()

        elif page == "👥   Students":

            self.show_students()

        elif page == "▣   Rooms":

            self.show_rooms()

        elif page == "◉   Profile":

            self.show_profile()

        elif page == "◆   Skills":

            self.show_skills()

        elif page == "★   Student Skills":

            self.show_student_skills()

        elif page == "◈   Events":

            self.show_events()

        elif page == "⚡   Team Builder":

            self.show_team_builder()

    # =========================================================
    # ACTIVE NAV
    # =========================================================

    def set_active_nav(self, active_page):

        for name, button in self.nav_buttons.items():

            if name == active_page:

                button.configure(
                    fg_color="#252A38",
                    text_color="#FFFFFF"
                )

            else:

                button.configure(
                    fg_color="transparent",
                    text_color="#A1A1AA"
                )

    # =========================================================
    # CLEAR PAGE
    # =========================================================

    def clear_page(self):

        if self.current_page:

            self.current_page.destroy()

            self.current_page = None

    # =========================================================
    # DASHBOARD
    # =========================================================

    def show_dashboard(self):

        dashboard = ctk.CTkFrame(
            self.main_area,
            fg_color="transparent"
        )

        dashboard.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=25
        )

        self.current_page = dashboard

        # Header

        ctk.CTkLabel(
            dashboard,
            text="Welcome back 👋",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            ),
            text_color="#F4F4F5"
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            dashboard,
            text="Here's an overview of your StudentHub platform.",
            font=ctk.CTkFont(size=13),
            text_color="#9CA3AF"
        ).pack(
            anchor="w",
            pady=(5, 25)
        )

        # Fetch data

        try:

            students = get_students()
            rooms = get_rooms()
            skills = get_skills()

            student_count = len(students)
            room_count = len(rooms)
            skill_count = len(skills)

        except Exception:

            student_count = 0
            room_count = 0
            skill_count = 0

        # Stats

        stats = ctk.CTkFrame(
            dashboard,
            fg_color="transparent"
        )

        stats.pack(
            fill="x"
        )

        for i in range(3):

            stats.grid_columnconfigure(
                i,
                weight=1
            )

        self.create_stat_card(
            stats,
            0,
            "Students",
            student_count,
            "👥"
        )

        self.create_stat_card(
            stats,
            1,
            "Rooms",
            room_count,
            "▣"
        )

        self.create_stat_card(
            stats,
            2,
            "Skills",
            skill_count,
            "◆"
        )

        # Overview

        overview = ctk.CTkFrame(
            dashboard,
            fg_color="#171A21",
            corner_radius=14,
            border_width=1,
            border_color="#282D38"
        )

        overview.pack(
            fill="both",
            expand=True,
            pady=(25, 0)
        )

        ctk.CTkLabel(
            overview,
            text="Platform Overview",
            font=ctk.CTkFont(
                size=19,
                weight="bold"
            ),
            text_color="#F4F4F5"
        ).pack(
            anchor="w",
            padx=25,
            pady=(25, 5)
        )

        ctk.CTkLabel(
            overview,
            text=(
                f"👥  {student_count} students registered\n\n"
                f"▣  {room_count} rooms available\n\n"
                f"◆  {skill_count} skills available"
            ),
            justify="left",
            anchor="w",
            font=ctk.CTkFont(size=14),
            text_color="#D1D5DB"
        ).pack(
            anchor="w",
            padx=25,
            pady=20
        )

    # =========================================================
    # STAT CARD
    # =========================================================

    def create_stat_card(
        self,
        parent,
        column,
        title,
        value,
        icon
    ):

        card = ctk.CTkFrame(
            parent,
            fg_color="#171A21",
            corner_radius=14,
            border_width=1,
            border_color="#282D38"
        )

        card.grid(
            row=0,
            column=column,
            sticky="nsew",
            padx=6
        )

        ctk.CTkLabel(
            card,
            text=icon,
            font=ctk.CTkFont(size=22),
            text_color="#6366F1"
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )

        ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),
            text_color="#9CA3AF"
        ).pack(
            anchor="w",
            padx=20
        )

        ctk.CTkLabel(
            card,
            text=str(value),
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            ),
            text_color="#F4F4F5"
        ).pack(
            anchor="w",
            padx=20,
            pady=(2, 20)
        )

    # =========================================================
    # STUDENTS PAGE
    # =========================================================

    def show_students(self):

        self.current_page = StudentsPage(
            self.main_area
        )

        self.current_page.pack(
            fill="both",
            expand=True
        )

    # =========================================================
    # ROOMS PAGE
    # =========================================================

    def show_rooms(self):

        self.current_page = RoomsPage(
            self.main_area
        )

        self.current_page.pack(
            fill="both",
            expand=True
        )

    # =========================================================
    # PROFILE PAGE
    # =========================================================

    def show_profile(self):

        self.current_page = ProfilePage(
            self.main_area
        )

        self.current_page.pack(
            fill="both",
            expand=True
        )

    # =========================================================
    # SKILLS PAGE
    # =========================================================

    def show_skills(self):

        self.current_page = SkillsPage(
            self.main_area
        )

        self.current_page.pack(
            fill="both",
            expand=True
        )

    # =========================================================
    # STUDENT SKILLS PAGE
    # =========================================================

    def show_student_skills(self):

        self.current_page = StudentSkillsPage(
            self.main_area
        )

        self.current_page.pack(
            fill="both",
            expand=True
        )

    # =========================================================
    # EVENTS PAGE
    # =========================================================

    def show_events(self):

        self.current_page = EventsPage(
            self.main_area
        )

        self.current_page.pack(
            fill="both",
            expand=True
        )

    # =========================================================
    # TEAM BUILDER PAGE
    # =========================================================

    def show_team_builder(self):

        self.current_page = TeamBuilderPage(
            self.main_area
        )

        self.current_page.pack(
            fill="both",
            expand=True
        )

    # =========================================================
    # SETTINGS
    # =========================================================

    def show_settings(self):

        self.clear_page()

        page = ctk.CTkFrame(
            self.main_area,
            fg_color="transparent"
        )

        page.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=30
        )

        self.current_page = page

        ctk.CTkLabel(
            page,
            text="Settings",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            ),
            text_color="#F4F4F5"
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            page,
            text="Application settings will be available here.",
            font=ctk.CTkFont(size=13),
            text_color="#9CA3AF"
        ).pack(
            anchor="w",
            pady=(6, 0)
        )

    # =========================================================
    # LOGOUT
    # =========================================================

    def logout(self):

        self.navigation_clicked(
            "⌂   Dashboard"
        )


# =============================================================
# START APPLICATION
# =============================================================

if __name__ == "__main__":

    app = App()

    app.mainloop()