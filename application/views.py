from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import calendar

from .tasks import email_Job

user_Name = str 
password = str
login_Flag = False

def connect_Sheet():
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',
                 "https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

    creds = ServiceAccountCredentials.from_json_keyfile_name("db.json",scope)
    global client
    client = gspread.authorize(creds)
    #return client

def connect_Sheet_Login():
    connect_Sheet()
    global client 
    sheet_1 = client.open("Event_Database").sheet1
    global user_Name,password
    user_Name = sheet_1.acell('A1').value
    password = sheet_1.acell('B1').value
    print("loaded >> ",user_Name)
    print("loaded >> ",password)

def connect_Sheet_Event_Update():
    connect_Sheet()
    global client
    sheet_2 = client.open("Event_Database").get_worksheet(1)
    #print(sheet_2.get_all_values())
    return sheet_2

def connect_Sheet_Summary_Update():
    connect_Sheet()
    global client
    sheet_3 = client.open("Event_Database").get_worksheet(2)
    return sheet_3

def check_Cred(req):
    print(req.POST['login_Form_Uname'])
    print(req.POST['login_Form_Password'])
   
    if user_Name == req.POST['login_Form_Uname'] and password == req.POST['login_Form_Password']:
        #return render(req,'home.html')
        global login_Flag
        login_Flag = True
        return HttpResponseRedirect('home')
    else:
        return render(req,'Login.html', {'warning':True ,'text':' Wrong Credential'})

def home(req):

    sheet_2 = connect_Sheet_Event_Update()
    data = sheet_2.get_all_values()

    global login_Flag
    if login_Flag:
        login_Flag = False
        data.pop(0)
        return render(req,'home.html',{'valid':True,'events':data})
    else :
        login_Flag = False
        connect_Sheet_Login()
        return render(req,'Login.html', {'warning':True ,'text':' Login is Required'})

# First page 
def login(request):
    connect_Sheet_Login()
    return render(request, 'Login.html',{'param' : 'pradeep'})

def event_Update(req):
    return render(req,'monthly_Event_Form.html',{'text':calendar.month_name[int(datetime.now().month)+1] + " "})

def add_Event(req):
    try:
        event_Data = []
        event_Data.append(req.POST['department'])
        event_Data.append(req.POST['date'])
        event_Data.append(req.POST['start-time'])
        event_Data.append(req.POST['end-time'])
        event_Data.append(req.POST['title'])
        event_Data.append(req.POST['incharge'])
        event_Data.append(req.POST['organizers'])
        month = datetime.now().month
        year = datetime.now().year
        event_Data.append(month)
        event_Data.append(year)
        print(event_Data)

        event_List = connect_Sheet_Event_Update()
        event_List.append_row(event_Data)

        dept = req.POST['department']

        events = []

     
        for i in event_List.get_all_values():
            if i[0] == dept:
                # li = [ i[4], i[1] ] 
                events.append(i)


        return render(req,'event_Update_Message.html',{'events':events,'dept':events[0][0]})
        #,{'text':'Event Updated','data':event_Data}
    except :
        dept = req.POST['department']
        events = []

        event_List = connect_Sheet_Event_Update()
        for i in event_List.get_all_values():
            if i[0] == dept:
                # li = [ i[4], i[1] ] 
                events.append(i)

        if len(events) == 0:
            return render(req,'event_Update_Message.html',{'events':events,'dept':dept})

        return render(req,'event_Update_Message.html',{'events':events,'dept':events[0][0]})        

def event_Summary(req):
        return render(req,'summary_Form.html')

def add_Summary(req):
    summary_Data = []
    summary_Data.append(req.POST['department'])
    summary_Data.append(req.POST['date'])
    summary_Data.append(req.POST['title'])
    summary_Data.append(req.POST['gallery'])
    summary_Data.append(req.POST['summary'])
    
    print(summary_Data)

    sheet_3 = connect_Sheet_Summary_Update()
    sheet_3.append_row(summary_Data)

    return render(req,'summary_Update_Message.html')

def delete_Event(req):
    dept = req.POST['dept']
    title = req.POST['delete_Event']

    print(dept)
    print(title)

    sheet_2 = connect_Sheet_Event_Update()
    data = sheet_2.get_all_values()



    for i in range(len(data)):
        print(data[i])
        if dept == data[i][0] and title == data[i][4]:
            sheet_2.delete_row(i+1)
            break

    events = []
    for j in sheet_2.get_all_values():
        if dept == j[0]:
            events.append(j)

    print(events)

    if len(events) == 0:
        return render(req,'event_Update_Message.html',{'events':events,'dept':dept})


    return render(req,'event_Update_Message.html',{'events':events,'dept':events[0][0]})
    