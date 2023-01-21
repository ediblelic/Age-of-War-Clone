class Singleton:
    _instance = None
    def __init__(self):
        if  Singleton._instance != None:
            raise Exception("Singleton exist already!")
        else:
            Singleton._instance = self

    @classmethod  #it can be @staticmethod without args
    def get_instance(cls):
        if not cls._instance:
            cls._instance = Singleton()
        return cls._instance

