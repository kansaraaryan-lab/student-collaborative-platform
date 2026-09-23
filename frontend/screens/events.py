import customtkinter as ctk
from tkinter import messagebox

from api_client import (
    get_events,
    create_event,
    update_event,
    delete_event,
)


class EventsPage(ctk.CTkFrame):

    BG = "#0B0D10"
    CARD = "#111418"
    CARD_HOVER = "#161A20"
    BORDER = "#242932"

    TEXT_PRIMARY = "#F5F7FA"
    TEXT_SECONDARY = "#9AA3B2"
    TEXT_MUTED = "#687180"

    ACCENT = "#7C3AED"
    ACCENT_HOVER = "#6D28D9"

    SUCCESS = "#22C55E"
    WARNING = "#F59E0B"
    INFO = "#3B82F6"

    DANGER = "#EF4444"

    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color=self.BG
        )

        self.current_status = None
        self.filter_buttons = {}

        self.create_ui()
        self.load_events()

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
            padx=36,
            pady=(32, 0)
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
            text="Events",
            font=("Segoe UI", 30, "bold"),
            text_color=self.TEXT_PRIMARY
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            title_section,
            text="Discover what's happening across your college.",
            font=("Segoe UI", 14),
            text_color=self.TEXT_SECONDARY
        ).pack(
            anchor="w",
            pady=(5, 0)
        )

        ctk.CTkButton(
            title_row,
            text="+ Create Event",
            width=145,
            height=40,
            corner_radius=9,
            fg_color=self.ACCENT,
            hover_color=self.ACCENT_HOVER,
            font=("Segoe UI", 13, "bold"),
            command=self.open_create_event
        ).pack(
            side="right",
            pady=(5, 0)
        )

        filter_wrapper = ctk.CTkFrame(
            self,
            fg_color=self.CARD,
            border_width=1,
            border_color=self.BORDER,
            corner_radius=12
        )

        filter_wrapper.pack(
            fill="x",
            padx=36,
            pady=(26, 20)
        )

        filter_frame = ctk.CTkFrame(
            filter_wrapper,
            fg_color="transparent"
        )

        filter_frame.pack(
            padx=8,
            pady=8
        )

        self.create_filter_button(
            filter_frame,
            "All",
            None
        )

        self.create_filter_button(
            filter_frame,
            "Ongoing",
            "ongoing"
        )

        self.create_filter_button(
            filter_frame,
            "Upcoming",
            "upcoming"
        )

        self.create_filter_button(
            filter_frame,
            "Previous",
            "previous"
        )

        self.update_filter_buttons()

        self.events_container = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color=self.BORDER,
            scrollbar_button_hover_color="#343A46"
        )

        self.events_container.pack(
            fill="both",
            expand=True,
            padx=36,
            pady=(0, 28)
        )

    # =========================================================
    # FILTER
    # =========================================================

    def create_filter_button(
        self,
        parent,
        text,
        status
    ):

        button = ctk.CTkButton(
            parent,
            text=text,
            width=110,
            height=36,
            corner_radius=8,
            font=("Segoe UI", 13, "bold"),
            fg_color="transparent",
            hover_color=self.CARD_HOVER,
            text_color=self.TEXT_SECONDARY,
            command=lambda s=status: self.change_status(s)
        )

        button.pack(
            side="left",
            padx=3
        )

        self.filter_buttons[status] = button

    def change_status(self, status):

        self.current_status = status

        self.update_filter_buttons()
        self.load_events()

    def update_filter_buttons(self):

        for status, button in self.filter_buttons.items():

            if status == self.current_status:

                button.configure(
                    fg_color=self.ACCENT,
                    hover_color=self.ACCENT_HOVER,
                    text_color="white"
                )

            else:

                button.configure(
                    fg_color="transparent",
                    hover_color=self.CARD_HOVER,
                    text_color=self.TEXT_SECONDARY
                )

    # =========================================================
    # LOAD EVENTS
    # =========================================================

    def load_events(self):

        for widget in self.events_container.winfo_children():
            widget.destroy()

        try:

            events = get_events(
                self.current_status
            )

            if not events:
                self.show_empty()
                return

            for event in events:
                self.create_event_card(event)

        except Exception as error:

            self.show_error(
                f"{error}"
            )

    # =========================================================
    # EVENT CARD
    # =========================================================

    def create_event_card(self, event):

        card = ctk.CTkFrame(
            self.events_container,
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
            padx=24,
            pady=20
        )

        top_row = ctk.CTkFrame(
            content,
            fg_color="transparent"
        )

        top_row.pack(
            fill="x"
        )

        title_frame = ctk.CTkFrame(
            top_row,
            fg_color="transparent"
        )

        title_frame.pack(
            side="left",
            fill="x",
            expand=True
        )

        title = event.get(
            "title",
            "Untitled Event"
        )

        ctk.CTkLabel(
            title_frame,
            text=title,
            font=("Segoe UI", 19, "bold"),
            text_color=self.TEXT_PRIMARY
        ).pack(
            anchor="w"
        )

        event_type = event.get(
            "event_type",
            "Event"
        )

        self.create_badge(
            top_row,
            event_type,
            self.INFO
        )

        description = event.get(
            "description",
            ""
        )

        if description:

            ctk.CTkLabel(
                content,
                text=description,
                font=("Segoe UI", 13),
                text_color=self.TEXT_SECONDARY,
                wraplength=900,
                justify="left"
            ).pack(
                anchor="w",
                pady=(12, 16)
            )

        info_frame = ctk.CTkFrame(
            content,
            fg_color="transparent"
        )

        info_frame.pack(
            fill="x",
            pady=(4, 0)
        )

        self.create_info_item(
            info_frame,
            "LOCATION",
            event.get("location") or "Not specified"
        )

        self.create_info_item(
            info_frame,
            "START",
            event.get("start_time", "Not specified")
        )

        self.create_info_item(
            info_frame,
            "END",
            event.get("end_time", "Not specified")
        )

        # -----------------------------------------------------
        # Action buttons
        # -----------------------------------------------------

        actions = ctk.CTkFrame(
            content,
            fg_color="transparent"
        )

        actions.pack(
            fill="x",
            pady=(18, 0)
        )

        ctk.CTkButton(
            actions,
            text="Edit",
            width=85,
            height=32,
            corner_radius=7,
            fg_color=self.INFO,
            hover_color="#2563EB",
            command=lambda e=event: self.open_edit_event(e)
        ).pack(
            side="left",
            padx=(0, 8)
        )

        ctk.CTkButton(
            actions,
            text="Delete",
            width=85,
            height=32,
            corner_radius=7,
            fg_color=self.DANGER,
            hover_color="#DC2626",
            command=lambda e=event: self.confirm_delete(e)
        ).pack(
            side="left"
        )

    # =========================================================
    # CREATE / EDIT EVENT
    # =========================================================

    def open_create_event(self):

        self.open_event_modal()

    def open_edit_event(self, event):

        self.open_event_modal(event)

    def open_event_modal(self, event=None):

        editing = event is not None

        modal = ctk.CTkToplevel(
            self
        )

        modal.title(
            "Edit Event" if editing else "Create Event"
        )

        modal.geometry(
            "520x650"
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
            text="Edit Event" if editing else "Create Event",
            font=("Segoe UI", 24, "bold")
        ).pack(
            pady=(25, 20)
        )

        def add_field(label, placeholder="", value=""):

            ctk.CTkLabel(
                modal,
                text=label,
                font=("Segoe UI", 12, "bold")
            ).pack(
                anchor="w",
                padx=55
            )

            entry = ctk.CTkEntry(
                modal,
                width=400,
                height=40,
                placeholder_text=placeholder
            )

            entry.pack(
                pady=(5, 12)
            )

            if value:
                entry.insert(
                    0,
                    str(value)
                )

            return entry

        title_entry = add_field(
            "Title",
            "Event title",
            event.get("title", "") if editing else ""
        )

        description_entry = add_field(
            "Description",
            "Event description",
            event.get("description", "") if editing else ""
        )

        type_entry = add_field(
            "Event Type",
            "Hackathon / Workshop / Seminar",
            event.get("event_type", "") if editing else ""
        )

        start_entry = add_field(
            "Start Time",
            "2026-09-25T10:00:00",
            event.get("start_time", "") if editing else ""
        )

        end_entry = add_field(
            "End Time",
            "2026-09-25T17:00:00",
            event.get("end_time", "") if editing else ""
        )

        location_entry = add_field(
            "Location",
            "Seminar Hall",
            event.get("location", "") if editing else ""
        )

        def save():

            title = title_entry.get().strip()
            description = description_entry.get().strip()
            event_type = type_entry.get().strip()
            start_time = start_entry.get().strip()
            end_time = end_entry.get().strip()
            location = location_entry.get().strip()

            if not title:
                messagebox.showerror(
                    "Validation Error",
                    "Please enter an event title.",
                    parent=modal
                )
                return

            if not event_type:
                messagebox.showerror(
                    "Validation Error",
                    "Please enter an event type.",
                    parent=modal
                )
                return

            if not start_time or not end_time:
                messagebox.showerror(
                    "Validation Error",
                    "Start time and end time are required.",
                    parent=modal
                )
                return

            try:

                if editing:

                    update_event(
                        event["id"],
                        title=title,
                        description=description,
                        event_type=event_type,
                        start_time=start_time,
                        end_time=end_time,
                        location=location
                    )

                else:

                    create_event(
                        title,
                        description,
                        event_type,
                        start_time,
                        end_time,
                        location
                    )

                modal.destroy()
                self.load_events()

            except Exception as error:

                messagebox.showerror(
                    "API Error",
                    str(error),
                    parent=modal
                )

        ctk.CTkButton(
            modal,
            text="Save Event",
            width=400,
            height=42,
            corner_radius=8,
            fg_color=self.ACCENT,
            hover_color=self.ACCENT_HOVER,
            command=save
        ).pack(
            pady=15
        )

    # =========================================================
    # DELETE EVENT
    # =========================================================

    def confirm_delete(self, event):

        confirmed = messagebox.askyesno(
            "Delete Event",
            f"Are you sure you want to delete:\n\n"
            f"{event.get('title', 'this event')}?"
        )

        if not confirmed:
            return

        try:

            delete_event(
                event["id"]
            )

            self.load_events()

        except Exception as error:

            self.show_error(
                f"Unable to delete event:\n\n{error}"
            )

    # =========================================================
    # BADGE
    # =========================================================

    def create_badge(
        self,
        parent,
        text,
        color
    ):

        badge = ctk.CTkLabel(
            parent,
            text=f"  {text}  ",
            height=26,
            corner_radius=7,
            fg_color=f"{color}22",
            text_color=color,
            font=("Segoe UI", 11, "bold")
        )

        badge.pack(
            side="right",
            padx=(10, 0)
        )

    # =========================================================
    # INFO ITEM
    # =========================================================

    def create_info_item(
        self,
        parent,
        label,
        value
    ):

        item = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )

        item.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 20)
        )

        ctk.CTkLabel(
            item,
            text=label,
            font=("Segoe UI", 10, "bold"),
            text_color=self.TEXT_MUTED
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            item,
            text=str(value),
            font=("Segoe UI", 12),
            text_color=self.TEXT_SECONDARY,
            wraplength=250
        ).pack(
            anchor="w",
            pady=(3, 0)
        )

    # =========================================================
    # EMPTY
    # =========================================================

    def show_empty(self):

        card = ctk.CTkFrame(
            self.events_container,
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
            text="No events found",
            font=("Segoe UI", 20, "bold"),
            text_color=self.TEXT_PRIMARY
        ).pack(
            pady=(40, 6)
        )

        ctk.CTkLabel(
            card,
            text="There are currently no events in this category.",
            font=("Segoe UI", 13),
            text_color=self.TEXT_SECONDARY
        ).pack(
            pady=(0, 40)
        )

    # =========================================================
    # ERROR
    # =========================================================

    def show_error(self, message):

        card = ctk.CTkFrame(
            self.events_container,
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
            text="Unable to load events",
            font=("Segoe UI", 20, "bold"),
            text_color=self.TEXT_PRIMARY
        ).pack(
            pady=(35, 10)
        )

        ctk.CTkLabel(
            card,
            text=message,
            font=("Segoe UI", 13),
            text_color=self.TEXT_SECONDARY,
            wraplength=800,
            justify="center"
        ).pack(
            padx=30,
            pady=(0, 35)
        )