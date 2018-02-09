import datetime, os, shelve

path=r"C:\Users\hp\Dropbox\Python Projects\Expenses\Expenses.txt"

outStrings={"mlm":"Money Left for the Month: ",
            "cmd":"Add Expense/Income: \n\n",
            "tml":"Total Money Left: ",
            "expd":"Expenses of the day: ",
           "dep":"Daily Expenditure Permitted"}

categ={"F":"Food","T":"Travel","PH":"Personal Hygiene"}

def breakIn(inp=">>>>F 10<>>>>PH 20"):
    inp=[x[4:].split() for x in inp.split("<")]
    a=[addExp(exp) if (exp[0] in categ.keys()) else perfTask(exp) for exp in list(map(lambda x:[categ[x[0]],x[1]],inp))]
    
def perfTask(tsk):
  pass
 
def readShel():
    if(not os.path.isdir("Data")):
        os.mkdir("Data")
    os.chdir("Data")

def closeShel():
    expenses["expenses"]=d
    expenses.close()

def refrShel():
    expenses.clear()

def getDateTime():
    x=str(datetime.datetime.today()).split()
    return x[0],x[1].split('.')[0]

def readTxt():
    f=open(path,'r')
    txt=f.read()
    f.close()
    return txt

def writeThis(txt="Test"):
    f=open(path,'w')
    f.write(txt)
    f.close()
 
def readCmd():
    txt=readTxt()
    bg=txt.find('>')
    end=txt.rfind('<')
    return txt[bg:end]

def formatTxt():
    return genNormOut()+"\n\n"+outStrings['cmd']

dt,tm=getDateTime()

def addInc(inc):
    d["curMonthMoney"]=d.get("curMonthMoney",0)+inc
    d["tml"]=d.get("tml",0)+inc
 
def addExp(exp):
    cat,am=exp[0],int(exp[1])
    if(cat=='INC'):
      addInc(am)
      am=-am
    else:
      dtExp=d.get(dt)
      if(not dtExp):
          d[dt]=[]
          dtExp=d.get(dt)
      dtExp.append([cat,am])
    d["tml"]=d.get("tml",0)-am
    d["curMonthMoney"]=d.get("curMonthMoney",0)-am
  
def getSumDayExp(dt=dt):
  return sum([x[1] for x in d.get(dt)])
 
def forgeDate(y,m,d):
  return datetime.datetime(year=y, month=m, day=d)
 
def genNormOut():
  return outStrings["tml"]+str(d["tml"])+"\n"+outStrings["expd"]+str(getSumDayExp())+"\n"+outStrings["mlm"]+str(d["curMonthMoney"])
 
def getSumDateRanExp(stDate,endDate):
  dateRan=[str(stDate+datetime.timedelta(n)).split()[0] for n in range(int((endDate - stDate).days))]
  return sum([getSumDayExp(str(x)) for x in dateRan])

def getSumMonExp(y,m):
  return getSumDateRanExp(forgeDate(y,m,1),forgeDate([y,y+1][m==12],[m+1,1][m==12],1))
 
def getDayExpAllowed(y,m):
  noDays=(forgeDate([y,y+1][m==12],[m+1,1][m==12],1)-forgeDate(y,m,1)).days
  return d["curMonthMoney"]/noDays
 
cmd=None
try:
  readShel()
  expenses=shelve.open("exp_data")
  d=expenses.get("expenses",{})
  cmd=readCmd()
  breakIn(cmd)
  writeThis(genNormOut())
  closeShel()
except Exception as e:
  writeThis(str(e))
