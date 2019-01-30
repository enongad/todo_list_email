#import csv
import pandas as pd
import numpy as np
import smtplib as smt
from email.message import EmailMessage
import datetime
#from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from tabulate import tabulate

##  set up email params
SMTP_Address = "server@host.com"
sender_address = 'daily.reminders@host.com'
sendee_address = 'whoever@host.com'

## create todays date
today = datetime.date.today().strftime("%B %d, %Y")
today_ugly = datetime.date.today().strftime("%Y-%m-%d")

### import xlsx
df = pd.read_excel('tasks.xlsx',"tasks")
df = df[df.completed == "no"]
df = df.drop('completed',1)

### format date variable
df['due_date'] = pd.to_datetime(df['due_date'])
df### remove Nans and replace is white space
df = df.replace(np.nan, '', regex=True)
df['due_date'] = pd.to_datetime(df['due_date'])

## get list of things due today
due_today = df[df.due_date == today_ugly]
df = df[df.due_date != today_ugly]

## split taskes my priority
high = df.loc[df['priority'] == 'high']
med = df.loc[df['priority'] == 'med']
low = df.loc[df['priority'] == 'low']

### remove priority columns
high = high.drop('priority',1)
med = med.drop('priority',1)
low = low.drop('priority',1)

## create string that will be body of the email
text = """DUE TODAY
{due_today}



HIGH PRIORITY
{high}



MEDIUM PRIORITY
{med}



LOW PRIORITY
{low}

"""

## headers of table
headers = ["Project", "Task", "Due Date", "Notes", "Done", "Left"]

## format of table
fmt = "presto"

text = text.format(due_today= tabulate(due_today, headers, tablefmt=fmt,showindex="never"),
                   high=tabulate(high, headers, tablefmt=fmt,showindex="never"),
                   med=tabulate(med, headers, tablefmt=fmt,showindex="never"),
                   low=tabulate(low, headers, tablefmt=fmt,showindex="never"))

## email set up
sender = sender_address
to = sendee_address
msg = MIMEText(text)
msg['From'] = sender
msg['To'] = to
msg['Subject'] = "Task list for "+today

### send email
s = smt.SMTP(SMTP_Address)
s.sendmail(sender, to, msg.as_string())
s.quit()
