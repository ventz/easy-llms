# llms.py
import importlib
import pkgutil

class LLMs:
    def __init__(self):
        pass

    @classmethod
    def auth(cls):
        pass

    def updateLLM(self):
        pass

    def run(self, prompt):
        pass

    @classmethod
    def list(cls):
        subclasses = cls.__subclasses__()
        subclass_names = [cls.name.lower() for cls in subclasses]
        return subclass_names
