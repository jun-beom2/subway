import pandas as pd
from datetime import datetime, timedelta

import dijkstra as di
import loader as ld
import utils


#예시 인풋

ex_depart = "반월당"
ex_destin = "칠성시장"

temp = ld.DfLine1_upper.loc[0]


ListLine1 = []
ListLine2 = []
ListLine3 = [] 
ListTrans = []


for x in ld.DfLine1_lower["역명"] :
    ListLine1.append(x)

for x in ld.DfLine2_lower["역명"] :
    ListLine2.append(x)

for x in ld.DfLine3_lower["역명"] :
    ListLine3.append(x)

for station in ListLine1 :
    if station in ListLine2 :
        ListTrans.append(station)
    elif station in ListLine3 :
        ListTrans.append(station)
for station in ListLine2 :
    if station in ListLine3 :
        ListTrans.append(station)

ListLines = [ListLine1,ListLine2,ListLine3]

def checkupdown(start, end, listline) :
    
    if start in listline and end in listline :
        return listline.index(start) - listline.index(end)
    #리턴 값이 음수면 하행 양수면 상행
    return 0

def getdeparttime(depart,destin) :
    
    departtime=0
    currenttime = datetime.now() #현재 시간 불러오기
    currenttime = currenttime.time().strftime("%H:%M")

    fmt = "%H:%M"
    fmts = "%H:%M:%S"

    if destin == "없음" :
        destin = StrDestin
    
    for i, listline in enumerate(ListLines) :
        if checkupdown(depart,destin,listline) < 0 :
            for index,time in enumerate(ld.DFLines_lower[i].iloc[listline.index(depart)]) :
                if index > 3 and pd.notna(time) :
                    t1 = datetime.strptime(currenttime, fmt)
                    t2 = datetime.strptime(str(time),fmts)
                    diff = t1-t2
                    departtime = t2
                    if diff < timedelta(0):
                        break
        elif checkupdown(depart,destin,listline) > 0 :
            for index,time in enumerate(ld.DfLines_upper[i].iloc[-(listline.index(depart)+1)]) :
                if index > 3 and pd.notna(time) :
                    t1 = datetime.strptime(currenttime, fmt)
                    t2 = datetime.strptime(str(time),fmts)
                    diff = t1-t2
                    departtime = t2
                    if diff < timedelta(0) : 
                        break

    return departtime.time()



def transfer(routes) :
    first = "없음"
    last = "없음"
    count = 0

    listindexs = [(0,1),(0,2),(1,0),(1,2),(2,0),(2,1)]

    for index, station in enumerate(routes) :
        if station in ListTrans and index > 0 and index < len(routes)-1:
            for listindex in listindexs:
                if routes[index-1] in ListLines[listindex[0]] and routes[index+1] in ListLines[listindex[1]] and not routes[index+1] in ListTrans:
                    if count == 0 :
                        first = station
                        last = station
                    last = station
                    count += 1
                    print(f"{station}에서 내려 {listindex[0]+1}호선에서 {listindex[1]+1}호선으로 갈아타주시길 바랍니다.")
    return first, last

StrDepart = "다사" # input으로 입력받아서 할 예정
StrDestin = "교대" # input으로 입력받아서 할 예정

firsttransfer = ""
lasttransfer = ""


#arrivaltime = currenttime + timedelta(minutes=DictDistance[StrDestin])


try :
    DictDistance, DictPrev = di.dijkstra(ld.DictInterval_data,StrDepart)
    ListRoutes = di.routes(DictPrev,StrDestin)
  

    print("최단시간", DictDistance[StrDestin])
    print(ListRoutes)

    firsttransfer,lasttransfer =transfer(ListRoutes)

    #print(checkupdown(StrDepart,firsttransfer,ListLine1))
    #print(checkupdown(StrDepart,firsttransfer,ListLine2))
    #print(checkupdown(StrDepart,firsttransfer,ListLine3))

    TimeDepart= getdeparttime(StrDepart,firsttransfer)
    TimeArrival = timedelta(minutes=DictDistance[StrDestin])
    
    print(f"출발시간: {TimeDepart}")
    print(f"도착시간: {TimeArrival}")

except KeyError as e:
    print("역명을 확인해주세요",e)




