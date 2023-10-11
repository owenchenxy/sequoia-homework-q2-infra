import yaml

class Config():
    _instance = None
    config = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(cls, *args, **kwargs)
            try:
                with open('config.yaml', "r") as file:
                    cls.config = yaml.safe_load(file)
            except:
                print("Error: config.yaml not found.")
                exit(1)
        return cls._instance
    