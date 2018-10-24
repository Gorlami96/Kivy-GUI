import fdb
import time
import random
import uuid
import numpy as np
import matplotlib.pyplot as plt

con = fdb.connect(host='localhost',database='G:\Report_builder_Adani\Report_builder_Adani\TEST.fdb', user='SYSDBA', password='masterkey')
cur = con.cursor()
##cur.execute("CREATE TABLE sensors(uuid varchar(50) NOT NULL,xname varchar(50) NOT NULL,xtime bigint NOT NULL,xvalue float NOT NULL)")
##con.commit()
uuids = []
key = 1
names = ['temperature','pressure','flow','volume']
for i in range(0,4):
        uuids.append(uuid.uuid4())
x=0;
x_axis=[]
rand=[]
while(key<1200):
        nowTime = int(round(time.time() * 1000))
        for i in range(0,4):
                randomNum = random.uniform(0,100)
                randomNum += abs(1000*np.sin(x))
                rand.append(randomNum)
                x_axis.append(x)
                x+=5;
                command = "INSERT INTO sensors values("+"'"+str(uuids[i])+"',"+"'"+names[i]+"',"+str(nowTime)+","+str(randomNum)+")"
                print(command)
                cur.execute(command)
                key+=1
                con.commit()
        time.sleep(1)

##plt.plot(x_axis,rand)
##plt.show()
