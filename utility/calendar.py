from django.utils import timezone
import datetime
from khayyam import *

HOURS_OFFSET=3
MINUTES_OFFSET=30
DAY_LIGHT_SAVING=True
def to_persian_datetime_tag(value,*args, **kwargs):
    if 'pure_text' in kwargs and kwargs['pure_text']==True:
        return f"""
        {date_} {time_}
        """
    try:    
        a=str(PersianCalendar().from_gregorian(value))
        date_=a[:10]
        time_=a[11:]
        greg=value.strftime("%Y/%m/%d %H:%M:%S") 
        return f"""<span class="ltr" title="{greg}">{date_} <small class="mx-1 text-muted">{time_}</small></span>"""
    except:
        return ""

PERSIAN_MONTH_NAMES=[
'فروردین',
'اردیبهشت',
'خرداد',
'تیر',
'مرداد',
'شهریور',
'مهر',
'آبان',
'آذر',
 'دی',
 'بهمن',
 'اسفند'
]

def to_persian_month_name(month):
    # return PERSIAN_MONTH_NAMES[month]
    if month>-1 and month<12:
        return PERSIAN_MONTH_NAMES[month]
    return "نامعتبر"

def days_in_month(year,month,day=1):
    nn=JalaliDate(year=year,month=month,day=day)
    return nn.daysinmonth


class PersianCalendar:
    def __init__(self,date=None):
        if date is None:
            from django.utils import timezone as timezone1
            self.date=timezone1.now()
            self.persian_date=self.from_gregorian(greg_date_time=self.date)
        if date is not None:
            self.date=date
            self.persian_date=self.from_gregorian(greg_date_time=self.date)
    
    def tag(self,value):
        a=self.from_gregorian(value)
        return f'<span title="{value.strftime("%Y/%m/%d %H:%M:%S") }">{str(a)}</span>'
    
    def to_gregorian(self,persian_date_input):
            
        if persian_date_input is None or persian_date_input=="" :
            return None
        return self.parse(persian_date_input).date
        
    def parse(self,value,add_time_zone=False):
        if value=="":
            return None
        shamsi_date_time=value

        year_=int(shamsi_date_time[0:4])
        month_=int(shamsi_date_time[5:7])
        day_=int(shamsi_date_time[8:10])
        padding=shamsi_date_time.find(':')
        
        hour_=0
        min_=0
        sec_=0
        
        if not padding==-1:
            padding-=2
            hour_=int(shamsi_date_time[padding:padding+2])
            if hour_>23:
                hour_=23
            if hour_<0:
                hour_=0
            
            padding+=3
            min_=int(shamsi_date_time[padding:padding+2])
            if min_>59:
                min_=59
            if min_<0:
                min_=0
            padding+=3
            if len(shamsi_date_time)>(padding):
                sec_=int(shamsi_date_time[padding:padding+2])
                if sec_>59:
                    sec_=59
                if sec_<0:
                    sec_=0
           
        if month_<7 and DAY_LIGHT_SAVING:
            HOURS_OFFSET_=1
        else:
            HOURS_OFFSET_=0
        self.persian_date = JalaliDatetime(year_, month_, day_, hour_, min_, sec_, 0)
        delta=datetime.timedelta(hours=-HOURS_OFFSET-HOURS_OFFSET_,minutes=-MINUTES_OFFSET)
        self.date=self.persian_date.todatetime()+delta
        
        return self
    
    def from_gregorian(self,greg_date_time,add_time_zone=True):
        if greg_date_time is None:
            return None
        year_=greg_date_time.year
        month_=greg_date_time.month
        day_=greg_date_time.day
        try:
            hour_=greg_date_time.hour
        except:
            hour_=0
        try:
            min_=greg_date_time.minute
        except:
            min_=0
        try:
            sec_=greg_date_time.second
        except:
            sec_=0
            
        sss=TehranTimezone()
        delta=datetime.timedelta(hours=HOURS_OFFSET,minutes=MINUTES_OFFSET)
        # delta=datetime.timedelta(hours=4,minutes=30)
        a=JalaliDatetime(datetime.datetime(year_, month_, day_, hour_, min_, sec_, 0, TehranTimezone())+delta)
        if a.month<7 and DAY_LIGHT_SAVING:
            delta2=datetime.timedelta(hours=1)
            a=JalaliDatetime(datetime.datetime(year_, month_, day_, hour_, min_, sec_, 0, TehranTimezone())+delta+delta2)
        return a.strftime("%Y/%m/%d %H:%M:%S")