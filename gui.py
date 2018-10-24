from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.actionbar import ActionBar,ActionView,ActionButton,ActionDropDown
import os
import fdb
import datetime
import sys
from xlsxwriter.workbook import Workbook
# import matplotlib
# matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')
import numpy as np
import time
# import first


class Main(App):

    def __init__(self):
        App.__init__(self)
        self.range = {}
        self.range['start'] = {'year':2000,'month':'January','date':'1','minute':0,'hour':'0','second':'0'}
        self.range['end'] = {'year':2017,'month':'July','date':'4','minute':0,'hour':'0','second':'1'}
        self.sensors = "3b9b0c6d-ea3c-4bdb-bbec-9a3414bd8c19"

    def build(self):
        #Set Window Size
        Window.size = (600, 300)

        layout = BoxLayout(orientation='vertical', padding=(10,10,10,10), spacing=5)
        sub_layout_start = BoxLayout(orientation='horizontal')
        sub_layout_end = BoxLayout(orientation='horizontal')
        layout.bind(on_size=lambda x:self.reposition_layouts(0,layout,sub_layout_start))
        layout.bind(on_size=lambda x:self.reposition_layouts(1,layout,sub_layout_start))

        self.months = ["January","February","March","April","May","June","July","August","September","October","November","December"]

        #Action bar
        # actionbar = ActionBar()
        # action_btn = ActionButton
        # action_dropdown = ActionDropDown

        #TODO: Remove Hack
        empty_label = Label(text='',size_hint=(1.0,0.08))
        #Labels
        start_label = Label(text="Select Starting Date", size_hint=(1.0, 0.20))
        #label_start_layout = AnchorLayout(anchor_x='right',anchor_y='center',size_hint=(1.0,0.08))
        #label_start_layout.add_widget(start_label)

        end_label = Label(text="Select Ending Date", size_hint=(1.0, 0.20))
        #label_end_layout = AnchorLayout(anchor_x='right',anchor_y='center',size_hint=(1.0,0.08))
        #label_end_layout.add_widget(end_label)

        #Dropdown for year
        year_start_dropdown = DropDown()
        main_year_start_btn = Button(text='Select Year')
        self.dropSize = main_year_start_btn.size[0]
        for i in range (2000,2018):
            btn = Button(text=str(i),size_hint=(main_year_start_btn.size[0],None),height=44)
            btn.bind(on_release=lambda btn: year_start_dropdown.select(btn.text))
            year_start_dropdown.add_widget(btn)
        main_year_start_btn.bind(on_release=year_start_dropdown.open)
        year_start_dropdown.bind(on_select=lambda instance, x: self.addToMap(main_year_start_btn,'start','year',x))

        year_end_dropdown = DropDown()
        for i in range (2000,2018):
            btn = Button(text=str(i),size_hint=(main_year_start_btn.size[0],None),height=44)
            btn.bind(on_release=lambda btn: year_end_dropdown.select(btn.text))
            year_end_dropdown.add_widget(btn)
        main_year_end_btn = Button(text='Select Year')
        main_year_end_btn.bind(on_release=year_end_dropdown.open)
        year_end_dropdown.bind(on_select=lambda instance, x: self.addToMap(main_year_end_btn,'end','year',x))

        #Date Selector
        date_start_dropdown = DropDown()
        main_date_start_btn = Button(text="Select Date")
        main_date_start_btn.bind(on_release=date_start_dropdown.open)
        date_start_dropdown.bind(on_select=lambda instance, x: self.addToMap(main_date_start_btn,'start','date',x))

        date_end_dropdown = DropDown()
        main_date_end_btn = Button(text="Select Date")
        main_date_end_btn.bind(on_release=date_end_dropdown.open)
        date_end_dropdown.bind(on_select=lambda instance, x: self.addToMap(main_date_end_btn,'end','date',x))

        #Dropdown for month
        month_start_dropdown = DropDown()
        for i in self.months:
            btn = Button(text=str(i),size_hint=(main_year_start_btn.size[0],None),height=44)
            btn.bind(on_release=lambda btn: self.month_selector_callback(0,btn.text,date_start_dropdown,month_start_dropdown))
            month_start_dropdown.add_widget(btn),
        main_month_start_btn = Button(text='Select Month')
        main_month_start_btn.bind(on_release=month_start_dropdown.open)
        month_start_dropdown.bind(on_select=lambda instance, x: self.addToMap(main_month_start_btn,'start','month',x))

        month_end_dropdown = DropDown()
        for i in self.months:
            btn = Button(text=str(i),size_hint=(main_year_start_btn.size[0],None),height=44)
            btn.bind(on_release=lambda btn: self.month_selector_callback(1,btn.text,date_end_dropdown,month_end_dropdown))
            month_end_dropdown.add_widget(btn)
        main_month_end_btn = Button(text='Select Month')
        main_month_end_btn.bind(on_release=month_end_dropdown.open)
        month_end_dropdown.bind(on_select=lambda instance, x: self.addToMap(main_month_end_btn,'end','month',x))

        #Hour selector
        hour_start_dropdown = DropDown()
        for i in range(0,24):
            btn = Button(text=str(i),size_hint=(main_year_start_btn.size[0],None),height=44)
            btn.bind(on_release=lambda btn: hour_start_dropdown.select(btn.text))
            hour_start_dropdown.add_widget(btn)
        main_hour_start_btn = Button(text='Select Hour')
        main_hour_start_btn.bind(on_release=hour_start_dropdown.open)
        hour_start_dropdown.bind(on_select=lambda instance, x: self.addToMap(main_hour_start_btn,'start','hour',x))

        hour_end_dropdown = DropDown()
        for i in range(0,24):
            btn = Button(text=str(i),size_hint=(main_year_start_btn.size[0],None),height=44)
            btn.bind(on_release=lambda btn: hour_end_dropdown.select(btn.text))
            hour_end_dropdown.add_widget(btn)
        main_hour_end_btn = Button(text='Select Hour')
        main_hour_end_btn.bind(on_release=hour_end_dropdown.open)
        hour_end_dropdown.bind(on_select=lambda instance, x: self.addToMap(main_hour_end_btn,'end','hour',x))

        #Minute selector
        minute_start_dropdown = DropDown()
        for i in range(0,60):
            btn = Button(text=str(i),size_hint=(main_year_start_btn.size[0],None),height=44)
            btn.bind(on_release=lambda btn: minute_start_dropdown.select(btn.text))
            minute_start_dropdown.add_widget(btn)
        main_minute_start_btn = Button(text='Select Minute')
        main_minute_start_btn.bind(on_release=minute_start_dropdown.open)
        minute_start_dropdown.bind(on_select=lambda instance, x: self.addToMap(main_minute_start_btn,'start','minute',x))

        minute_end_dropdown = DropDown()
        for i in range(0,60):
            btn = Button(text=str(i),size_hint=(main_year_start_btn.size[0],None),height=44)
            btn.bind(on_release=lambda btn: minute_end_dropdown.select(btn.text))
            minute_end_dropdown.add_widget(btn)
        main_minute_end_btn = Button(text='Select Minute')
        main_minute_end_btn.bind(on_release=minute_end_dropdown.open)
        minute_end_dropdown.bind(on_select=lambda instance, x: self.addToMap(main_minute_end_btn,'end','minute',x))

        #Second selector
        second_start_dropdown = DropDown()
        for i in range(0,60):
            btn = Button(text=str(i),size_hint=(main_year_start_btn.size[0],None),height=44)
            btn.bind(on_release=lambda btn: second_start_dropdown.select(btn.text))
            second_start_dropdown.add_widget(btn)
        main_second_start_btn = Button(text='Select Second')
        main_second_start_btn.bind(on_release=second_start_dropdown.open)
        second_start_dropdown.bind(on_select=lambda instance, x: self.addToMap(main_second_start_btn,'start','second',x))

        second_end_dropdown = DropDown()
        for i in range(0,60):
            btn = Button(text=str(i),size_hint=(main_year_start_btn.size[0],None),height=44)
            btn.bind(on_release=lambda btn: second_end_dropdown.select(btn.text))
            second_end_dropdown.add_widget(btn)
        main_second_end_btn = Button(text='Select Second')
        main_second_end_btn.bind(on_release=second_end_dropdown.open)
        second_end_dropdown.bind(on_select=lambda instance, x: self.addToMap(main_second_end_btn,'end','second',x))

        #Text Input
        uuid_input = TextInput(text="Enter Uuids here seperated by a space")
        uuid_label = Label(text="Sensor Id",size_hint=(1.0,0.20))
        uuid_input.bind(text=lambda instance,x: self.setSensors(x))        

        #Sensors
        # sensor_label = Label(text="Choose Sensors",size_hint=(1.0,0.20))
        # temperature = ToggleButton(text="Temperature",group="temp",state='down')
        # temperature.bind(on_release=lambda x: self.addToSensorList('temperature',temperature.state))
        # pressure = ToggleButton(text="Pressure",group="press",state='down')
        # pressure.bind(on_release=lambda x: self.addToSensorList('pressure',pressure.state))
        # flow = ToggleButton(text="Flow",group="flow",state='down')
        # flow.bind(on_release=lambda x: self.addToSensorList('flow',flow.state))
        # volume = ToggleButton(text="Volume",group="vol",state='down')
        # volume.bind(on_release=lambda x: self.addToSensorList('volume',volume.state))
        # sensors_layout = BoxLayout(orientation='horizontal')
        # sensors_layout.add_widget(temperature)
        # sensors_layout.add_widget(pressure)
        # sensors_layout.add_widget(flow)
        # sensors_layout.add_widget(volume)

        #Submit Button
        submit_layout = AnchorLayout(anchor_x='center',anchor_y='center', size_hint=(1, 0.5))
        submit_button = Button(text="Submit", size_hint=(0.5, 1))
        submit_button.bind(on_release=self.submit)
        submit_layout.add_widget(submit_button)

        #Adding Start Widgets
        sub_layout_start.add_widget(main_year_start_btn)
        sub_layout_start.add_widget(main_month_start_btn)
        sub_layout_start.add_widget(main_date_start_btn)
        sub_layout_start.add_widget(main_hour_start_btn)
        sub_layout_start.add_widget(main_minute_start_btn)
        sub_layout_start.add_widget(main_second_start_btn)

        #Adding End widgets
        sub_layout_end.add_widget(main_year_end_btn)
        sub_layout_end.add_widget(main_month_end_btn)
        sub_layout_end.add_widget(main_date_end_btn)
        sub_layout_end.add_widget(main_hour_end_btn)
        sub_layout_end.add_widget(main_minute_end_btn)
        sub_layout_end.add_widget(main_second_end_btn)

        #Add to main layout
        layout.add_widget(start_label)
        layout.add_widget(sub_layout_start)
        layout.add_widget(end_label)
        layout.add_widget(sub_layout_end)
        layout.add_widget(uuid_label)
        layout.add_widget(uuid_input)
        # layout.add_widget(sensor_label)
        # layout.add_widget(sensors_layout)
        layout.add_widget(submit_layout)
        return layout

    def month_selector_callback(self,identifier,txt,date_dropdown,month_dropdown):
        if(txt in ["January","March","May","July","August","October","December"]):
            date_dropdown.clear_widgets()
            for i in range(1,32):
                btn = Button(text=str(i),size_hint=(self.dropSize,None),height=44)
                btn.bind(on_release=lambda btn: date_dropdown.select(btn.text))
                if(identifier is 0):
                    date_dropdown.add_widget(btn)
                else:
                    date_dropdown.add_widget(btn)

        elif(txt is "February"):
            date_dropdown.clear_widgets()
            for i in range(1,29):
                btn = Button(text=str(i),size_hint=(self.dropSize,None),height=44)
                btn.bind(on_release=lambda btn: date_dropdown.select(btn.text))
                if(identifier is 0):
                    date_dropdown.add_widget(btn)
                else:
                    date_dropdown.add_widget(btn)

        elif(txt in ["April","June","September","November"]):
            date_dropdown.clear_widgets()
            for i in range(1,31):
                btn = Button(text=str(i),size_hint=(self.dropSize,None),height=44)
                btn.bind(on_release=lambda btn: date_dropdown.select(btn.text))
                if(identifier is 0):
                    date_dropdown.add_widget(btn)
                else:
                    date_dropdown.add_widget(btn)
        month_dropdown.select(txt)

    def reposition_layouts(identifier,root,layout):
        layout.pos = root.x, root.height / 2 - layout.height / 2

    def addToMap(self,btn,identifier,key,value):
        setattr(btn, 'text', str(value))
        self.range[identifier][key] = value

    def addToSensorList(self,key,value):
        if(value is "down"):
            self.sensors[key] = 1
        else:
            self.sensors[key] = 0

    def submit(self,x):
        print(self.range.keys())
        print(self.range['start'].keys())
        print(self.range['end'].keys())
        print(self.range['start'].values())
        print(self.range['end'].values())
        print(self.sensors)
        self.range['start']['month'] = self.months.index(self.range['start']['month'])+1
        self.range['end']['month'] = self.months.index(self.range['end']['month'])+1
        for i in self.range['start'].keys():
            self.range['start'][i] = int(self.range['start'][i])
            self.range['end'][i] = int(self.range['end'][i])
        start_date = datetime.datetime(self.range['start']['year'],self.range['start']['month'],self.range['start']['date'],self.range['start']['hour'],self.range['start']['minute'],self.range['start']['second'])
        end_date = datetime.datetime(self.range['end']['year'],self.range['end']['month'],self.range['end']['date'],self.range['end']['hour'],self.range['end']['minute'],self.range['end']['second'])
        start_date = self.unix_time_millis(start_date)
        end_date = self.unix_time_millis(end_date)
        print(end_date)
        self.func(start_date,end_date,self.sensors)
        self.range['start'] = {'year':2000,'month':'January','date':'1','hour':'0','minute':0,'second':'0'}
        self.range['end'] = {'year':2017,'month':'July','date':'3','hour':'0','minute':0,'second':'1'}
        # self.sensors = ""

    def setSensors(self,text):
    	self.sensors = text

    def unix_time_millis(self,dt):
        epoch = datetime.datetime.utcfromtimestamp(0)
        return (dt - epoch).total_seconds() * 1000.0

    def func(self,start_time,end_time,uuids):
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
        con = fdb.connect(dsn='G:\Report_builder_Adani\Report_builder_Adani\TEST.fdb', user='sysdba', password='masterkey')
        cursor = con.cursor()
        query="SELECT * FROM sensors WHERE xtime BETWEEN " + str(int(float(start_time))) + " AND " + str(int(float(end_time))) + " AND " + "uuid IN " + str_uuids
        print(query)
        c=time.clock()
        cursor.execute(query)
        print("The time taken to fetch the data was - " + str(time.clock()-c))
        workbook = Workbook('outfile4.xlsx')
        sheet = workbook.add_worksheet()
        data = cursor.fetchall()
        global x
        global y
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
        self.xgraph(data,graph_heads,sheet)
        workbook.close()
        # matplotlib.pyplot.show()

    def xgraph(self,data,graph_heads,sheet):
        import matplotlib.pyplot as plt
        r=1;
        l=len(graph_heads)
        row = 1
        def graph(x_axis,y_axis,subplot_no,l):
            plt.subplot(l,1,subplot_no)
            plt.plot(x_axis,y_axis)
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
        plt.show()


if __name__ == '__main__':
    Main().run()
