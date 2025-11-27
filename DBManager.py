from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from bson import ObjectId #permite guardar fechas mejor y usar el metodo sort (es de tipo binario)
from datetime import datetime

CONNECTION_STRING = "mongodb+srv://tina:g4torojo@cluster0.yjsoclc.mongodb.net/"

class DatabaseManager:
    def __init__(self):
        self._client = None
        self._db = None
        self._settings_collection = None
        self._tasks_collection = None
        self.is_connected = False
        
        try:
            self._client = MongoClient(CONNECTION_STRING)
            self._client.admin.command('ping')
            self.is_connected = True
            print("Conexión a MongoDB exitosa.")

        except ConnectionFailure as e:
            print(f"Error: No se pudo conectar a MongoDB. {e}")
            self.is_connected = False  
            return

        if self.is_connected:
            self._db = self._client["PomodoroApp"]            
            self._settings_collection = self._db["settings"]
            self._tasks_collection = self._db["tasks"]      

    def get_settings(self):
        if self._settings_collection is None:
            return None
        settings = self._settings_collection.find_one({"_id": "main_config"})

        if settings is None:
            default_settings = {
                "_id": "main_config",
                "pomodoro_mins": 25,
                "short_break_mins": 5,
                "long_break_mins": 10,
                "sound_enabled": True
            }
            self._settings_collection.insert_one(default_settings)
            return default_settings
        return settings

    def save_settings(self, settings_data):
        if self._settings_collection is None:
            return
        self._settings_collection.update_one(
            {"_id": "main_config"},
            {"$set": settings_data},
             upsert=True
        )

    def get_all_tasks(self):
        """Devuelve una lista de todas las tareas no completadas, luego las completadas."""
        if self._settings_collection is None: return
        return list(self._tasks_collection.find().sort([("completed", 1), ("created_at", -1)])) # ordena primero por no completadas, luego por más nuevas
    
    def add_task(self, text):
        if self._settings_collection is None: return None
        task_document = {
            "text": text,
            "completed" : False,
            "created_at": datetime.utcnow()
        }
        return self._tasks_collection.insert_one(task_document).inserted_id
    
    def update_task_status(self, task_id, is_completed):
        if self._settings_collection is None: return
        # ObjectId() es crucial para que MongoDB encuentre el documento por su _id
        self._tasks_collection.update_one(
            {"_id": ObjectId(task_id)},
            {"$set": {"completed": is_completed}}
        )
    def delete_task(self, task_id):
        if self._settings_collection is None: return
        self._tasks_collection.delete_one({"_id": ObjectId(task_id)})


# Al final de db_manager.py (solo para probar)
if __name__ == "__main__":
    db = DatabaseManager()

    if db.client:
        print("\n--- Probando get_settings ---")
        config = db.get_settings()
        print("Configuración actual:", config)
        
        print("\n--- Probando save_settings ---")
        db.save_settings({"pomodoro_mins": 25, "sound_enabled": False})
        
        print("\n--- Verificando los cambios ---")
        new_config = db.get_settings()
        print("Configuración nueva:", new_config)