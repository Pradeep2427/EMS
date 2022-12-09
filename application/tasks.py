from celery import shared_task
import smtplib,ssl
from importlib_metadata import email
from email.message import EmailMessage
import datetime as dt

# Gspread connection pckg
import gspread
from oauth2client.service_account import ServiceAccountCredentials

mail_Id_Dict = {'MCA' : 'pradeep2000new@gmail.com','MSC DS':'sugusen71@gmail.com','MSC IT':'ps5245@srmist.edu.in'}

mail_Id = list(mail_Id_Dict.values())

# mail_Id = ['pradeep2000new@gmail.com','ps5245@srmist.edu.in','djana381@gmail.com']



def connect_Sheet():
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',
                 "https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

    creds = ServiceAccountCredentials.from_json_keyfile_name("db.json",scope)
    client = gspread.authorize(creds)
    return client

def get_Completed_Events():
    client = connect_Sheet()
    data = client.open("Event_Database").get_worksheet(1).get_all_values()

    # Removing the column names from the data - Event sheet
    data.pop(0)

    date = dt.datetime.now().day
    date = date -1

    completed_Data = []
    for i in data:
        event_Date = int(i[1])

        if date == event_Date:
            completed_Data.append(i)

    return completed_Data


@shared_task
def email_Job():

    # password = oopzqgtkkbuyxvea
    # <a href="http://127.0.0.1:8000/Event-Update"> Event Update </a><br>
    

    if dt.datetime.now().day == 2:

        email_Addr = 'spradeep2410@gmail.com'
        email_Pass = 'oopzqgtkkbuyxvea'

        msg = EmailMessage()
        msg['From'] = 'spradeep2410@gmail.com'
        msg['To'] = ", ".join(mail_Id) 
        msg['Subject'] = 'Monthly Event Update'
        msg.add_alternative("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <style>
                div {               
                    background: linear-gradient(to right, #d04ed6, #834d9b);
                    text-align: center;
                    padding-left : 20px;
                    padding-right : 20px;
                    padding-bottom: 10px;
                    font-family: cursive;
                    color: white;
                }
            </style>
        </head>
        <body>
            <div>
                <h1 style="padding-top: 20px; color: white;">Dear Head Of the Department,</h1>
                <hr style="border-top : 1px white;">
                <h3> Remainder Mail for updating Events for next month. <br> Kindly follow the link to update the events.
                <br>
                <a href="http://127.0.0.1:8000/Event-Update"> Event Update </a><br>
                Thank you!<br>
                Regards Team</h3>
            </div>
        </body>
        </html>
        """,subtype='html')
        smtp = smtplib.SMTP_SSL('smtp.gmail.com',465)
        smtp.login(email_Addr,email_Pass)
        smtp.send_message(msg)

    # Code to send mail after event getting over

    yesterday_Events = get_Completed_Events()
    print(yesterday_Events)

    if len(yesterday_Events) > 0:

        email_Addr = 'spradeep2410@gmail.com'
        email_Pass = 'oopzqgtkkbuyxvea'

        for i in yesterday_Events:
        
            msg = EmailMessage()
            msg['From'] = 'spradeep2410@gmail.com'
            msg['To'] = mail_Id_Dict[i[0]]
            msg['Subject'] = 'Event Completion Summary -' + i[4]
            msg.add_alternative("""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <style>
                    div {               
                        background: linear-gradient(to right, #d04ed6, #834d9b);
                        text-align: center;
                        padding-left : 20px;
                        padding-right : 20px;
                        padding-bottom: 10px;
                        font-family: cursive;
                        color: white;
                    }
                </style>
            </head>
            <body>
                <div>
                    <h1 style="padding-top: 20px; color: white;">Dear, Head Of the Department,</h1>
                    <hr style="border-top : 1px white;">
                    <h3> Hope you have completed the """ + i[4] + """ Event Sucessfully.<br>
                    Kindly update the event summary for the event by following the below link.
                    <br>
                    <a href="http://127.0.0.1:8000/event-summary"> Add Summary </a><br>
                    <br>
                    Thank you!<br>
                    Regards Team</h3>
                </div>
            </body>
            </html>
            """,subtype='html')
            smtp = smtplib.SMTP_SSL('smtp.gmail.com',465)
            smtp.login(email_Addr,email_Pass)
            smtp.send_message(msg)

