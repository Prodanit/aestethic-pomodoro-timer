import pygame

class Notifier:
    def notify(self, event_type, config):
        pass

class SoundNotifier(Notifier):
    def __init__(self):
        self.sounds_loaded = False
        try:
            pygame.mixer.init()
            self.sounds = {
                "click": pygame.mixer.Sound("sounds/ui_click.mp3"),
                "task_complete": pygame.mixer.Sound("sounds/task_completed.mp3"), 
                "timer_finish": pygame.mixer.Sound("sounds/notification_ping.mp3"),
                "add_task": pygame.mixer.Sound("sounds/pop_sound.mp3"),
                "delete_task": pygame.mixer.Sound("sounds/delete_sound.mp3")
                }
                               
            self.sounds_loaded = True
            print("Sound uploaded correctly.")
        except Exception as e:
            print(f"Error uploading sounds: {e}")
        
    def notify(self, event_type, config):
        if self.sounds_loaded and isinstance(config, dict) and config.get("sound_enabled", False):
            if event_type in self.sounds:
                self.sounds[event_type].play()

class ConsoleNotifier(Notifier):
    def notify(self, event_type, config):
        print(f"[CONSOLE NOTIFIER]: Evento recibido - '{event_type}")

    
                   

    
    
    
    

