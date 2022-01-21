import datetime
import methods

dT = datetime.datetime.now()

def current_date(format="Y-M-D 00:00:00"):
    if format == "D M,Y":
        return dT.strftime("%d %B, %Y")
    else:
        return dT

def get_currentdiff(date):
    date = datetime.datetime.strptime(date, '%d %B, %Y')
    #date = date.days
    return int((dT-date).days)
    
def sync_time(date):
    first = datetime.datetime.strptime(date, '%d %B, %Y')  # converts date from 29 October, 2021 to 2021-10-29 00:00:00
    last = methods.get_last_access_date()
    last = datetime.datetime.strptime(last, '%d %B, %Y')
    val = dT - last
    val = val.days
    if val > 1:             #If program has not been run in more than one day    
        methods.fillin(val)
    else:                         #Regularly opened
        z = dT - first 
        z = z.days + 1            #int days, +1 to accomodate inclusivity for the date  
        methods.update_single("true", z)    #updates the true days since initial date
        methods.update_followed()           #updates the followed days since initial date
        
def _checkin_proof(date):   #matches current date with last check in
    current = dT.strftime("%d %B, %Y")
    if date == current:
        return True, current
    return False, current

def return_day(date):                               #Given date in format: 29 October, 2021, returns day of the week
    date_time_obj = datetime.datetime.strptime(date, '%d %B, %Y')
    return date_time_obj.strftime('%A')