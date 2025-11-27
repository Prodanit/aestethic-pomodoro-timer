from CTkMessagebox import CTkMessagebox
import customtkinter as ctk


class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, master, db_manager, current_config, main_font):
        super().__init__(master)

        self.master_app = master #Ref a la ventana principal
        self.db = db_manager # Manejar la bd

        self.title("Settings")
        self.geometry("400x400")
        self.transient(master) #Para mantenerla por encima de la main page
        self.grab_set() # Bloquea la interaccio con la ventana principal hasta que esta se cierre
        self.iconbitmap("graphics/cherry.ico")

        #WIdgets
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        current_config = self.db.get_settings()

        # Entry pomodoro
        ctk.CTkLabel(main_frame, text="pomodoro (minutes):", font=main_font).pack(anchor="w")
        self.pomodoro_entry = ctk.CTkEntry(main_frame, font=main_font)
        self.pomodoro_entry.insert(0, current_config.get("pomodoro_mins", 25))
        self.pomodoro_entry.pack(fill="x", pady=(0,10))

        #Entry short break
        ctk.CTkLabel(main_frame, text="short break (minutes):", font=main_font).pack(anchor="w")
        self.short_break_entry = ctk.CTkEntry(main_frame, font=main_font)
        self.short_break_entry.insert(0, current_config.get("short_break_mins", 5))
        self.short_break_entry.pack(fill="x", pady=(0,10))

        #Entry long break
        ctk.CTkLabel(main_frame, text="long break (minutes):", font=main_font).pack(anchor="w")
        self.long_break_entry = ctk.CTkEntry(main_frame, font=main_font)
        self.long_break_entry.insert(0, current_config.get("long_break_mins", 10))
        self.long_break_entry.pack(fill="x", pady=(0,10))

        # Switch sonido
        self.sound_switch = ctk.CTkSwitch(main_frame, text="enable sound", font=main_font)
        if current_config.get("sound_enabled", True):
            self.sound_switch.select()
        self.sound_switch.pack(anchor="w",pady=(0,20))
        #Boton Save
        save_button = ctk.CTkButton(main_frame, text="save and close", font= main_font, text_color="#FDF5F5",                                    command=self.save_and_close)
        save_button.pack(pady=20)
    
    def save_and_close(self):
        try:
            new_pomodoro = int(self.pomodoro_entry.get())
            new_short_break = int(self.short_break_entry.get())
            new_long_break = int(self.long_break_entry.get())
            new_sound_enabled = self.sound_switch.get() == 1 # .get() devuelve 1 si está on, 0 si está off

            if new_pomodoro <= 0 or new_short_break <= 0 or new_long_break <= 0:
                raise ValueError("Time values must be positive integers.")
                return
            
            new_setting = {
                "pomodoro_mins": new_pomodoro,
                "short_break_mins": new_short_break,
                "long_break_mins": new_long_break,
                "sound_enabled": new_sound_enabled
            }
            # Guardar configuraciones en la base de datos
            self.db.save_settings(new_setting)
            self.master_app.apply_new_settings()
            self.destroy()

        except ValueError:
            CTkMessagebox(title="entry error", message="please introduce valid numbers", icon="warning").lift()
        except Exception as e:
            CTkMessagebox(title="error", message=f"an error happened at save. {e}", icon="error").lift()
        