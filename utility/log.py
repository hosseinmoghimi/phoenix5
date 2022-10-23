from phoenix.server_settings import DEBUG
def leolog(*args, **kwargs):
    if not DEBUG:
        return
    print("")
    print("")
    for a in kwargs:
        print(80*" #")
        print(a)
        print(80*" #")
        print(kwargs[a])
    print(80*" #")
    print("")
    print("")