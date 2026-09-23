import customtkinter as ctk

from api_client import (
    get_students,
    get_student_profile,
    create_student_profile,
    update_student_profile,
)


class ProfilePage(ctk.CTkFrame):

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

    SUCCESS = "#22C55E"
    ERROR = "#EF4444"

    # =========================================================
    # INITIALIZATION
    # =========================================================

    def __init__(self, parent):

        super().__init__(
            parent,
            fg_color=self.BG
        )

        self.students = []
        self.student_map = {}
        self.current_student_id = None
        self.profile_exists = False

        self.build_ui()
        self.load_students()

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

        header.pack(
            fill="x",
            padx=36,
            pady=(32, 0)
        )

        ctk.CTkLabel(
            header,
            text="Profile",
            font=("Segoe UI", 30, "bold"),
            text_color=self.TEXT_PRIMARY
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            header,
            text="Manage student information and professional links.",
            font=("Segoe UI", 14),
            text_color=self.TEXT_SECONDARY
        ).pack(
            anchor="w",
            pady=(5, 0)
        )

        # -----------------------------------------------------
        # CONTENT
        # -----------------------------------------------------

        content = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color=self.BORDER,
            scrollbar_button_hover_color="#343A46"
        )

        content.pack(
            fill="both",
            expand=True,
            padx=36,
            pady=(26, 28)
        )

        # -----------------------------------------------------
        # STUDENT SELECTOR
        # -----------------------------------------------------

        selector_card = ctk.CTkFrame(
            content,
            fg_color=self.CARD,
            border_width=1,
            border_color=self.BORDER,
            corner_radius=14
        )

        selector_card.pack(
            fill="x",
            pady=(0, 18)
        )

        selector_inner = ctk.CTkFrame(
            selector_card,
            fg_color="transparent"
        )

        selector_inner.pack(
            fill="x",
            padx=22,
            pady=20
        )

        # Selector title row

        title_row = ctk.CTkFrame(
            selector_inner,
            fg_color="transparent"
        )

        title_row.pack(
            fill="x"
        )

        ctk.CTkLabel(
            title_row,
            text="Student",
            font=("Segoe UI", 15, "bold"),
            text_color=self.TEXT_PRIMARY
        ).pack(
            side="left"
        )

        ctk.CTkLabel(
            title_row,
            text="Choose a student to manage their profile",
            font=("Segoe UI", 12),
            text_color=self.TEXT_MUTED
        ).pack(
            side="left",
            padx=(12, 0)
        )

        self.student_dropdown = ctk.CTkComboBox(
            selector_inner,
            width=430,
            height=42,
            corner_radius=9,
            state="readonly",
            command=self.student_selected,

            fg_color=self.INPUT,
            border_color=self.BORDER,
            border_width=1,

            button_color=self.ACCENT,
            button_hover_color=self.ACCENT_HOVER,

            dropdown_fg_color=self.CARD,
            dropdown_hover_color=self.CARD_HOVER,

            text_color=self.TEXT_PRIMARY,
            font=("Segoe UI", 13)
        )

        self.student_dropdown.pack(
            anchor="w",
            pady=(12, 0)
        )

        # -----------------------------------------------------
        # PROFILE CARD
        # -----------------------------------------------------

        profile_card = ctk.CTkFrame(
            content,
            fg_color=self.CARD,
            border_width=1,
            border_color=self.BORDER,
            corner_radius=14
        )

        profile_card.pack(
            fill="x"
        )

        profile_inner = ctk.CTkFrame(
            profile_card,
            fg_color="transparent"
        )

        profile_inner.pack(
            fill="x",
            padx=26,
            pady=26
        )

        # -----------------------------------------------------
        # PROFILE HEADER
        # -----------------------------------------------------

        profile_header = ctk.CTkFrame(
            profile_inner,
            fg_color="transparent"
        )

        profile_header.pack(
            fill="x",
            pady=(0, 22)
        )

        ctk.CTkLabel(
            profile_header,
            text="Student Profile",
            font=("Segoe UI", 20, "bold"),
            text_color=self.TEXT_PRIMARY
        ).pack(
            anchor="w"
        )

        self.status_label = ctk.CTkLabel(
            profile_header,
            text="Select a student to load their profile.",
            font=("Segoe UI", 12),
            text_color=self.TEXT_MUTED
        )

        self.status_label.pack(
            anchor="w",
            pady=(5, 0)
        )

        # -----------------------------------------------------
        # ABOUT SECTION
        # -----------------------------------------------------

        self.create_section_title(
            profile_inner,
            "About"
        )

        self.create_field_label(
            profile_inner,
            "Bio"
        )

        self.bio_text = ctk.CTkTextbox(
            profile_inner,
            height=120,
            corner_radius=10,
            fg_color=self.INPUT,
            border_width=1,
            border_color=self.BORDER,
            text_color=self.TEXT_PRIMARY,
            font=("Segoe UI", 13)
        )

        self.bio_text.pack(
            fill="x",
            pady=(6, 18)
        )

        # -----------------------------------------------------
        # PROFILE PICTURE
        # -----------------------------------------------------

        self.create_field_label(
            profile_inner,
            "Profile Picture URL"
        )

        self.profile_picture_entry = self.create_entry(
            profile_inner,
            "https://example.com/profile.jpg"
        )

        # -----------------------------------------------------
        # PROFESSIONAL LINKS
        # -----------------------------------------------------

        self.create_section_title(
            profile_inner,
            "Professional Links",
            pady=(8, 16)
        )

        # GitHub

        self.create_field_label(
            profile_inner,
            "GitHub"
        )

        self.github_entry = self.create_entry(
            profile_inner,
            "https://github.com/username"
        )

        # LinkedIn

        self.create_field_label(
            profile_inner,
            "LinkedIn"
        )

        self.linkedin_entry = self.create_entry(
            profile_inner,
            "https://linkedin.com/in/username"
        )

        # -----------------------------------------------------
        # DIVIDER
        # -----------------------------------------------------

        ctk.CTkFrame(
            profile_inner,
            height=1,
            fg_color=self.BORDER
        ).pack(
            fill="x",
            pady=(4, 20)
        )

        # -----------------------------------------------------
        # SAVE AREA
        # -----------------------------------------------------

        save_row = ctk.CTkFrame(
            profile_inner,
            fg_color="transparent"
        )

        save_row.pack(
            fill="x"
        )

        self.save_button = ctk.CTkButton(
            save_row,
            text="Save Profile",
            width=150,
            height=42,
            corner_radius=9,
            fg_color=self.ACCENT,
            hover_color=self.ACCENT_HOVER,
            font=("Segoe UI", 13, "bold"),
            text_color="white",
            command=self.save_profile
        )

        self.save_button.pack(
            side="left"
        )

    # =========================================================
    # SECTION TITLE
    # =========================================================

    def create_section_title(
        self,
        parent,
        text,
        pady=(4, 16)
    ):

        ctk.CTkLabel(
            parent,
            text=text,
            font=("Segoe UI", 14, "bold"),
            text_color=self.TEXT_PRIMARY
        ).pack(
            anchor="w",
            pady=pady
        )

    # =========================================================
    # FIELD LABEL
    # =========================================================

    def create_field_label(
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
            anchor="w"
        )

    # =========================================================
    # ENTRY
    # =========================================================

    def create_entry(
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
            pady=(6, 18)
        )

        return entry

    # =========================================================
    # STUDENTS
    # =========================================================

    def load_students(self):

        try:

            self.students = get_students()

            if not self.students:

                self.student_dropdown.configure(
                    values=["No students available"]
                )

                self.student_dropdown.set(
                    "No students available"
                )

                self.status_label.configure(
                    text="Create a student first to manage their profile.",
                    text_color=self.TEXT_MUTED
                )

                self.set_form_state(False)

                return

            self.student_map = {}

            dropdown_values = []

            for student in self.students:

                student_id = student.get("id")

                name = student.get(
                    "name",
                    f"Student {student_id}"
                )

                label = f"{name}  •  ID {student_id}"

                dropdown_values.append(label)

                self.student_map[label] = student_id

            self.student_dropdown.configure(
                values=dropdown_values
            )

            self.student_dropdown.set(
                dropdown_values[0]
            )

            self.student_selected(
                dropdown_values[0]
            )

        except Exception as error:

            self.status_label.configure(
                text=f"Unable to load students: {error}",
                text_color=self.ERROR
            )

            self.set_form_state(False)

    # =========================================================
    # STUDENT SELECTED
    # =========================================================

    def student_selected(
        self,
        selection
    ):

        student_id = self.student_map.get(
            selection
        )

        if not student_id:
            return

        self.current_student_id = student_id

        self.load_profile(
            student_id
        )

    # =========================================================
    # LOAD PROFILE
    # =========================================================

    def load_profile(
        self,
        student_id
    ):

        self.clear_form()

        self.status_label.configure(
            text="Loading profile...",
            text_color=self.TEXT_MUTED
        )

        try:

            profile = get_student_profile(
                student_id
            )

            self.profile_exists = True

            self.bio_text.insert(
                "1.0",
                profile.get("bio") or ""
            )

            self.profile_picture_entry.insert(
                0,
                profile.get("profile_picture") or ""
            )

            self.github_entry.insert(
                0,
                profile.get("github_url") or ""
            )

            self.linkedin_entry.insert(
                0,
                profile.get("linkedin_url") or ""
            )

            self.status_label.configure(
                text="Profile loaded. You can edit the information below.",
                text_color=self.SUCCESS
            )

            self.save_button.configure(
                text="Update Profile"
            )

            self.set_form_state(True)

        except Exception as error:

            # 404 means the student exists but
            # does not have a profile yet.

            if "404" in str(error):

                self.profile_exists = False

                self.status_label.configure(
                    text="No profile exists yet. Create one below.",
                    text_color=self.TEXT_MUTED
                )

                self.save_button.configure(
                    text="Create Profile"
                )

                self.set_form_state(True)

            else:

                self.status_label.configure(
                    text=f"Unable to load profile: {error}",
                    text_color=self.ERROR
                )

                self.set_form_state(False)

    # =========================================================
    # SAVE PROFILE
    # =========================================================

    def save_profile(self):

        if not self.current_student_id:
            return

        bio = self.bio_text.get(
            "1.0",
            "end"
        ).strip()

        profile_picture = (
            self.profile_picture_entry
            .get()
            .strip()
        )

        github_url = (
            self.github_entry
            .get()
            .strip()
        )

        linkedin_url = (
            self.linkedin_entry
            .get()
            .strip()
        )

        self.save_button.configure(
            state="disabled",
            text="Saving..."
        )

        try:

            if self.profile_exists:

                update_student_profile(
                    self.current_student_id,
                    bio,
                    profile_picture,
                    github_url,
                    linkedin_url
                )

                self.status_label.configure(
                    text="Profile updated successfully.",
                    text_color=self.SUCCESS
                )

            else:

                create_student_profile(
                    self.current_student_id,
                    bio,
                    profile_picture,
                    github_url,
                    linkedin_url
                )

                self.profile_exists = True

                self.status_label.configure(
                    text="Profile created successfully.",
                    text_color=self.SUCCESS
                )

            self.save_button.configure(
                text="Update Profile"
            )

        except Exception as error:

            self.status_label.configure(
                text=f"Unable to save profile: {error}",
                text_color=self.ERROR
            )

        finally:

            self.save_button.configure(
                state="normal"
            )

    # =========================================================
    # CLEAR FORM
    # =========================================================

    def clear_form(self):

        self.bio_text.delete(
            "1.0",
            "end"
        )

        self.profile_picture_entry.delete(
            0,
            "end"
        )

        self.github_entry.delete(
            0,
            "end"
        )

        self.linkedin_entry.delete(
            0,
            "end"
        )

    # =========================================================
    # FORM STATE
    # =========================================================

    def set_form_state(
        self,
        enabled
    ):

        state = (
            "normal"
            if enabled
            else "disabled"
        )

        self.bio_text.configure(
            state=state
        )

        self.profile_picture_entry.configure(
            state=state
        )

        self.github_entry.configure(
            state=state
        )

        self.linkedin_entry.configure(
            state=state
        )

        self.save_button.configure(
            state=state
        )