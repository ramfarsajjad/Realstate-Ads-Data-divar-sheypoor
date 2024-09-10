def dicfdr (list, key, value):
    
    check = 0
    for item in list:
        if key in item:
            if item[key] == value:
                check += 1
                break

    if check == 1:
        return item
    else:
        return None


def keyfdr (list, key):
    
    check = 0
    for item in list:
        if key in item:        
            check += 1
            break

    if check == 1:
        return item['value']
    else:
        return None


def multifdr (list, key, value1, value2):
    passdic = dict()
    passoption = set()
    check = 0
    counter = 0
    for item in list:
        counter += 1
        if item[key] == value1:
            passdic[item["data"]["title"]] = item["data"]["value"]
            check += 1

        elif item[key] == value2:
            passoption.add(item["data"]["title"])
            passdic["options"] = passoption
            check += 1
            

            

    if check > 0:
        return passdic
    else:
        return None