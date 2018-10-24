import fdb
import datetime
import sys
from xlsxwriter.workbook import Workbook
import matplotlib.pyplot as plt
import numpy as np

def func(start_time,end_time,uuids):
    graph_heads = uuids
    graph_heads = graph_heads.split()
    uuids=uuids.split()
    str_uuids="("
    for uuid in uuids:
        str_uuids+="'"+uuid+"'"
        str_uuids+=","
    if str_uuids.endswith(","):
        str_uuids = str_uuids[:-1]
    str_uuids+=")"
    print(str_uuids)
    con = fdb.connect(dsn='C:\Python Stuff\Database\MOCK.fdb', user='sysdba', password='masterkey')
    cursor = con.cursor()
    query="SELECT * FROM sensors WHERE xtime BETWEEN " + str(int(float(start_time))) + " AND " + str(int(float(end_time))) + " AND " + "uuid IN " + str_uuids
    print(query)
    cursor.execute(query)
    workbook = Workbook('outfile1.xlsx')
    sheet = workbook.add_worksheet()
    data = cursor.fetchall()
    x = {}
    y = {}
    for head in graph_heads:
        x[head] = []
        y[head] = []
    print(len(data))
    print(np.asarray(data).shape)
    for r, row in enumerate(data):
        x[row[0]].append(row[2])
        y[row[0]].append(float(row[3]))
        sheet.write(r, 0, row[0])
        sheet.write(r, 1, row[1])
        sheet.write(r, 2, datetime.datetime.fromtimestamp(row[2]/1000).strftime('%Y-%m-%d %H:%M:%S'))
        sheet.write(r, 3, row[3])
    r=1;
    l=len(graph_heads)
    row = 1
    for i,head in enumerate(graph_heads):
        sheet.write(len(data)+row,0,head)
        sheet.write(len(data)+row,1,"Minimum")
        sheet.write(len(data)+row,2,np.array(y[head]).min())
        row+=1
        sheet.write(len(data)+row,0,head)
        sheet.write(len(data)+row,1,"Maximum")
        sheet.write(len(data)+row,2,np.array(y[head]).max())
        row+=1
        sheet.write(len(data)+row,0,head)
        sheet.write(len(data)+row,1,"Average")
        sheet.write(len(data)+row,2,np.array(y[head]).mean())
        row+=1
        sheet.write(len(data)+row,0,head)
        sheet.write(len(data)+row,1,"Standard deviation")
        sheet.write(len(data)+row,2,np.array(y[head]).std())
        row+=1
        sheet.write(len(data)+row,0,head)
        sheet.write(len(data)+row,1,"Variance")
        sheet.write(len(data)+row,2,np.array(y[head]).var())
        row+=2
        graph(x[head],y[head],r,l)
        r+=1
    workbook.close()
    plt.show()


def graph(x_axis,y_axis,subplot_no,l):
    plt.subplot(l,1,subplot_no)
    plt.plot(x_axis,y_axis)

