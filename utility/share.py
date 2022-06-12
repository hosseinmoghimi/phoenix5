def whatsapp_link(number):
    # print("number")
    # print(number)
    # if len(number)>5:
    #     print(number[0:2])
    #     print(number[0:2]==['0','9'])
    #     print(number[0:2]=="09")
    # print(100*"#")
    if number[0:2]=="09":
        number="+98"+number[1:]
    return f"https://wa.me/{number}"