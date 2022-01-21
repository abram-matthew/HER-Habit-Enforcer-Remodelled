import chronos
import iohandle
from collections import Counter

consecutive = False         #Ensures multiple operations before a file is written

#Pre-Fetches Stored Data to avoid delays
PATH = "Files\_json_files\data.json"
js_obj = iohandle.get_content(PATH) if iohandle.check_exists(PATH) else 0   ###UNRESOLVED ISSUES

#Get parameters
def get_pilot():
    return str(js_obj["pilot"])
def get_head():
    return str(js_obj["head"])
def get_true():
    return str(js_obj["true"])
def get_followed():
    return str(js_obj["followed"])
def get_fails():
    return str(js_obj["fails"])
def get_success():
    return str(js_obj["success"])
def get_deviation():
    return str(js_obj["deviation"])
def get_log():
    log = js_obj["log"]
    dates = [str(log[i].get("dated")) for i in range(len(log))]
    days = [str(log[i].get("day")) for i in range(len(log))]
    values = [str(log[i].get("value")) for i in range(len(log))]
    return dates, days, values
def get_points():
    return js_obj["plot_points"]
def get_last_access_date():
    return js_obj["last_accessed"]
def get_lasttrip():
    dates,_,_ = get_log()
    return None if len(dates) == 0 else dates[-1]
def get_downtime():
    return js_obj["downtime"]
def get_streak():
    return js_obj["streak"]
def get_habitname():
    return js_obj["habitname"]

#Update parameters

def update_single(key, value):
    js_obj[key] = value
    if not consecutive:
        iohandle.dump_content(PATH,js_obj)

def update_followed():
    js_obj["followed"] = js_obj["true"] - js_obj["fails"] 
    if not consecutive: 
        iohandle.dump_content(PATH,js_obj)

def update_success():
    js_obj["success"] = round((js_obj["followed"]/js_obj["true"])*100, 2)
    if not consecutive:
        iohandle.dump_content(PATH,js_obj)
    return js_obj["success"]

def update_fails():                          
    js_obj["fails"] += 1 
    if not consecutive:
        iohandle.dump_content(PATH,js_obj)

def update_log(date,value=1):
    consecutive = True
    js_obj["log"].append({"dated": date, 
                           "day": chronos.return_day(date),
                           "value": value})
    update_followed()
    update_success()
    update_downtime(90)
    update_streak(False)
    js_obj["plot_points"][-1] = float(get_success())
    consecutive = False
    if not consecutive:
        iohandle.dump_content(PATH,js_obj)

def update_points():
    js_obj["plot_points"].append(js_obj["success"])
    if not consecutive:
        iohandle.dump_content(PATH,js_obj)

def update_downtime(target):
    tru = int(get_true())+1
    fol = int(get_followed())
    relative_success = (fol/tru)*100
    update_downtime.down = 0
    if relative_success < target: 
        idx = 0
        while idx <=target:
            idx = fol/tru*100
            fol+=1; tru+=1
        update_downtime.down = (tru-1) - int(get_true())

    js_obj["downtime"] = update_downtime.down
    if not consecutive:
        iohandle.dump_content(PATH,js_obj)

def update_streak(isTrue = True):
    if isTrue:
        if js_obj["streak"] < 5:
            js_obj["streak"] += 1
            if not consecutive:
                iohandle.dump_content(PATH,js_obj)
    else:
        js_obj["streak"] = 0
        if not consecutive:
                iohandle.dump_content(PATH,js_obj)

def update_habitname(newname):
    js_obj["habitname"] = newname
    if not consecutive:
        iohandle.dump_content(PATH,js_obj)

#Miscellaneus 
 
def checkin():
    flag, current = chronos._checkin_proof(str(js_obj["last_accessed"]))
    if not(flag):
       js_obj["last_accessed"] = current           #Adds current date 
       ###Update Streak###
       current_streak = int(get_streak())
       since = since_lasttrip()       
       if since != 0:
        for idx in range(4): 
            start = ((idx+1)*7)
            term = ((idx+1)*7)+7
            if since in range(start,term) and current_streak != idx+1:
                update_streak()
        if since >= 35:
            update_streak()
       #======================================#
       if not consecutive:
          update_points()
          iohandle.dump_content(PATH,js_obj)
        
def fillin(value):
    global consecutive 
    consecutive = True
    current_days = get_true()
    for _ in range(value):
          update_single("true", int(current_days)+1)
          update_followed()
          update_success()
          update_points()
          current_days = int(current_days)+1
    checkin()
    consecutive = False
    iohandle.dump_content(PATH,js_obj)

def generate_per_pi():
    _, days, _ = get_log()
    count = Counter(days)
    val = list(count.values()) 
    key = list(count.keys())
    data = {"Monday": 0,
            "Tuesday": 0,
            "Wednesday": 0,
            "Thursday": 0,
            "Friday": 0,
            "Saturday": 0,
            "Sunday": 0,
    }
    for idx in range(len(count)):
        data[key[idx]]=(val[idx]/int(get_fails()))*100
    return data

def since_lasttrip():
    trip = get_lasttrip()
    if trip == None:
        return int(get_true()) 
    else:
        since = chronos.get_currentdiff(trip)
        return since

def gen_goal():
    down = get_downtime()
    return down if down!=0 else 7

def trips_per_month():
    dates,_,_ = get_log()
    relative_sample = chronos.current_date("D M,Y")[3:]
    freq = 0
    for idx in range(len(dates)):
        if dates[idx][3:] == relative_sample:
            freq+=1
    return freq

###FIRST RUN PREP
def rereadfile(PATH):
    global js_obj
    js_obj = iohandle.get_content(PATH) 
    
def notnew_user():
    return iohandle.check_exists(PATH)

def prepare_new_profile(fails=0):
    iohandle.create_file(PATH)
    success = 100 if fails == 0 else 0
    data = {
            "pilot": "", 
            "habitname": "Default Habit",
            "head": str(chronos.current_date("D M,Y")), 
            "true": 1, 
            "followed": 1-fails, 
            "fails": 0, 
            "success": success,
            "deviation": 0, 
            "log": [],
            "plot_points": [success],
            "downtime": 0, 
            "streak": 0,
            "last_accessed": str(chronos.current_date("D M,Y")),
    }
    iohandle.dump_content(PATH, data)
    rereadfile(PATH)

def reset(fails = 0):
    success = 100 if fails == 0 else 0
    data = {
            "pilot": "", 
            "habitname": "Default Habit",
            "head": str(chronos.current_date("D M,Y")), 
            "true": 1, 
            "followed": 1-fails, 
            "fails": 0, 
            "success": success,
            "deviation": 0, 
            "log": [],
            "plot_points": [success],
            "downtime": 0, 
            "streak": 0,
            "last_accessed": str(chronos.current_date("D M,Y")),
        }
    iohandle.dump_content(PATH,data)

