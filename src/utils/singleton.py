"""Singleton pattern implementation."""

class Singleton:
    _instances = {}

    def __new__(cls, *_args, **_kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__new__(cls)
        return cls._instances[cls]
