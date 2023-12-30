class Scene:
    def __init__(self):
        self.labels = {}
        self.buttons = {}
        self.callbacks = {}

        self.components = []

        self.visible = True

    def add_component(self, component):
        self.components.append(component)
    
    def draw(self):
        for label in self.labels.values():
            label.draw()
        
        for button in self.buttons.values():
            button.draw()

        for component in self.components:
            if self.visible:
                component.draw()
    
    def show(self):
        self.visible = True
    
    def hide(self):
        self.visible = False