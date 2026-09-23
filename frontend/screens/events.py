import customtkinter as ctk

from api_client import get_events


class EventsPage(ctk.CTkFrame):

    # =========================================================
    # DESIGN SYSTEM
    # =========================================================

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

        # -----------------------------------------------------
        # Header
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
            text="Events",
            font=("Segoe UI", 30, "bold"),
            text_color=self.TEXT_PRIMARY
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            header,
            text="Discover what's happening across your college.",
            font=("Segoe UI", 14),
            text_color=self.TEXT_SECONDARY
        ).pack(
            anchor="w",
            pady=(5, 0)
        )

        # -----------------------------------------------------
        # Filter Bar
        # -----------------------------------------------------

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

        # -----------------------------------------------------
        # Events Container
        # -----------------------------------------------------

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
    # FILTER BUTTON
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

    # =========================================================
    # STATUS FILTER
    # =========================================================

    def change_status(self, status):

        self.current_status = status

        self.update_filter_buttons()

        self.load_events()

    # =========================================================
    # UPDATE FILTER BUTTONS
    # =========================================================

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

                self.create_event_card(
                    event
                )

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

        # -----------------------------------------------------
        # Main Content
        # -----------------------------------------------------

        content = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        content.pack(
            fill="x",
            padx=24,
            pady=20
        )

        # -----------------------------------------------------
        # Top Row
        # -----------------------------------------------------

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

        # -----------------------------------------------------
        # Description
        # -----------------------------------------------------

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

        # -----------------------------------------------------
        # Information Grid
        # -----------------------------------------------------

        info_frame = ctk.CTkFrame(
            content,
            fg_color="transparent"
        )

        info_frame.pack(
            fill="x",
            pady=(4, 0)
        )

        location = event.get(
            "location",
            "Not specified"
        )

        start_time = event.get(
            "start_time",
            "Not specified"
        )

        end_time = event.get(
            "end_time",
            "Not specified"
        )

        self.create_info_item(
            info_frame,
            "LOCATION",
            location
        )

        self.create_info_item(
            info_frame,
            "START",
            start_time
        )

        self.create_info_item(
            info_frame,
            "END",
            end_time
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
    # EMPTY STATE
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
    # ERROR STATE
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