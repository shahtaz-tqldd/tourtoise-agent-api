from datetime import datetime
def print_log(name: str = "LOG", message: str = None):
    print(f"------------------{name} : {datetime.now()}------------------")
    print(message)
    print("--------------------------------------------------")