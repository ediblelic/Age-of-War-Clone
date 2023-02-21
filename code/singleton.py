class Singleton:
    _instance = None
    def __init__(self):
        if  Singleton._instance is not None:
            raise PermissionError("Singleton exist already!")
        Singleton._instance = self
    @classmethod  #it can be @staticmethod without args
    def get_instance(cls):
        if not cls._instance:
            cls._instance = Singleton()
        return cls._instance
    