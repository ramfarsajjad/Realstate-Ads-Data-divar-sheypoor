
def listd_p(data, real_state):
    if 'Property' in data:
        for item in data['Property']:
            if item['title'] == "متراژ":
                real_state['meterage'] = int(item['value'])
            elif item['title'] == "ساخت":
                if (item['value'].split())[0] == 'قبل':
                    real_state['build_date'] = 1370
                else:
                    real_state['build_date'] = int(item['value'])
            elif item['title'] == "اتاق":
                if (item['value'].split())[0] == 'بدون':
                    real_state['room'] = 0
                else:
                    real_state['room'] = int(item['value'])                
            elif item['title'] == "تعداد واحد در طبقه":
                real_state['unitpf'] = int(item['value'])
            elif item['title'] == "سند":
                real_state['sanad'] = item['value']
            elif item['title'] == "جهت ساختمان":
                real_state['jahat'] = item['value']
            elif item['title'] == "وضعیت واحد":
                real_state['vaziat'] = item['value']
            elif item['title'] == "تعداد کل طبقات ساختمان":
                real_state['tabaghe'] = item['value']
            

    if 'benefit' in data:
        for item in data['benefit']:
            words = item.split()
            if  words[0] == "بالکن":
                if len(words) > 1:
                    real_state['balkon'] = " ".join(words[1:])
                else:
                    real_state['balkon'] = "دارد"
                continue
            elif  words[0] == "پارکینگ":
                if len(words) > 1:
                    real_state['parking'] = " ".join(words[1:])
                else:
                    real_state['parking'] = "دارد"                
                continue
            elif  words[0] == "انباری":
                if len(words) > 1:
                    real_state['storage'] = " ".join(words[1:])
                else:
                    real_state['storage'] = "دارد"                
                continue
            elif  words[0] == "آسانسور":
                if len(words) > 1:
                    real_state['elevator'] = " ".join(words[1:])
                else:
                    real_state['elevator'] = "دارد"                
                continue
            elif words[0] == "سرویس":
                real_state["wc"] = " ".join(words[2:])
                continue
            elif words[0] == "جنس":
                real_state["jenskaff"] = " ".join(words[2:])
                continue
            elif words[0] == "سرمایش":
                real_state["cooler"] = " ".join(words[1:])
                continue
            elif words[0] == "گرمایش":
                real_state["heater"] = " ".join(words[1:])
                continue
            elif words[0] == "تأمین\u200cکننده":
                real_state["tamin_hot_water"] = " ".join(words[3:])

    return real_state


