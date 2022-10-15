from phoenix.server_settings import DEBUG
def leolog(*args, **kwargs):
    if not DEBUG:
        return
    print("")
    print(80*" #")
    for a in kwargs:
        print(f"{a} = {kwargs[a]}")
    print(80*" #")
    print("")