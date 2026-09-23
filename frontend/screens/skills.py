import customtkinter as ctk

from api_client import (
    get_skills,
    create_skill,
    update_skill,
    delete_skill
)


class SkillsPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Header
        header = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=35,
            pady=(30, 5)
        )

        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header,
            text="Skills",
            font=("Arial", 30, "bold")
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        ctk.CTkButton(
            header,
            text="+  Add Skill",
            width=140,
            height=40,
            corner_radius=10,
            command=self.open_add_skill
        ).grid(
            row=0,
            column=1,
            sticky="e"
        )

        ctk.CTkLabel(
            self,
            text="Manage technical skills available on the platform.",
            font=("Arial", 14)
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=35,
            pady=(0, 20)
        )

        # Skills list
        self.skill_list = ctk.CTkScrollableFrame(
            self,
            corner_radius=15
        )

        self.skill_list.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=35,
            pady=(0, 30)
        )

        self.load_skills()

    def load_skills(self):
        for widget in self.skill_list.winfo_children():
            widget.destroy()

        try:
            skills = get_skills()

            if not skills:
                ctk.CTkLabel(
                    self.skill_list,
                    text="No skills found.\n\nClick '+ Add Skill' to create one.",
                    font=("Arial", 16),
                    justify="center"
                ).pack(pady=80)

                return

            for skill in skills:
                self.create_skill_card(skill)

        except Exception as error:
            ctk.CTkLabel(
                self.skill_list,
                text=f"Could not load skills.\n{error}",
                font=("Arial", 14),
                wraplength=600
            ).pack(pady=50)

    def create_skill_card(self, skill):
        card = ctk.CTkFrame(
            self.skill_list,
            height=80,
            corner_radius=12
        )

        card.pack(
            fill="x",
            padx=10,
            pady=8
        )

        skill_id = skill.get("id", "-")
        name = skill.get("name", "Unknown Skill")

        info = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )
        info.pack(
            side="left",
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        ctk.CTkLabel(
            info,
            text=name,
            font=("Arial", 17, "bold")
        ).pack(anchor="w")

        ctk.CTkLabel(
            info,
            text=f"Skill ID: {skill_id}",
            font=("Arial", 11)
        ).pack(anchor="w")

        actions = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )
        actions.pack(
            side="right",
            padx=20
        )

        ctk.CTkButton(
            actions,
            text="Edit",
            width=75,
            height=35,
            corner_radius=8,
            command=lambda s=skill: self.open_edit_skill(s)
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            actions,
            text="Delete",
            width=75,
            height=35,
            corner_radius=8,
            fg_color="#8B2E2E",
            hover_color="#A83A3A",
            command=lambda sid=skill_id: self.confirm_delete(sid)
        ).pack(
            side="left",
            padx=5
        )

    def open_add_skill(self):
        self.open_skill_dialog()

    def open_edit_skill(self, skill):
        self.open_skill_dialog(skill)

    def open_skill_dialog(self, skill=None):
        editing = skill is not None

        dialog = ctk.CTkToplevel(self)

        dialog.title(
            "Edit Skill" if editing else "Add Skill"
        )

        dialog.geometry("430x300")
        dialog.resizable(False, False)

        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()

        ctk.CTkLabel(
            dialog,
            text="Edit Skill" if editing else "Add Skill",
            font=("Arial", 25, "bold")
        ).pack(
            anchor="w",
            padx=30,
            pady=(30, 5)
        )

        ctk.CTkLabel(
            dialog,
            text="Enter the skill name.",
            font=("Arial", 13)
        ).pack(
            anchor="w",
            padx=30,
            pady=(0, 20)
        )

        skill_entry = ctk.CTkEntry(
            dialog,
            placeholder_text="e.g. Python",
            height=42
        )

        skill_entry.pack(
            fill="x",
            padx=30,
            pady=8
        )

        if editing:
            skill_entry.insert(
                0,
                skill.get("name", "")
            )

        status_label = ctk.CTkLabel(
            dialog,
            text="",
            font=("Arial", 12),
            wraplength=350
        )

        status_label.pack(pady=5)

        def submit():
            name = skill_entry.get().strip()

            if not name:
                status_label.configure(
                    text="Please enter a skill name."
                )
                return

            try:
                if editing:
                    update_skill(
                        skill["id"],
                        name
                    )
                else:
                    create_skill(name)

                dialog.destroy()
                self.load_skills()

            except Exception as error:
                status_label.configure(
                    text=f"Operation failed.\n{error}"
                )

        ctk.CTkButton(
            dialog,
            text="Save Changes" if editing else "Add Skill",
            height=42,
            corner_radius=10,
            command=submit
        ).pack(
            fill="x",
            padx=30,
            pady=15
        )

        ctk.CTkButton(
            dialog,
            text="Cancel",
            height=38,
            corner_radius=10,
            fg_color="transparent",
            border_width=1,
            command=dialog.destroy
        ).pack(
            fill="x",
            padx=30
        )

    def confirm_delete(self, skill_id):
        dialog = ctk.CTkToplevel(self)

        dialog.title("Delete Skill")
        dialog.geometry("400x220")
        dialog.resizable(False, False)

        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()

        ctk.CTkLabel(
            dialog,
            text="Delete this skill?",
            font=("Arial", 22, "bold")
        ).pack(pady=(30, 10))

        ctk.CTkLabel(
            dialog,
            text="This action cannot be undone.",
            font=("Arial", 13)
        ).pack()

        buttons = ctk.CTkFrame(
            dialog,
            fg_color="transparent"
        )
        buttons.pack(pady=25)

        def remove():
            try:
                delete_skill(skill_id)
                dialog.destroy()
                self.load_skills()

            except Exception as error:
                dialog.destroy()

                self.show_error(
                    f"Could not delete skill.\n{error}"
                )

        ctk.CTkButton(
            buttons,
            text="Delete",
            width=100,
            fg_color="#8B2E2E",
            hover_color="#A83A3A",
            command=remove
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            buttons,
            text="Cancel",
            width=100,
            command=dialog.destroy
        ).pack(
            side="left",
            padx=5
        )

    def show_error(self, message):
        dialog = ctk.CTkToplevel(self)

        dialog.title("Error")
        dialog.geometry("400x200")
        dialog.resizable(False, False)

        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()

        ctk.CTkLabel(
            dialog,
            text=message,
            font=("Arial", 13),
            wraplength=340
        ).pack(pady=(45, 20))

        ctk.CTkButton(
            dialog,
            text="OK",
            width=100,
            command=dialog.destroy
        ).pack()

