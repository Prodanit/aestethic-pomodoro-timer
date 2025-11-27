Pomodoro App – Gestor de Tiempo y Tareas.
UNIVERSIDAD TECNOLÓGICA DE PEREIRA
Facultad de Ingenierías
IS553 Programación IV
Autoras
Valentina Lasprilla Velásquez
Gabriela Saldarriaga Saldarriaga
Docente
Andrés Felipe Ramírez Correa
Pereira, Noviembre del 2025
Descripción del Proyecto
Este proyecto es una aplicación de escritorio diseñada para la gestión del tiempo y la productividad personal. Su objetivo es ayudar a estudiantes, profesionales y cualquier persona que busque optimizar su rendimiento diario. La aplicación se basa en la técnica Pomodoro, un método que divide el tiempo de estudio o trabajo en intervalos de concentración seguidos de descansos cortos.
La "Pomodoro App" ofrece una herramienta intuitiva y funcional para organizar tareas, mantener la concentración durante períodos prolongados y combatir la procrastinación.
Características Principales
Requerimientos Funcionales
Gestión de Tareas:
Añadir, eliminar y marcar tareas como completadas.
Los cambios en la lista de tareas se almacenan en una base de datos MongoDB.
Temporizador Pomodoro:
Configurar la duración de los intervalos de trabajo y descanso.
Iniciar, pausar y reiniciar el temporizador.
Visualizar el tiempo restante en tiempo real.
Recibir notificaciones al finalizar cada intervalo.
Configuración Personalizada:
Activar o desactivar el sonido de las notificaciones.
Las configuraciones de tiempo y sonido se guardan en MongoDB y se cargan al iniciar la aplicación.
Requerimientos No Funcionales
Usabilidad: Interfaz intuitiva, fácil de usar y con un diseño visual consistente.
Rendimiento: La aplicación inicia y responde a las acciones del usuario de manera fluida.
Compatibilidad: Compatible con Windows 10 o superior y pantallas con una resolución mínima de 1280x720.
Confiabilidad: Almacenamiento seguro de los datos del usuario para evitar pérdidas.
Seguridad: Conexión segura con MongoDB mediante SRV y cifrado TLS. Las credenciales de acceso a la base de datos están protegidas.
Mantenibilidad: Configuración modular para facilitar el mantenimiento del código.
Tecnologías Utilizadas
El sistema fue implementado en Python y utiliza las siguientes librerías:
CustomTkinter: Para la creación de una interfaz gráfica moderna y profesional.
CTkMessagebox: Para mostrar ventanas emergentes de alertas y notificaciones.
Pillow (PIL): Para cargar y mostrar imágenes en la interfaz, como íconos y fondos.
Pymongo: Como driver oficial para la conexión y realización de operaciones CRUD con la base de datos MongoDB.
bson: Para la serialización de datos y el manejo de ObjectId de MongoDB.
datetime: Para la gestión de fechas, horas e intervalos de tiempo.
sys y os: Para interactuar con el sistema operativo, gestionar rutas y facilitar el empaquetado de la aplicación.
pygame: Para la reproducción de sonidos, como las notificaciones del temporizador.
Flujo de Trabajo
Inicio de la Aplicación: El usuario abre el programa y el sistema intenta conectarse a MongoDB.
Interfaz Principal: Si la conexión es exitosa, se cargan las tareas y configuraciones. El usuario puede gestionar su lista de tareas, iniciar el temporizador y acceder a la configuración.
Configuración (Settings): El usuario puede modificar la duración de los intervalos de trabajo/descanso y activar/desactivar el sonido de las notificaciones.
Cierre de la Aplicación: Al cerrar el programa, todos los datos ya se encuentran guardados en MongoDB.
Estructura del Proyecto
El proyecto sigue una arquitectura orientada a objetos, con las siguientes clases principales:
DatabaseManager: Gestiona la conexión y las operaciones con la base de datos MongoDB.
PomodoroApp: Clase principal que controla la lógica de la aplicación y la interfaz de usuario.
SettingsWindow: Maneja la ventana de configuración y la interacción del usuario con las opciones.
Notifier (y sus subclases SoundNotifier, ConsoleNotifier): Se encargan de las notificaciones visuales y sonoras.
Para una visión más detallada, consulte los diagramas de clases y de flujo de trabajo incluidos en la documentación del proyecto.
Casos de Uso
La aplicación permite a los usuarios realizar las siguientes acciones principales:
Gestión de Tareas: Añadir, eliminar, marcar y desmarcar tareas.
Temporizador Pomodoro: Iniciar, pausar y reiniciar los ciclos de trabajo y descanso.
Configuración: Personalizar los tiempos de los intervalos y las notificaciones de sonido.
Todos los cambios relevantes se guardan automáticamente en la base de datos para persistencia de la información.