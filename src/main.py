import pandas as pd
from datetime import datetime, timedelta

import dijkstra as di
import loader as ld
import utils


#예시 인풋

ex_depart = "반월당"
ex_destin = "칠성시장"



temp = ld.DfLine1_upper.loc[0]


#print(temp.iloc[0])

ListLine1  = []
ListLine2 = []
ListLine3 = [] 
ListTrans = []

for x in ld.DfLine1_lower["역명"] :
    ListLine1.append(x)

for x in ld.DfLine2_lower["역명"] :
    ListLine2.append(x)

for x in ld.DfLine3_lower["역명"] :
    ListLine3.append(x)

if ex_depart in ListLine1 :
    print("1호선")
    print(ListLine1.index(ex_depart))
if ex_depart in ListLine2 :
    print("2호선")
    print(ListLine2.index(ex_depart))
if ex_depart in ListLine3 :
    print("3호선")
    print(ListLine3.index(ex_depart))

for x in ld.DfLine1_lower["환승"] :
    if pd.notna(x):
        print(x)

def transfer(routes) :
    transroutes = []
    for index, station in enumerate(routes) :
        if station in ListTrans & index > 0 & index < len(routes)-1:
            if routes[index-1] != routes[index+1] :
                transroutes.append(station)
    return transroutes


StrDepart = "다사" # input으로 입력받아서 할 예정
StrDestin = "동대구역" # input으로 입력받아서 할 예정
DtCurrenttime = datetime.now() #현재 시간 불러오기

distance, prev = di.dijkstra(ld.DictInterval_data,StrDepart)
m_routes = di.routes(prev,StrDestin)
arrivaltime = DtCurrenttime + timedelta(minutes=distance[StrDestin])


print("현재시각", DtCurrenttime.time().strftime("%H:%M"))
print("최단시간", distance[StrDestin])
print("도착시각", arrivaltime.strftime("%H:%M"))
print(m_routes)

