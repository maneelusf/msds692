import mycsv
import sys

def getdata():
    header, data = mycsv.readcsv(mycsv.getdata())
    header_string = ''.join(['<th>{}</th>'.format(x) for x in header])
    header_string = '<tr>{}</tr>'.format(header_string)
    data_strings = ''
    for data_line in data:
        data_string = ''.join(['<td>{}</td>'.format(x) for x in data_line])
        data_string = '<tr>{}</tr>\n'.format(data_string)
        data_strings = data_strings + data_string
    string  = "<html>\n<body>\n<table>\n{}\n{}</table>\n</body>\n</html>".format(header_string,data_strings)
    print(string)

getdata()


