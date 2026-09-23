import customtkinter as ctk

from api_client import (
    get_students,
    get_skills,
    get_student_skills,
    add_student_skill,
    delete_student_skill,
)


class StudentSkillsPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color="transparent"
        )

        self.students = []
        self.skills = []
        self.student_map = {}
        self.skill_map = {}

        self.create_ui()
        self.load_data()

    # ================= UI =================

    def create_ui(self):

        title = ctk.CTkLabel(
            self,
            text="Student Skills",
            font=("Arial", 30, "bold")
        )

        title.pack(
            anchor="w",
            padx=35,
            pady=(30, 5)
        )

        subtitle = ctk.CTkLabel(
            self,
            text="Manage technical skills and proficiency levels.",
            font=("Arial", 14)
        )

        subtitle.pack(
            anchor="w",
            padx=35
        )

        controls = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        controls.pack(
            fill="x",
            padx=35,
            pady=25
        )

        self.student_dropdown = ctk.CTkComboBox(
            controls,
            width=300,
            values=["Loading students..."],
            command=self.student_selected
        )

        self.student_dropdown.pack(
            side="left",
            padx=(0, 10)
        )

        add_button = ctk.CTkButton(
            controls,
            text="+ Add Skill",
            width=130,
            height=40,
            command=self.open_add_skill
        )

        add_button.pack(
            side="left"
        )

        self.skills_container = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )

        self.skills_container.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=(0, 25)
        )

    # ================= DATA =================

    def load_data(self):

        try:
            self.students = get_students()
            self.skills = get_skills()

            self.student_map = {
                f"{student['name']} • {student['college_email']}":
                    student["id"]
                for student in self.students
            }

            self.skill_map = {
                skill["name"]: skill["id"]
                for skill in self.skills
            }

            student_names = list(self.student_map.keys())

            if student_names:
                self.student_dropdown.configure(
                    values=student_names
                )

                self.student_dropdown.set(
                    student_names[0]
                )

                self.load_student_skills(
                    self.student_map[student_names[0]]
                )

            else:
                self.student_dropdown.configure(
                    values=["No students found"]
                )

        except Exception as error:

            self.show_error(
                f"Failed to load data:\n{error}"
            )

    def student_selected(self, selected_student):

        student_id = self.student_map.get(
            selected_student
        )

        if student_id:
            self.load_student_skills(student_id)

    def load_student_skills(self, student_id):

        for widget in self.skills_container.winfo_children():
            widget.destroy()

        try:

            student_skills = get_student_skills(
                student_id
            )

            if not student_skills:

                ctk.CTkLabel(
                    self.skills_container,
                    text="No skills added for this student.",
                    font=("Arial", 16)
                ).pack(
                    pady=50
                )

                return

            for item in student_skills:

                self.create_skill_card(
                    item,
                    student_id
                )

        except Exception as error:

            self.show_error(
                f"Failed to load student skills:\n{error}"
            )

    # ================= SKILL CARD =================

    def create_skill_card(self, item, student_id):

        card = ctk.CTkFrame(
            self.skills_container,
            corner_radius=12
        )

        card.pack(
            fill="x",
            pady=7
        )

        skill_name = item.get(
            "skill_name",
            item.get("name", "Unknown Skill")
        )

        proficiency = item.get(
            "proficiency",
            "Not specified"
        )

        ctk.CTkLabel(
            card,
            text=skill_name,
            font=("Arial", 18, "bold")
        ).pack(
            side="left",
            padx=20,
            pady=18
        )

        ctk.CTkLabel(
            card,
            text=f"Proficiency: {proficiency}",
            font=("Arial", 14)
        ).pack(
            side="left",
            padx=20
        )

        delete_button = ctk.CTkButton(
            card,
            text="Remove",
            width=90,
            fg_color="#B91C1C",
            hover_color="#991B1B",
            command=lambda:
                self.remove_skill(
                    student_id,
                    item.get("skill_id")
                )
        )

        delete_button.pack(
            side="right",
            padx=20
        )

    # ================= ADD SKILL =================

    def open_add_skill(self):

        selected_student = self.student_dropdown.get()

        student_id = self.student_map.get(
            selected_student
        )

        if not student_id:
            self.show_error(
                "Please select a student first."
            )
            return

        if not self.skills:
            self.show_error(
                "No skills available. Create a skill first."
            )
            return

        modal = ctk.CTkToplevel(self)

        modal.title("Add Student Skill")
        modal.geometry("420x350")
        modal.resizable(False, False)

        modal.transient(self.winfo_toplevel())
        modal.grab_set()

        ctk.CTkLabel(
            modal,
            text="Add Skill",
            font=("Arial", 24, "bold")
        ).pack(
            pady=(30, 20)
        )

        skill_dropdown = ctk.CTkComboBox(
            modal,
            values=list(self.skill_map.keys()),
            width=300
        )

        skill_dropdown.pack(
            pady=10
        )

        skill_dropdown.set(
            list(self.skill_map.keys())[0]
        )

        ctk.CTkLabel(
            modal,
            text="Proficiency"
        ).pack(
            pady=(15, 5)
        )

        proficiency_dropdown = ctk.CTkComboBox(
            modal,
            values=[
                "Beginner",
                "Intermediate",
                "Advanced",
                "Expert"
            ],
            width=300
        )

        proficiency_dropdown.pack(
            pady=5
        )

        proficiency_dropdown.set(
            "Beginner"
        )

        def save():

            skill_name = skill_dropdown.get()
            proficiency = proficiency_dropdown.get()

            skill_id = self.skill_map.get(
                skill_name
            )

            try:

                add_student_skill(
                    student_id,
                    skill_id,
                    proficiency
                )

                modal.destroy()

                self.load_student_skills(
                    student_id
                )

            except Exception as error:

                self.show_error(
                    f"Failed to add skill:\n{error}"
                )

        ctk.CTkButton(
            modal,
            text="Add Skill",
            width=300,
            height=40,
            command=save
        ).pack(
            pady=25
        )

    # ================= DELETE =================

    def remove_skill(self, student_id, skill_id):

        try:

            delete_student_skill(
                student_id,
                skill_id
            )

            self.load_student_skills(
                student_id
            )

        except Exception as error:

            self.show_error(
                f"Failed to remove skill:\n{error}"
            )

    # ================= ERROR =================

    def show_error(self, message):

        error_window = ctk.CTkToplevel(self)

        error_window.title("Error")
        error_window.geometry("400x220")
        error_window.resizable(False, False)

        error_window.transient(
            self.winfo_toplevel()
        )

        ctk.CTkLabel(
            error_window,
            text="Something went wrong",
            font=("Arial", 20, "bold")
        ).pack(
            pady=(30, 15)
        )

        ctk.CTkLabel(
            error_window,
            text=message,
            wraplength=340
        ).pack(
            padx=20
        )

        ctk.CTkButton(
            error_window,
            text="OK",
            width=100,
            command=error_window.destroy
        ).pack(
            pady=20
        )