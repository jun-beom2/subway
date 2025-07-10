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

for x in ld.DfLine1_lower["환승"] :
    if pd.notna(x):
        print(x)

def transfer(routes) :
    for index, station in enumerate(routes) :
        if station in ListTrans and index > 0 and index < len(routes)-1:
            if routes[index-1] in ListLine1 and routes[index+1] in ListLine2:
                print(f"{station}에서 내려 1호선에서 2호선으로 갈아타주시길 바랍니다.")
            elif routes[index-1] in ListLine1 and routes[index+1] in ListLine3:
                print(f"{station}에서 내려 1호선에서 3호선으로 갈아타주시길 바랍니다.")
            elif routes[index-1] in ListLine2 and routes[index+1] in ListLine1:
                print(f"{station}에서 내려 2호선에서 1호선으로 갈아타주시길 바랍니다.")
            elif routes[index-1] in ListLine2 and routes[index+1] in ListLine3:
                print(f"{station}에서 내려 2호선에서 3호선으로 갈아타주시길 바랍니다.")
            elif routes[index-1] in ListLine3 and routes[index+1] in ListLine1:
                print(f"{station}에서 내려 3호선에서 1호선으로 갈아타주시길 바랍니다.")
            elif routes[index-1] in ListLine3 and routes[index+1] in ListLine2:
                print(f"{station}에서 내려 3호선에서 2호선으로 갈아타주시길 바랍니다.")


StrDepart = "다사" # input으로 입력받아서 할 예정
StrDestin = "대구역" # input으로 입력받아서 할 예정
IntDepartLine = 0
IntDestinLine = 0
DtCurrenttime = datetime.now() #현재 시간 불러오기

try :
    DictDistance, DictPrev = di.dijkstra(ld.DictInterval_data,StrDepart)
    ListRoutes = di.routes(DictPrev,StrDestin)
    DtArrivaltime = DtCurrenttime + timedelta(minutes=DictDistance[StrDestin])

    print("현재시각", DtCurrenttime.time().strftime("%H:%M"))
    print("최단시간", DictDistance[StrDestin])
    print("도착시각", DtArrivaltime.strftime("%H:%M"))
    print(ListRoutes)

    transfer(ListRoutes)
    
except KeyError as e:
    print("역명을 확인해주세요",e)




