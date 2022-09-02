import xmltodict
import sys

def getdata():
    if len(sys.argv)==1: # if no file given, read from stdin
        data = sys.stdin.read()
    else:
        f = open(sys.argv[1], "r")
        data = f.read()
        f.close()
    xml = xmltodict.parse(data, process_namespaces=True)
    csv_string = ''
    csv_string = csv_string + xml['file']['headers'] + '\n'
    data_records = [','.join(list(x.values())) for x in xml['file']['data']['record']]
    for data_record in data_records:
        csv_string = csv_string + data_record + '\n'
    print(csv_string,end = "")

getdata()