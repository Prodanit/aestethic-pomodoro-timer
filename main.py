import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from PIL import Image
import settings
from ui_components import SettingsWindow
from DBManager import DatabaseManager
from sound_manager import SoundNotifier, ConsoleNotifier

ctk.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("cherry.json")


class PomodoroApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Pomodoro Timer")
        self.geometry("800x600")
        self.iconbitmap("graphics/tomato-sin-fondo.ico")
        self.configure(fg_color=settings.BG_COLOR)

        self.db = DatabaseManager()
        if not self.db.is_connected:
            CTkMessagebox(title="Error connecting", message="Crtical error. Could not conenct to the data base", icon="cancel")
            self.after(100, self.destroy)
            return
        self.config = self.db.get_settings()
        self.notifiers = [
            SoundNotifier(),
            ConsoleNotifier()
        ]
        self.load_fonts()
        self.load_icons()

        self.create_widgets()

        # Inicializamos
        self.is_running = False
        self._timer_job = None #  1. Inicializamos la variable para guardar el "ticket"
        self.current_mode = "pomodoro"
        self.pomodoros_since_long_break = 0
        self.remaining_time = self.config["pomodoro_mins"] * 60

        self.update_timer_display()
        self.load_tasks()

    def load_fonts(self):
        # Fonts
        try:
            self.font_timer = ctk.CTkFont(family="Space Grotesk", size=100, weight="bold")
            self.font_main = ctk.CTkFont(family="Space Grotesk", size=16, weight="bold")
        except FileNotFoundError:
            print("Advertencia: Fuentes no encontradas, se usan por defecto.")
            self.font_timer = ctk.CTkFont(family="Helvetica", size=100, weight="bold")
            self.font_main = ctk.CTkFont(family="Arial", size=16)

    def load_icons(self):
        try:
            delete_image = Image.open("graphics/delete_icon.png")
            self.delete_icon = ctk.CTkImage(light_image=delete_image, dark_image=delete_image, size=(20,20))
        except FileNotFoundError:
            print("No hay img de delete")
            self.delete_icon = None
        
    def create_widgets(self):
        #Frame izquierdo
        izq_frame = ctk.CTkFrame(self, fg_color="transparent", width=400)
        izq_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        # Frame superior - modos
        state_frame = ctk.CTkFrame(izq_frame, fg_color="transparent")
        state_frame.pack(pady=(15, 5))

        self.pomodoro_button = ctk.CTkButton(
            state_frame, 
            text="pomodoro", 
            font=self.font_main,
            height=40,
            corner_radius=500, 
            fg_color="white", 
            text_color="#6D4C6C",
            hover=False,
        )
        self.pomodoro_button.pack(side="left", padx=5)
        self.pomodoro_button.configure(command=lambda: self.switch_mode("pomodoro"))

        self.short_break_button = ctk.CTkButton(
            state_frame, 
            text="short break", 
            font=self.font_main,
            height=40,
            corner_radius=500, 
            fg_color="transparent",
            border_width=2, 
            border_color="#6D4C6C",
            text_color=("#6D4C6C", "#FDF5F5")
        )
        self.short_break_button.pack(side="left", padx=5)
        self.short_break_button.configure(command=lambda: self.switch_mode("short_break"))

        self.long_break_button = ctk.CTkButton(
            state_frame, 
            text="long break", 
            font=self.font_main,
            height=40,
            corner_radius=500, 
            fg_color="transparent",
            border_width=2,
            border_color="#6D4C6C",
            text_color=("#6D4C6C", "#FDF5F5")
        )
        self.long_break_button.pack(side="left", padx=5)
        self.long_break_button.configure(command=lambda: self.switch_mode("long_break"))

        # Frame timer
        timer_frame = ctk.CTkFrame(izq_frame, fg_color="transparent")
        timer_frame.pack(pady=20, expand=True)

        self.timer_label = ctk.CTkLabel(
            timer_frame, text="",
            font=self.font_timer, text_color=("#6D4C6C")
        )
        self.timer_label.pack(pady=10, expand=True)

        # Frame botones
        control_frame = ctk.CTkFrame(izq_frame, fg_color="transparent")
        control_frame.pack(pady=(0, 20))

        self.start_button = ctk.CTkButton(
            control_frame, 
            text="start",
            font=self.font_main, 
            height=40,
            corner_radius=500,
            command=self.start_timer
        )
        self.start_button.pack(side="left", padx=10)
        self.start_button.configure(command=self.toggle_timer)

        self.reset_button = ctk.CTkButton(
            control_frame, 
            text="reset",
            font=self.font_main, 
            height=40,
            corner_radius=500,
            command=self.reset_timer
        )
        self.reset_button.pack(side="left", padx=10)
        self.reset_button.configure(command=self.reset_timer)

        # Configuracion
        self.settings_button = ctk.CTkButton(
            control_frame,
            text="⚙️ settings",
            font=(self.font_main,15,"bold"),
            height=40,
            corner_radius=500,
            command=self.open_settings_window
        )
        self.settings_button.pack(side="left", padx=10)

        #Frame derecha (tasks list)
        der_frame = ctk.CTkFrame(self, fg_color=("#FCEFEE"), corner_radius=12, width=400)
        der_frame.pack(side="right", fill="y", padx=(0,20), pady=20)
        der_frame.pack_propagate(False)
        
        task_header_frame = ctk.CTkFrame(
            der_frame, fg_color="transparent"
        )
        task_header_frame.pack(fill="x", padx=10, pady=10)

        tasks_Label = ctk.CTkLabel(
            task_header_frame,
            text="to-do list",
            font=ctk.CTkFont(family="Montserrat", size=20, weight="bold"),
            wraplength=350,
            anchor="w",
            justify="left"
        )
        tasks_Label.pack(pady=(10, 15), padx=20)

        # Añadir tareas
        add_task_frame=ctk.CTkFrame(
            der_frame,
            fg_color="transparent"
        )
        add_task_frame.pack(fill="x", padx=10, pady=(0,10))

        self.task_entry = ctk.CTkEntry(add_task_frame,
            placeholder_text = "add new task...", 
            font=self.font_main)
        self.task_entry.pack(side="left", fill="x", expand=True, padx=(0,10))
        self.task_entry.bind("<Return>", self.add_task_event)

        self.add_task_button = ctk.CTkButton(
            add_task_frame,
            text="add",
            font=self.font_main,
            width=60
        )
        self.add_task_button.pack(side="left")
        self.add_task_button.configure(command=self.add_task_event)

        self.task_list_frame = ctk.CTkScrollableFrame(
            der_frame,
            fg_color="transparent"
        )
        self.task_list_frame.pack(fill="both", expand=True, padx=10, pady=10)
   
    # Timer functions
    def toggle_timer(self):
        self._notify_all("click")
        if self.is_running:
            self.pause_timer()
        else:
            self.start_timer()

    def start_timer(self):
        self.is_running = True
        self.start_button.configure(text="pause")
        self.countdown()

    def pause_timer(self):
        self.is_running = False
        self.start_button.configure(text="start")
        if self._timer_job:
            self.after_cancel(self._timer_job)

    def reset_timer(self):
        self._notify_all("click")
        self.pause_timer()
        self.remaining_time = self.config[f"{self.current_mode}_mins"] * 60
        self.update_timer_display()

    def countdown(self):
        if self.is_running and self.remaining_time > 0:
            self.remaining_time -= 1
            self.update_timer_display()
            # Guardamos el ID del job 'after' para poder cancelarlo despues
            self._timer_job = self.after(1000, self.countdown)

        elif self.is_running and self.remaining_time == 0:
            self.timer_finished()
    
    def timer_finished(self):
        self.pause_timer()
        self._notify_all("timer_finish")
        print("Time has finished")
        next_mode=""
        
        if self.current_mode == "pomodoro":
            self.pomodoros_since_long_break += 1

            if self.pomodoros_since_long_break % 4 == 0:
                next_mode ="long_break"
                message = "good job! time for a long break"
            else: 
                next_mode = "short_break"
                message = "time for a short break!"
        else:
            next_mode = "pomodoro"
            message = "back to work!"
        
        CTkMessagebox(title="finished cycle", message = message, icon="check")
        
        self.switch_mode(next_mode, is_automatic=True)
        self.start_timer()        
    
    def switch_mode(self, mode:str, is_automatic: bool = False):
        if not is_automatic:
            self._notify_all("click")
        
        self.current_mode = mode
        self.pause_timer()
        self.remaining_time = self.config[f"{mode}_mins"] * 60
        self.update_timer_display()

        self.pomodoro_button.configure(**(settings.STYLE_ACTIVO if mode == "pomodoro" else settings.STYLE_INACTIVO))
        self.short_break_button.configure(**(settings.STYLE_ACTIVO if mode == "short_break" else settings.STYLE_INACTIVO))
        self.long_break_button.configure(**(settings.STYLE_ACTIVO if mode == "long_break" else settings.STYLE_INACTIVO))
    
    def update_timer_display(self):
        mins = self.remaining_time // 60
        secs = self.remaining_time % 60
        self.timer_label.configure(text=f"{mins:02d}:{secs:02d}")

    # FUnciones de tareas
    def load_tasks(self):
        for widget in self.task_list_frame.winfo_children():
            widget.destroy()

        tasks = self.db.get_all_tasks()

        for task in tasks:
            self._create_task_widget(task)
    
    def _create_task_widget(self, task_data):
        task_id = task_data["_id"]

        task_frame = ctk.CTkFrame(self.task_list_frame,
            fg_color=("#E5D9D8", "#333"), corner_radius=10)
        task_frame.pack(fill="x", padx=5, pady=5)

        checkbox = ctk.CTkCheckBox(
            task_frame,
            text="",
            width=20,
            fg_color="#6D4C6C",
            hover_color="#8F6B8E",
            checkmark_color="white"
        )
        label = ctk.CTkLabel(
            task_frame,
            text=task_data["text"],
            font=self.font_main,
            wraplength=250,
            anchor="w",
            justify="left"
        )

        if task_data["completed"]:
            checkbox.select()
            checkbox.configure(font=ctk.CTkFont(family="Space Grotesk", size=16, overstrike=True))
        
        delete_button = ctk.CTkButton(
            task_frame,
            text="",
            image=self.delete_icon,
            width=20,
            height=20,
            font=ctk.CTkFont(size=18),
            fg_color="transparent",
            text_color="black",
            hover_color="#E57373",
            command = lambda id=task_id: self.delete_task(id)
        )
        delete_button.pack(side="right", padx=10, pady=5)
        checkbox.pack(side="left", padx=(10,5), pady=5)
        label.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        label.bind("<Button-1>", lambda event, chk=checkbox: self.toggle_checkbox(chk))
        checkbox.configure(command=lambda id=task_id, chk=checkbox: self.toggle_task_status(id, chk.get() == 1))

        if task_data["completed"]:
            checkbox.select()
            label.configure(font=ctk.CTkFont(family="Space Grotesk", size=16, overstrike=True))
    
    def toggle_checkbox(self, checkbox_widget):
        checkbox_widget.toggle()
    
    # El 'event=None' permite que la función sea llamada por un botón (sin evento)
    # o por la tecla Enter (con evento)
    def add_task_event(self, event=None):
        self._notify_all("add_task")
        new_task_event = self.task_entry.get().strip()

        if new_task_event:
            self.db.add_task(new_task_event)
            self.task_entry.delete(0, "end")
            self.load_tasks()
    
    def delete_task(self, task_id):
        self.db.delete_task(task_id)
        self._notify_all("delete_task")
        self.load_tasks()

    def toggle_task_status(self, task_id, is_completed):
        if is_completed:
            self._notify_all("task_complete")
        self.db.update_task_status(task_id, is_completed)
        self.load_tasks()

    # Funcion para ventanas secundarias

    def open_settings_window(self):
        if not hasattr(self, 'setting_win') or not self.settings_win.winfo_exists():
            self.settings_win = SettingsWindow(master=self,db_manager=self.db,
            current_config=self.config,
            main_font=self.font_main)
    
    def apply_new_settings(self):
        print("Aplicando nueva config...")
        self.config = self.db.get_settings()

        if not self.is_running:
            self.switch_mode(self.current_mode)

    def _notify_all(self, event_type):
        for notifier in self.notifiers:
            notifier.notify(event_type, self.config)
    

app = PomodoroApp()
app.mainloop()