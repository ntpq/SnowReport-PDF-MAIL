import requests
from bs4 import BeautifulSoup
import time,calendar
from datetime import date
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Flowable, Paragraph, Spacer, Image,Table, TableStyle, Paragraph, Frame, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch,mm
from reportlab.lib.enums import TA_RIGHT,TA_JUSTIFY
WebRemarkable = "https://www.theremarkables.co.nz/weather-report"
WebCoronetpeak = "https://www.coronetpeak.co.nz/weather-report"
WebCardrona = "https://www.snowhq.com/nz/queenstown-and-wanaka/cardrona/cardrona-snow-report"

class MCLine(Flowable):
   """Line flowable --- draws a line in a flowable"""

   def __init__(self,width):
      Flowable.__init__(self)
      self.width = width

   def __repr__(self):
      return "Line(w=%s)" % self.width

   def draw(self):
      self.canv.line(0,0,self.width,0)
def TextNormal(Story,topic,data):
    ptext = '<font size=20>%s : %s</font>' %(topic,data)
    Story.append(Paragraph(ptext, styles["Normal"]))
    NewLine(Story)

def info(Story,Name,Temp,MountainStatus,RoadStatus,ChainStatus,RoadCondition,LastTime):
    NameHTML = '<b><font size=25>%s</font></b>' % Name
    TempHTML = '<b><font size=25>%s</font></b>' % Temp

    ############## Table for Name and Temp ##########
    style_right = ParagraphStyle(name='right', parent=styles['Normal'], alignment=TA_RIGHT)
    tbl_data = [
        [Paragraph(NameHTML, styles["Normal"]), Paragraph(TempHTML, style_right)]
    ]
    tbl = Table(tbl_data)
    Story.append(tbl)
    NewLine(Story)
    #NewLine(Story)
    TextNormal(Story,'Mountain Status',MountainStatus)
    TextNormal(Story,'Road Status',RoadStatus)
    TextNormal(Story,'Chain Status',ChainStatus)
    ######## Road Condition ######
    ptext = '<font size=20>Road Condition </font>'
    Story.append(Paragraph(ptext, styles["Normal"]))   
    Story.append(Spacer(1, 12)) 
    ptext = '<font size=12>%s</font>' %RoadCondition
    Story.append(Paragraph(ptext, styles["Justify"]))
    #NewLine(Story)
    ptext = '<font size=12>%s</font>' %LastTime
    Story.append(Paragraph(ptext, style_right))
    NewLine(Story)
    line = MCLine(530)
    Story.append(line)
    #NewLine(Story)

def NewLine(Story):
    spacer = Spacer(0, 0.25*inch)
    Story.append(spacer)
    #Story.append(Spacer(1, 12))
def addCredit(canvas, doc):
    text = "Create By _NTPQ :)"
    canvas.drawRightString(200*mm, 20*mm, text)
class SnowReport:
    Name = 0
    Temp = 0
    Time = 0
    MountainStatus = 0
    RoadStatus = 0
    ChainStatus = 0
    RoadCondition = 0
    Web = 0
##### Start ####
doc = SimpleDocTemplate("form_letter.pdf",pagesize=letter,
                        rightMargin=36,leftMargin=36,
                        topMargin=36,bottomMargin=18)
Story=[]
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
########### Head ##########
Head = '<b><u><font size=40>Snow Report</font></u></b>'
HeadStyle = styles['Heading1']
HeadStyle.alignment = 1
Story.append(Paragraph(Head,HeadStyle))
NewLine(Story)

Skifield = ['Remarkable','Coronetpeak','Cardrona']
for i in Skifield :
   name = i;
   i = SnowReport();
   i.Name = name;
   if (i.Name == 'Remarkable') or (i.Name == 'Coronetpeak'):
      if(i.Name == 'Remarkable'):
         i.Web = WebRemarkable;
      elif(i.Name == 'Coronetpeak'):
         i.Web = WebCoronetpeak;
      #print(i.Web)
      WebRequest = requests.get(i.Web)
      soup = BeautifulSoup(WebRequest.content, "html.parser")
      i.Temp = soup.find_all("p",{"class":"weather-report__weather__temperture"})[0].text
      i.Time = soup.find_all("span",{"class":"weather-report__weather__details-update"})[0].text
      i.MountainStatus = soup.select('#mountain-full-weather > div > div > div.col-12.col-xl-8.print-100 > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div > p.w_weather-status__data')[0].text.strip()
      i.RoadStatus = soup.select('#mountain-full-weather > div > div > div.col-12.col-xl-8.print-100 > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div > p.w_weather-status__data')[0].text.strip()
      i.ChainStatus = soup.select('#mountain-full-weather > div > div > div.col-12.col-xl-8.print-100 > div:nth-child(2) > div:nth-child(2) > div:nth-child(3) > div > p.w_weather-status__data')[0].text.strip()
      i.RoadCondition = soup.select('#mountain-full-weather > div > div > div.col-12.col-xl-4.print-100 > div.l-weather-report__info_container.dont-hide > div:nth-child(1) > p')[0].text.strip()
      info(Story,i.Name,i.Temp,i.MountainStatus,i.RoadStatus,i.ChainStatus,i.RoadCondition,i.Time)
   elif(i.Name == 'Cardrona'): 
      i.Web = WebCardrona;
      WebRequest = requests.get(i.Web)
      soup = BeautifulSoup(WebRequest.content, "html.parser")
      i.Temp = soup.select("#fh5co-main > div > section.report-fields > div > div.col-md-4 > ul > li:nth-child(4)")[0].text[13:16]
      i.Time = soup.select("#fh5co-main > div > h5")[0].text
      
      my_date = date.today()
      a = i.Time[15:].split(' ')
      a[2] = a[0]
      a[1] = a[1].split(',')[0]
      a[0] = calendar.day_name[my_date.weekday()]
      a[3] = a[3][:4]
      i.Time = 'Last Update: '+' '.join(a)
      i.MountainStatus = soup.select('#fh5co-main > div > section.report-fields > div > div.col-md-4 > ul > li:nth-child(1) > span')[0].text.strip()
      i.RoadStatus = soup.select('#fh5co-main > div > section.report-fields > div > div.col-md-8 > div > div:nth-child(5) > table > tbody > tr:nth-child(1) > td.text-right > span')[0].text.strip()
      i.ChainStatus = 'Chains Carried'
      i.RoadCondition = soup.select('#fh5co-main > div > section.report-fields > div > div.col-md-8 > div > div:nth-child(5) > table > tbody > tr:nth-child(2) > td')[0].text.strip()
      info(Story,i.Name,i.Temp,i.MountainStatus,i.RoadStatus,i.ChainStatus,i.RoadCondition,i.Time)
    
doc.build(Story,onFirstPage=addCredit, onLaterPages=addCredit)
print('success')