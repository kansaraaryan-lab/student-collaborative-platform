import customtkinter as ctk

from api_client import get_students, create_student, get_rooms


class StudentsPage(ctk.CTkFrame):
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
            text="Students",
            font=("Arial", 30, "bold")
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        ctk.CTkButton(
            header,
            text="+  Add Student",
            width=140,
            height=40,
            corner_radius=10,
            command=self.open_add_student
        ).grid(
            row=0,
            column=1,
            sticky="e"
        )

        ctk.CTkLabel(
            self,
            text="View and manage students registered on the platform.",
            font=("Arial", 14)
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=35,
            pady=(0, 20)
        )

        # Student list
        self.student_list = ctk.CTkScrollableFrame(
            self,
            corner_radius=15
        )

        self.student_list.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=35,
            pady=(0, 30)
        )

        self.load_students()

    def load_students(self):
        for widget in self.student_list.winfo_children():
            widget.destroy()

        try:
            students = get_students()

            if not students:
                ctk.CTkLabel(
                    self.student_list,
                    text="No students found.\n\nClick '+ Add Student' to add one.",
                    font=("Arial", 16),
                    justify="center"
                ).pack(pady=80)

                return

            for student in students:
                self.create_student_card(student)

        except Exception as error:
            ctk.CTkLabel(
                self.student_list,
                text=f"Could not load students.\n{error}",
                font=("Arial", 14),
                wraplength=600
            ).pack(pady=50)

    def create_student_card(self, student):
        card = ctk.CTkFrame(
            self.student_list,
            height=100,
            corner_radius=12
        )

        card.pack(
            fill="x",
            padx=10,
            pady=8
        )

        name = student.get("name", "Unknown Student")
        email = student.get("college_email", "No email")
        student_id = student.get("id", "-")
        room_id = student.get("room_id", "-")

        ctk.CTkLabel(
            card,
            text=name,
            font=("Arial", 18, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 2)
        )

        ctk.CTkLabel(
            card,
            text=(
                f"{email}   •   "
                f"Student ID: {student_id}   •   "
                f"Room ID: {room_id}"
            ),
            font=("Arial", 12)
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 15)
        )

    def open_add_student(self):
        try:
            rooms = get_rooms()

        except Exception as error:
            self.show_error(
                f"Could not load rooms.\n{error}"
            )
            return

        if not rooms:
            self.show_error(
                "No rooms available.\n\n"
                "Create a room first from the Rooms section."
            )
            return

        dialog = ctk.CTkToplevel(self)

        dialog.title("Add Student")
        dialog.geometry("450x500")
        dialog.resizable(False, False)

        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()

        ctk.CTkLabel(
            dialog,
            text="Add Student",
            font=("Arial", 26, "bold")
        ).pack(
            anchor="w",
            padx=30,
            pady=(30, 5)
        )

        ctk.CTkLabel(
            dialog,
            text="Enter the student's details.",
            font=("Arial", 13)
        ).pack(
            anchor="w",
            padx=30,
            pady=(0, 25)
        )

        name_entry = ctk.CTkEntry(
            dialog,
            placeholder_text="Student name",
            height=42
        )
        name_entry.pack(
            fill="x",
            padx=30,
            pady=8
        )

        email_entry = ctk.CTkEntry(
            dialog,
            placeholder_text="College email",
            height=42
        )
        email_entry.pack(
            fill="x",
            padx=30,
            pady=8
        )

        # Create readable room names
        room_options = {}

        for room in rooms:
            room_id = room["id"]

            room_text = (
                f"Year {room['year']} • "
                f"{room['branch']} • "
                f"Division {room['division']}"
            )

            room_options[room_text] = room_id

        room_dropdown = ctk.CTkComboBox(
            dialog,
            values=list(room_options.keys()),
            height=42,
            state="readonly"
        )

        room_dropdown.pack(
            fill="x",
            padx=30,
            pady=8
        )

        room_dropdown.set("Select Room")

        status_label = ctk.CTkLabel(
            dialog,
            text="",
            font=("Arial", 12),
            wraplength=350
        )

        status_label.pack(
            padx=30,
            pady=5
        )

        def submit():
            name = name_entry.get().strip()
            email = email_entry.get().strip()
            selected_room = room_dropdown.get()

            if not name or not email:
                status_label.configure(
                    text="Please fill in all fields."
                )
                return

            if selected_room == "Select Room":
                status_label.configure(
                    text="Please select a room."
                )
                return

            room_id = room_options[selected_room]

            try:
                create_student(
                    college_email=email,
                    name=name,
                    room_id=room_id
                )

                dialog.destroy()
                self.load_students()

            except Exception as error:
                status_label.configure(
                    text=f"Could not create student.\n{error}"
                )

        ctk.CTkButton(
            dialog,
            text="Add Student",
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

    def show_error(self, message):
        dialog = ctk.CTkToplevel(self)

        dialog.title("Error")
        dialog.geometry("400x220")
        dialog.resizable(False, False)

        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()

        ctk.CTkLabel(
            dialog,
            text="Something went wrong",
            font=("Arial", 20, "bold")
        ).pack(pady=(30, 10))

        ctk.CTkLabel(
            dialog,
            text=message,
            font=("Arial", 13),
            wraplength=340
        ).pack(pady=10)

        ctk.CTkButton(
            dialog,
            text="OK",
            width=100,
            command=dialog.destroy
        ).pack(pady=15)

