from ..button import Button
from ..screen import Scene
from ..text import Text

title = '''     __                                                    
    / /\                                                   
   / / /    ███████   ███████   █     █   █     █   ███████
  / / /     █         █         █     █   ██    █   █     █
 / /  \     █         █         █     █   █ █   █   █     █
/_/ /\ \    ███████   █         ███████   █  █  █   █     █
\_\/\ \ \   █         █         █     █   █   █ █   █     █
     \ \ \  █         █         █     █   █    ██   █     █
      \ \ \ ███████   ███████   █     █   █     █   ███████
       \_\/                                                '''

def get_scene(screen):
    main_menu = Scene()

    x = 0
    labels = {}
    for line in title.split("\n"):
        labels[f"title{x + 1}"] = Text(screen, line, (620, 30 + x * 24), "#ffffff", "assets/mono.ttf", 18)
        x += 1

    labels[f"title{x + 1}"] = Text(screen, "Client", (640, 320), "#ffffff", "assets/minecraft.ttf", 60)

    buttons = {}
    buttons["singleplayer"] = Button(screen, "Singleplayer", (640, 415), (500, 30))
    buttons["multiplayer"] = Button(screen, "Multiplayer", (640, 460), (500, 30))
    buttons["launch"] = Button(screen, "Launch", (550, 505), (320, 30))
    buttons["version"] = Button(screen, "1.8.9", (805, 505), (170, 30))

    def _change_version(version):
        buttons["version"] = Button(screen, version, (805, 505), (170, 30))

    callbacks = {}
    callbacks["Singleplayer"] = lambda: None
    callbacks["Multiplayer"] = lambda: None
    callbacks["Launch"] = lambda: None
    callbacks["1.8.9"] = lambda: _change_version("Forge 1.8.9")
    callbacks["Forge 1.8.9"] = lambda: _change_version("Skyblock 1.8.9")
    callbacks["Skyblock 1.8.9"] = lambda: _change_version("1.20.2")
    callbacks["1.20.2"] = lambda: _change_version("Fabric 1.20.2")
    callbacks["Fabric 1.20.2"] = lambda: _change_version("Iris 1.20.2")
    callbacks["Iris 1.20.2"] = lambda: _change_version("1.8.9")

    main_menu.labels = labels
    main_menu.buttons = buttons
    main_menu.callbacks = callbacks

    return main_menu