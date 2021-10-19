# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 16:47:58 2018

@author: chong
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 16:23:08 2018

@author: chong
"""
import matplotlib.pyplot as plt

def change_rain(rain,time,orifile,outfile):
    #orifile中仅有管网数据，没有泵的运行数据
    #outfile是orifile加上降雨数据之后得到的
    
    def handle_line(line, title):
        flag=False
        if line.find(title) >= 0:
            flag = True
        return flag
    
    output = open(outfile, 'wt')
    with open(orifile, 'rt') as data:
        time_flag=  False
        k=0
        for line in data:
            # Aim at three property to update origin data
            line = line.rstrip('\n')
            
            if not time_flag:
                time_flag = handle_line(line, '[TIMESERIES]')
                
            if time_flag:
                if k==0:
                    k+=1
                    output.write(line + '\n')
                else:
                    if line.find(';')>=0 and k<2:
                        k+=1
                        output.write(line + '\n')
                    else:
                        tem=line + '\n'
                        it=0
                        for item in time:
                            tem+='10y'+' '*25+item+' '*6+str(rain[it])+'\n'
                            it+=1
                        tem+=';'+'\n'
                        output.write(tem)
                        time_flag=False
            else:
                output.write(line + '\n')
    output.close()

if __name__ == '__main__':
    infile='ori_model.inp'
    outfile='out_model.inp'
    A=10#random.randint(5,15)
    C=13#random.randint(5,20)
    P=2#random.randint(1,5)
    b=1#random.randint(1,3)
    n=0.5#random.random()
    R=0.5#random.random()
    deltt=1
    
    date_time=['08:00','08:05','08:10','08:15','08:20','08:25',\
                        '08:30','08:35','08:40','08:45','08:50','08:55',\
                        '09:00','09:05','09:10','09:15','09:20','09:25',\
                        '09:30','09:35','09:40','09:45','09:50','09:55',\
                        '10:00','10:05','10:10','10:15','10:20','10:25',\
                        '10:30','10:35','10:40','10:45','10:50','10:55',\
                        '11:00','11:05','11:10','11:15','11:20','11:25',\
                        '11:30','11:35','11:40','11:45','11:50','11:55','12:00']
    #change_rain(A,C,P,b,n,infile,outfile)
    rain=[10.0 for _ in range(240)]
    #plt.plot(range(240),rain)
    #copy_result(infile,'arg-original.inp')
    change_rain(rain,date_time,infile,outfile)