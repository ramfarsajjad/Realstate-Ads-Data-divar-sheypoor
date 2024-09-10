from div_secfind import dicfdr
from div_desireitem import deslis

def p_clean_sec(data):
    if bool(dicfdr(data['sections'], "section_name", "IMAGE")):
        des_num1 = deslis(data['sections'], "section_name", "IMAGE")
        dic_key = data['sections'][des_num1]['section_name']
        lis_image = []
        for item in data['sections'][des_num1]['images']:               
            lis_image.append(item['image'].pop('url'))

        data['sections'][des_num1][dic_key] = lis_image
        data['sections'][des_num1].pop('section_name')
        data['sections'][des_num1].pop('images')

    if bool(dicfdr(data['sections'], "section_name", "MAP")):
        des_num1 = deslis(data['sections'], "section_name", "MAP")
        dic_key = data['sections'][des_num1]['section_name']
        data['sections'][des_num1][dic_key] = data['sections'][des_num1].pop('location')
        data['sections'][des_num1].pop('section_name')

    if bool(dicfdr(data['sections'], "section_name", "BUSINESS_SECTION")):
        des_num1 = deslis(data['sections'], "section_name", "BUSINESS_SECTION")
        dic_key = data['sections'][des_num1]['section_name']
        if bool(dicfdr(data['sections'][des_num1]['widgets'], "widget_type", "EVENT_ROW")):
            des_num2 = deslis(data['sections'][des_num1]['widgets'], "widget_type", "EVENT_ROW")
            data['sections'][des_num1]['widgets'][des_num2]['data']['action']['payload'].pop('@type')
            data['sections'][des_num1]['widgets'][des_num2]['data']['action'].update(data['sections'][des_num1]['widgets'][des_num2]['data']['action'].pop('payload'))
            data['sections'][des_num1]['widgets'][des_num2]['data'].update(data['sections'][des_num1]['widgets'][des_num2]['data'].pop('action'))
            data['sections'][des_num1][dic_key] = data['sections'][des_num1]['widgets'][des_num2].pop('data')
            data['sections'][des_num1].pop('widgets', None)
            data['sections'][des_num1].pop('section_name')

    if bool(dicfdr(data['sections'], "section_name", "LIST_DATA")):
        des_num1 = deslis(data['sections'], "section_name", "LIST_DATA")
        dic_key = data['sections'][des_num1]['section_name']
        data['sections'][des_num1][dic_key] = {}
        if bool(dicfdr(data['sections'][des_num1]['widgets'], "widget_type", "GROUP_INFO_ROW")):
            des_num2 = deslis(data['sections'][des_num1]['widgets'], "widget_type", "GROUP_INFO_ROW")           
            data['sections'][des_num1][dic_key]['Property'] = data['sections'][des_num1]['widgets'][des_num2].pop('items')

        if bool(dicfdr(data['sections'][des_num1]['widgets'], "widget_type", "GROUP_FEATURE_ROW")):
            des_num2 = deslis(data['sections'][des_num1]['widgets'], "widget_type", "GROUP_FEATURE_ROW")
            data['sections'][des_num1][dic_key]['benefit'] = []
            if 'possibilty' in data['sections'][des_num1]['widgets'][des_num2]:
                for item in data['sections'][des_num1]['widgets'][des_num2]['possibilty']:
                    if item['widget_type'] == 'UNEXPANDABLE_ROW':
                        data['sections'][des_num1][dic_key]['Property'].append(item.pop('data'))

                    elif item['widget_type'] == 'FEATURE_ROW':
                        data['sections'][des_num1][dic_key]['benefit'].append(item['data'].pop('title'))

        data['sections'][des_num1].pop('widgets')
        data['sections'][des_num1].pop('section_name')
