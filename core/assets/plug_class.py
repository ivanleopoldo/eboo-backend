# classes
class Base:
    """Base Plugin Class"""
    plugins = []

    def __init_subclass__(self):
        super().__init_subclass__()
        self.plugins.append(self)