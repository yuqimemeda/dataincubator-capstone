#### this part is for the web app 

from os.path import dirname, join
import numpy as np
from bokeh.plotting import Figure,output_file,show,output_server
from bokeh.models import ColumnDataSource, HoverTool, HBox, VBoxForm,BoxSelectTool,LassoSelectTool
from bokeh.models.widgets import Slider, Select, TextInput,Tabs,Panel
from bokeh.models import CustomJS, ColumnDataSource, Slider, Select, TextInput
from bokeh.io import curdoc,vplot
import pandas as pd
import matplotlib.pyplot as plt
from pandas import Series, DataFrame, Panel
import pandas as pd
import datetime
from datetime import time,tzinfo,datetime,timedelta,date
import time
from time import gmtime, strftime,localtime
import collections
import urllib as ul #url.request lib for handling the url
from datetime import datetime, date, time

data_frame=pd.read_csv('new.csv')

stationid = data_frame['start.station.id']
stationaddress = data_frame['start.station.name']
df = DataFrame({'stationid': stationid,'stationstreet': stationaddress} )
df=df.drop_duplicates()
table1=dict(zip(df.stationid, df.stationstreet)) #construct a dictionary mapping station address to stationid

from datetime import datetime
def totalminute(month):#calculate total minutes of different months
    month_30=[4,6,9,11]
    month_31=[1,3,5,7,8,10,12]
    month_28=[2]
    if month in month_30:
        n=43200
    elif month in month_31:
        n=44640
    elif month in month_28:
        n=40320
    return n

def cumm(month,station):# calculate cummulative sum of station net inflow
    month_30=[4,6,9,11]
    month_31=[1,3,5,7,8,10,12]
    month_28=[2]
    if month in month_30:
        n=43200
    elif month in month_31:
        n=44640
    elif month in month_28:
        n=40320
    time_no_seconds=[1,2,3,6]
    data_frame_start_477=data_frame.ix[(data_frame['start.station.id']==station)&(data_frame['month']==month)]
    data_frame_end_477=data_frame.ix[(data_frame['end.station.id']==station)&(data_frame['month']==month)]
#time to min
    if month in time_no_seconds:
        start_time_477=(data_frame_start_477.starttime).astype(str)
        Actual_477=[datetime.strptime(x,"%m/%d/%Y %H:%M") for x in start_time_477]
        end_time_477=(data_frame_end_477.stoptime).astype(str)
        Actual_477_end=[datetime.strptime(x,"%m/%d/%Y %H:%M") for x in end_time_477]
    else:
        start_time_477=(data_frame_start_477.starttime).astype(str)
        Actual_477=[datetime.strptime(x,"%m/%d/%Y %H:%M:%S") for x in start_time_477]
        end_time_477=(data_frame_end_477.stoptime).astype(str)
        Actual_477_end=[datetime.strptime(x,"%m/%d/%Y %H:%M:%S") for x in end_time_477]
    #n=totalminute(month)
    minute=[]
    minute_end=[]
    for i in Actual_477:
        t=1440*(i.day-1)+60*i.hour+i.minute #t=previous x
        minute.append(t)
        num=np.zeros(n,dtype=np.int)
    for i in minute:
        N=minute.count(i)
        num[i]=N

    for i in Actual_477_end:
        t=1440*(i.day-1)+60*i.hour+i.minute
        minute_end.append(t)
        num_end=np.zeros(n,dtype=np.int)
    for i in minute_end:
        N1=minute_end.count(i)
        num_end[i]=N1 
    z=num_end-num
    cumsum=np.cumsum(z)
    return cumsum





TOOLS="pan,wheel_zoom,box_select,lasso_select,box_zoom,hover"#design the tool box
source=ColumnDataSource(data=dict(x=[],y=[]))
plot=Figure(x_axis_type="datetime",plot_width=800,tools=TOOLS,title="station")
plot.line('x','y',source=source,line_width=3,line_alpha=0.6)#construct time series plot 
month= Select(title="month",options=["1","2","3","4","5","6","7","8","9","10","11","12"],value="1")#add selectiont widget
station=TextInput(title="StationID",value='477')#add textinput widget


plot.select_one(HoverTool).tooltips = [
    ("cummulative sum", "@y"),
    ("time","$x"),
]



def update_data(attrname,old,new):#update source data while we input new month and stationID
    startpoint=['1/1/2015','2/1/2015','3/1/2015','4/1/2015','5/1/2015','6/1/2015','7/1/2015','8/1/2015','9/1/2015','10/1/2015','11/1/2015','12/1/2015']
    a=month.value
    b=station.value
    plot.title = table1.get(int(b))#get corresponding station address
    times=pd.date_range(startpoint[int(a)-1], periods=totalminute(int(a)), freq='1min')
    cum=cumm(int(a),int(b))
    source.data = dict(x=times, y=cum)
for w in [month, station]:
    w.on_change('value', update_data)




inputs = VBoxForm(children=[month, station])
curdoc().add_root(HBox(children=[inputs, plot], width=1000))