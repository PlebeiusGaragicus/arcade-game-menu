class SingletonDataclass:
    _instance = None

    def __init__(self):
        # Singleton pattern must prevent normal instantiation
        raise Exception("Cannot directly instantiate a Singleton. Access via get_instance()")

    @classmethod
    def get_instance(cls):
        # This is the only way to access the one and only instance
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls._instance.__post_init__() # __post_init__() is needed becuase Config is a dataclass
        return cls._instance



# class Singleton:
#     _instance = None

#     def __init__(self):
#         # Singleton pattern must prevent normal instantiation
#         raise Exception("Cannot directly instantiate a Singleton. Access via get_instance()")

#     @classmethod
#     def get_instance(cls):
#         # This is the only way to access the one and only instance
#         if cls._instance:
#             return cls._instance
#         else:
#             # Instantiate the one and only Controller instance
#             return cls.configure_instance()


class Singleton:
    _instance = None

    def __init__(self):
        # Singleton pattern must prevent normal instantiation
        raise Exception("Cannot directly instantiate a Singleton. Access via get_instance()")

    @classmethod
    def get_instance(cls):
        # This is the only way to access the one and only instance
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
        return cls._instance
