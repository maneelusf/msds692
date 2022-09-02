import mycsv

def getdata():
    header, data = mycsv.readcsv(mycsv.getdata())
    header_string = '  <headers>{}</headers>'.format(','.join(header))
    header = [x.replace(' ','_') for x in header]
    data_strings = ''
    for data_number in range(0,len(data)):
        data_string = ['<{}>{}</{}>'.format(header[ds],dy,header[ds]) for ds,dy in enumerate(data[data_number])]
        data_string = ''.join(data_string)
        data_string = '    <record>\n      {}\n    </record>'.format(data_string)
        data_strings = data_strings + data_string + '\n'


    string = '<?xml version="1.0"?>\n<file>\n{}\n  <data>\n{}  </data>\n</file>'.format(header_string,data_strings)
    print(string,end ="")

getdata()

#
# <?xml version="1.0"?>
# <file>
#   <headers>when,a,b</headers>
#   <data>
#     <record>
#       <when>2016-08-12</when><a>1.2</a><b>3.0</b>
#     </record>
#     <record>
#       <when>2016-08-13</when><a>3.99003</a><b>4.3</b>
#     </record>
#   </data>
# </file>