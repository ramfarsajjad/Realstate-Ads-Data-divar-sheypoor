def deslis (list, key, value):
    
    check = 0
    counter = 0
    for item in list:
        if key in item:
            if item[key] == value:
                check += 1
                break
        counter += 1

    if check == 1:
        return counter
    else:
        return None