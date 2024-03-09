from abc import ABC


class AbstractPermission(ABC):
    def __init__(self):
        self.write = False
        self.read = False
        self.delete = False
        self.post = False
        self.export = False


class UserPermission(AbstractPermission):
    def __init__(self):
        super().__init__()

        self.write = True
        self.read = True
        self.delete = True


class ModeratorPermission(AbstractPermission):
    def __init__(self):
        super().__init__()

        self.write = True
        self.read = True
        self.delete = True
        self.post = True


class AdminPermission(AbstractPermission):
    def __init__(self):
        super().__init__()

        self.write = True
        self.read = True
        self.delete = True
        self.post = True
        self.export = True
