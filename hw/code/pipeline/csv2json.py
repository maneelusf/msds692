import mycsv

def getdata():
    header, data = mycsv.readcsv(mycsv.getdata())
    header_string = '{' + '"headers":[{}],'.format(','.join(['"{}"'.format(x) for x in header]))
    data_strings = []
    for data_value in range(len(data)):
        data_string = ','.join(['"{}":"{}"'.format(header[number],data[data_value][number])
                                for number in range(len(data[data_value]))])
        data_string = '{' + data_string + '}'
        data_strings.append(data_string)
    data_strings = '"data":[' + ','.join(data_strings) + ']}'
    total_string = header_string + data_strings
    print(total_string)

    # print(json.dumps(dict1,indent = 1))
#
#
# def getdata():
#     header, data = mycsv.readcsv(mycsv.getdata())
#     print(header)
#     print(data)
#     header_string = '{' + '"headers": {}'.format(header)
#     print(header_string)
#     # x = '''''''{"headers": {},"data":[{"when":"2016-08-12", "a":"1.2", "b":"3"},
#     # {"when":"2016-08-13", "a":"3.99003", "b":"4.3"}]}
getdata()