import requests
from lxml import html
import csv

dump = []

for i in range(0,354):#354):
    print(i)
    response = requests.get("https://www.ifao.egnet.net/bases/cachette/?descr=block+statue&os="+str(i))

    tree = html.fromstring(response.text)

    keys = tree.xpath('//label')
    values = tree.xpath('//div[@class="donnees"]')
    dict = {}
    dict['id']=i
    for _idx,key in enumerate(keys):

        # if _idx > 9:
        #     continue

        # print(_idx)

        _children = key.getchildren()
        if _children == []:
            _this_key = key.text
            # print(key.text)
        else:
            _this_key = _children[1].text
            # print(_children[1].text)

        
        if _this_key == 'Dimensions':    
            _values_children = values[_idx].xpath('.//tr//*[not(*)]')
        elif _this_key in ('Remarks on material','Remarks on datation','Remarks','Related monuments'
                        ,'URL for this page','Documents and archives','Conservation','Porter and Moss II, 2nd ed.','Notes on PM','Date'):  
            continue        
        else:
            _values_children = values[_idx].xpath('.//*[not(*)]')

        if _values_children == []:
            _val = values[_idx].text
            # print(values[_idx].text)
        else:
            if _this_key == 'Dimensions':
                # print(_values_children)
                _dimensions = []
                for i in _values_children[12:]:
                    # print(i.text)
                    _dimensions.append(i.text)
                # print(_dimensions)
                _val = _dimensions

                if _val == []:
                    continue

                dict['height']=_dimensions[0]
                dict['width']=_dimensions[1]
                dict['length']=_dimensions[2]
                dict['depth']=_dimensions[3]
                dict['diameter']=_dimensions[4]
                dict['remarks']=_dimensions[5]
                continue

            elif _this_key == 'Datation':
                _datation = []

                # print(_values_children) 

                _val = ""
                for i in [_values_children[i] for i in range(1,len(_values_children),2)]:
                    # print(i.text)
                    _datation.append(i.text)
                    _val = _val +' '+ i.text
                # print(_datation)
                # _val = _datation
            else:
                # print(_values_children)

                # print(_this_key)

                _val = _values_children[1].text
        
        dict[_this_key]=_val

    # print(dict)
    dump.append(dict)

print(dump)

with open('cachette.csv', 'w', newline='',encoding='utf8') as csvfile:
    fieldnames = ['id','K','Short description','Type 1','Type 2','Material'
        ,'height','width','length','depth','diameter','remarks','Condition','Datation','Remarks on datation', 'Date of discovery (DD/MM/YYYY)','Conservation']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    
    for _stat in dump:
        writer.writerow(_stat)
