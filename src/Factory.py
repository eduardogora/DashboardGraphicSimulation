# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 16:33:32 2024

@author: eduar
"""

import simpy 
import random
import json

#mandar a todo el env como parametro


class Product:
    def __init__(self):
        
        # Tiempo en cada estacion
        self.timeS1 = 0
        self.timeS2 = 0
        self.timeS3 = 0
        self.timeS4 = 0
        self.timeS5 = 0
        self.timeS6 = 0
        
        # Tiempo de Espera
        self.waitTime = 0
        
        # Es defectuoso
        self.state = 0
        


def getWorkingTime():
    return abs(random.normalvariate(4))

def getRefillTime():
    return abs(random.normalvariate(4))

def getFixingTime():
    return abs(random.expovariate(3))

def getRandomNumber():
    return random.randint(1, 100)

def printGeneral():
    print("------------GENERAL----------")
    print('Finished Products: %i'% (factory.finishedP))
    print('Rejected Products: %i'% (factory.rejectedP))
    print('Total    Products: %i'% (factory.finishedP + factory.rejectedP))
    

def printStation(station):
    global runTime
    print("------------------------")
    print('Name:              %s'% (station.name))
    print('Production Time:   %.2f'% (station.prodTime))
    print('Down Time:         %.2f'% (runTime - station.prodTime))
    print('Number of failing: %.2f'% (station.failNumber))
    print('Fixing Time:       %.2f'% (station.fixingTime))
    print('Units Left:        %.2f'% (station.material))
    print("------------------------")
    
def printDevice(device):
    print("------------------------")
    print('Name:              %s'  % (device.name))
    print('Production Time:   %.2f'% (device.totalRefillingTime))
    print("------------------------")
    
def printDevices():
    print("----------DEVICES----------")
    printDevice(factory.d1)
    printDevice(factory.d2)
    printDevice(factory.d3)
    

def printStations():
    print("----------Stations----------")
    printStation(factory.s1)
    printStation(factory.s2)
    printStation(factory.s3)
    printStation(factory.s4)
    printStation(factory.s5)
    printStation(factory.s6)


class Device():
    def __init__(self, env, name):
        self.env = env
        self.name = name
        
        self.totalRefillingTime = 0
        self.res = simpy.Resource(self.env, 1)
        
    def refill(self):
        #print("refilling")
        n = getRefillTime()
        self.totalRefillingTime += n
        yield self.env.timeout(n)
        

class Station():
    def __init__(self, probFailing, env, name):
        self.env = env
        self.name = name
        
        self.material = 25
        
        self.prodTime = 0
        
        self.probFailing = probFailing
        self.fixingTime = 0
        self.failNumber = 0
        
        self.res = simpy.Resource(self.env, 1)
        
        
    def getFailingProb(self):
        return random.normalvariate(self.probFailing)
    
    def work(self):
        #print("working")
        n = getWorkingTime()
        self.prodTime += n
        self.material -= 1
        yield self.env.timeout(n)
        
    def repair(self):
        if(getRandomNumber() <= self.probFailing):
           # print("reparing")
            n = getFixingTime()
            self.fixingTime += n
            self.failNumber += 1
            yield self.env.timeout(n)
            
    def chain(self, product):
        #print("chaining")
        with self.res.request() as req:
            #Waiting Time
            before = self.env.now
            yield req
            #after = self.env.now #- before
            after = self.env.now - before
            product.waitTime += after
            
            #print('Before waiting time %.2f' % before)
            #print('After waiting time %.2f' % after)
            #tener tiempo de fin
            yield self.env.process(self.repair())
            yield self.env.process(self.work())
    

class Factory(object):
    def __init__(self, env) -> None:
        self.env = env
        self.fullTime = 0
        
        #Maquinas
        self.s1 = Station(20, self.env, "S1")
        self.s2 = Station(10, self.env, "S2")
        self.s3 = Station(15, self.env, "S3")
        self.s4 = Station( 5, self.env, "S4")
        self.s5 = Station( 7, self.env, "S5")
        self.s6 = Station(10, self.env, "S6")
        
        #Devices
        self.d1 = Device(self.env, "D1")
        self.d2 = Device(self.env, "D2")
        self.d3 = Device(self.env, "D3")
        
        #Productos
        self.finishedP = 0
        self.rejectedP = 0
        # self.action = self.env.process(self.run())
    
        
    def produce(self, producto, num):
        #Entramos a la estación 1
        # Revisamos que tenga material la estación
        if(self.s1.material == 0):
            self.s1.material = 25
            yield self.env.process(self.d1.refill()) #| self.env.process(self.d2.refill()) | self.env.process(self.d3.refill())
        
        #Iniciamos el proceso
        beforeE = self.env.now
        yield self.env.process(self.s1.chain(producto))
        after = self.env.now - beforeE
        self.s1.prodTime += after
        
        #Entramos a la estación 2
        yield self.env.process(self.s2.chain(producto))
        
        #Entramos a la estación 3
        yield self.env.process(self.s3.chain(producto))
        
        if(num % 2 == 0):
            #Entramos a la estación 4
            yield self.env.process(self.s4.chain(producto))
            
            #Entramos a la estación 5
            yield self.env.process(self.s5.chain(producto))
        else:
            #Entramos a la estación 5
            yield self.env.process(self.s5.chain(producto))
            #Entramos a la estación 4
            yield self.env.process(self.s4.chain(producto))
        
        #Entramos a la estación 6
        yield self.env.process(self.s6.chain(producto))
        
        #----------Final-------------------------------------
        if(getRandomNumber() <= 5):
            self.rejectedP += 1
        else:
            self.finishedP += 1
            
        #print('Salio el producto %.2f' % numOfProd)
        products.append(producto)
        

    def run(self, weWork):
        offTime = 500
        while True:
            if(weWork):
                offTime = random.randint(1, runTime)
                
            if(offTime <= self.env.now):
                yield self.env.timeout(runTime - offTime)
                
            #Creamos los productos
            global numOfProd
            numOfProd += 1
            nuevoProducto = Product()
            numProd = random.randint(0, 1)
            yield self.env.process(self.produce(nuevoProducto, numProd))
            


#Variables
runTime = 500
months = 2
weeks = 4*months
days = 28*months
products = []
before = 0
after = 0

numOfProd = 0
finishedProd = 0

#Monthly Info
averageProduction = 0
qualityFailures = 0
ocupancyS1 = 0
ocupancyS2 = 0
ocupancyS3 = 0
ocupancyS4 = 0
ocupancyS5 = 0
ocupancyS6 = 0

DayOcupancyS1 = []
DayOcupancyS2 = []
DayOcupancyS3 = []
DayOcupancyS4 = []
DayOcupancyS5 = []
DayOcupancyS6 = []

downTimeS1 = 0
downTimeS2 = 0
downTimeS3 = 0
downTimeS4 = 0
downTimeS5 = 0
downTimeS6 = 0

DayDownTimeS1 = []
DayDownTimeS2 = []
DayDownTimeS3 = []
DayDownTimeS4 = []
DayDownTimeS5 = []
DayDownTimeS6 = []

fixTimeG = 0

#Data process INFO
List_fixingTime_S1 = []
List_fixingTime_S2 = []
List_fixingTime_S3 = []
List_fixingTime_S4 = []
List_fixingTime_S5 = []
List_fixingTime_S6 = []

List_fixingTime_S1_Week = []
List_fixingTime_S2_Week = []
List_fixingTime_S3_Week = []
List_fixingTime_S4_Week = []
List_fixingTime_S5_Week = []
List_fixingTime_S6_Week = []


List_fixingTime_S1_Month = []
List_fixingTime_S2_Month = []
List_fixingTime_S3_Month = []
List_fixingTime_S4_Month = []
List_fixingTime_S5_Month = []
List_fixingTime_S6_Month = []

finishProduct_Day = []
List_finishProduct_Week = []
List_finishProduct_Month = []

rejectProduct_Day = []
List_rejectProduct_Week = []
List_rejectProduct_Month = []

List_Ocupancy_S1_Week = []
List_Ocupancy_S1_Month = []
List_Ocupancy_S2_Week = []
List_Ocupancy_S2_Month = []
List_Ocupancy_S3_Week = []
List_Ocupancy_S3_Month = []
List_Ocupancy_S4_Week = []
List_Ocupancy_S4_Month = []
List_Ocupancy_S5_Week = []
List_Ocupancy_S5_Month = []
List_Ocupancy_S6_Week = []
List_Ocupancy_S6_Month = []

List_DownTime_S1_Week = []
List_DownTime_S1_Month = []
List_DownTime_S2_Week = []
List_DownTime_S2_Month = []
List_DownTime_S3_Week = []
List_DownTime_S3_Month = []
List_DownTime_S4_Week = []
List_DownTime_S4_Month = []
List_DownTime_S5_Week = []
List_DownTime_S5_Month = []
List_DownTime_S6_Week = []
List_DownTime_S6_Month = []

List_Production = []
List_Production_Week = []
List_Production_Month = []

#Yield stops each 

#Representa tics
for i in range(1, days+1):
    print("-----------DAY %i -----------"% i)
    
    weWork = random.randint(1, 100) == 1
    
    env = simpy.Environment()
    factory = Factory(env)
    env.process(factory.run(weWork))
    env.run(until= runTime)
    printGeneral()
    
    #Fill data
    averageProduction += factory.finishedP
    finishProduct_Day.append(factory.finishedP)
    
    qualityFailures += factory.rejectedP
    rejectProduct_Day.append(factory.rejectedP)
    
    ocupancyS1 += factory.s1.prodTime
    ocupancyS2 += factory.s2.prodTime
    ocupancyS3 += factory.s3.prodTime
    ocupancyS4 += factory.s4.prodTime
    ocupancyS5 += factory.s5.prodTime
    ocupancyS6 += factory.s6.prodTime
    DayOcupancyS1.append(factory.s1.prodTime)
    DayOcupancyS2.append(factory.s2.prodTime)
    DayOcupancyS3.append(factory.s3.prodTime)
    DayOcupancyS4.append(factory.s4.prodTime)
    DayOcupancyS5.append(factory.s5.prodTime)
    DayOcupancyS6.append(factory.s6.prodTime)

    downTimeS1 += runTime - factory.s1.prodTime
    downTimeS2 += runTime - factory.s2.prodTime
    downTimeS3 += runTime - factory.s3.prodTime
    downTimeS4 += runTime - factory.s4.prodTime
    downTimeS5 += runTime - factory.s5.prodTime
    downTimeS6 += runTime - factory.s6.prodTime
    DayDownTimeS1.append(runTime - factory.s1.prodTime)
    DayDownTimeS2.append(runTime - factory.s2.prodTime)
    DayDownTimeS3.append(runTime - factory.s3.prodTime)
    DayDownTimeS4.append(runTime - factory.s4.prodTime)
    DayDownTimeS5.append(runTime - factory.s5.prodTime)
    DayDownTimeS6.append(runTime - factory.s6.prodTime)

    fixTimeG = (factory.s1.fixingTime + factory.s2.fixingTime + factory.s3.fixingTime + factory.s4.fixingTime + factory.s5.fixingTime + factory.s6.fixingTime)/6  
    List_fixingTime_S1.append(factory.s1.fixingTime)
    List_fixingTime_S2.append(factory.s2.fixingTime)
    List_fixingTime_S3.append(factory.s3.fixingTime)
    List_fixingTime_S4.append(factory.s4.fixingTime)
    List_fixingTime_S5.append(factory.s5.fixingTime)
    List_fixingTime_S6.append(factory.s6.fixingTime)
    print()

#for product in products:
    #print('WaitTime: %.2f'% (product.waitTime))


def printMonthly():
    print("Average production: %.2f"% (averageProduction / days))
    print("quality failures:   %.2f"% (qualityFailures / days))
    print("Ocupancy Station 1: %.2f"% (ocupancyS1 / days))
    print("Ocupancy Station 2: %.2f"% (ocupancyS2 / days))
    print("Ocupancy Station 3: %.2f"% (ocupancyS3 / days))
    print("Ocupancy Station 4: %.2f"% (ocupancyS4 / days))
    print("Ocupancy Station 5: %.2f"% (ocupancyS5 / days))
    print("Ocupancy Station 6: %.2f"% (ocupancyS6 / days))
    print("Downtime Station 1: %.2f"% (downTimeS1 / days))
    print("Downtime Station 2: %.2f"% (downTimeS2 / days))
    print("Downtime Station 3: %.2f"% (downTimeS3 / days))
    print("Downtime Station 4: %.2f"% (downTimeS4 / days))
    print("Downtime Station 5: %.2f"% (downTimeS5 / days))
    print("Downtime Station 6: %.2f"% (downTimeS6 / days))
    print("Fixtime           : %.2f"% (fixTimeG / days))
    
    ProcessData()
    
def ProcessData(): 
    #Data Graph1 & 5
    Good = 0
    Bad = 0
    #Data Graph3
    Ocupancy_S1 = 0
    Ocupancy_S2 = 0
    Ocupancy_S3 = 0
    Ocupancy_S4 = 0
    Ocupancy_S5 = 0
    Ocupancy_S6 = 0
    #Data Graph4
    Downtime_S1 = 0
    Downtime_S2 = 0
    Downtime_S3 = 0
    Downtime_S4 = 0
    Downtime_S5 = 0
    Downtime_S6 = 0
    #Data Graph 2
    Tfix_S1 = 0
    Tfix_S2 = 0
    Tfix_S3 = 0
    Tfix_S4 = 0
    Tfix_S5 = 0
    Tfix_S6 = 0
        
    #Brakedown WEEKS
    chek = 1
    for i in range(0,days):
        if chek <= 7:
            Good += finishProduct_Day[i]
            Bad += rejectProduct_Day[i]
            
            Ocupancy_S1 += DayOcupancyS1[i]
            Ocupancy_S2 += DayOcupancyS2[i]
            Ocupancy_S3 += DayOcupancyS3[i]
            Ocupancy_S4 += DayOcupancyS4[i]
            Ocupancy_S5 += DayOcupancyS5[i]
            Ocupancy_S6 += DayOcupancyS6[i]
            
            Downtime_S1 += DayDownTimeS1[i]
            Downtime_S2 += DayDownTimeS2[i]
            Downtime_S3 += DayDownTimeS3[i]
            Downtime_S4 += DayDownTimeS4[i]
            Downtime_S5 += DayDownTimeS5[i]
            Downtime_S6 += DayDownTimeS6[i]
                        
            Tfix_S1 += List_fixingTime_S1[i]
            Tfix_S2 += List_fixingTime_S2[i]
            Tfix_S3 += List_fixingTime_S3[i]
            Tfix_S4 += List_fixingTime_S4[i]
            Tfix_S5 += List_fixingTime_S5[i]
            Tfix_S6 += List_fixingTime_S6[i]
            
            chek += 1
        else:
            chek = 2
            #save products
            List_finishProduct_Week.append(Good)
            List_rejectProduct_Week.append(Bad)
            #save ocupancy
            List_Ocupancy_S1_Week.append(Ocupancy_S1)
            List_Ocupancy_S2_Week.append(Ocupancy_S2)
            List_Ocupancy_S3_Week.append(Ocupancy_S3)
            List_Ocupancy_S4_Week.append(Ocupancy_S4)
            List_Ocupancy_S5_Week.append(Ocupancy_S5)
            List_Ocupancy_S6_Week.append(Ocupancy_S6)
            #save Dowtime
            List_DownTime_S1_Week.append(Downtime_S1)
            List_DownTime_S2_Week.append(Downtime_S2)
            List_DownTime_S3_Week.append(Downtime_S3)
            List_DownTime_S4_Week.append(Downtime_S4)
            List_DownTime_S5_Week.append(Downtime_S5)
            List_DownTime_S6_Week.append(Downtime_S6)
            #save Fixing time
            List_fixingTime_S1_Week.append(Tfix_S1)
            List_fixingTime_S2_Week.append(Tfix_S2)
            List_fixingTime_S3_Week.append(Tfix_S3)
            List_fixingTime_S4_Week.append(Tfix_S4)
            List_fixingTime_S5_Week.append(Tfix_S5)
            List_fixingTime_S6_Week.append(Tfix_S6)
            
            Good = 0
            Bad = 0

            Ocupancy_S1 = 0
            Ocupancy_S2 = 0
            Ocupancy_S3 = 0
            Ocupancy_S4 = 0
            Ocupancy_S5 = 0
            Ocupancy_S6 = 0
            
            Downtime_S1 = 0
            Downtime_S2 = 0
            Downtime_S3 = 0
            Downtime_S4 = 0
            Downtime_S5 = 0
            Downtime_S6 = 0
            
            Tfix_S1 = 0
            Tfix_S2 = 0
            Tfix_S3 = 0
            Tfix_S4 = 0
            Tfix_S5 = 0
            Tfix_S6 = 0
            
            Good += finishProduct_Day[i]
            Bad += rejectProduct_Day[i]
            
            Ocupancy_S1 += DayOcupancyS1[i]
            Ocupancy_S2 += DayOcupancyS2[i]
            Ocupancy_S3 += DayOcupancyS3[i]
            Ocupancy_S4 += DayOcupancyS4[i]
            Ocupancy_S5 += DayOcupancyS5[i]
            Ocupancy_S6 += DayOcupancyS6[i]
            
            Downtime_S1 += DayDownTimeS1[i]
            Downtime_S2 += DayDownTimeS2[i]
            Downtime_S3 += DayDownTimeS3[i]
            Downtime_S4 += DayDownTimeS4[i]
            Downtime_S5 += DayDownTimeS5[i]
            Downtime_S6 += DayDownTimeS6[i]
            
            Tfix_S1 += List_fixingTime_S1[i]
            Tfix_S2 += List_fixingTime_S2[i]
            Tfix_S3 += List_fixingTime_S3[i]
            Tfix_S4 += List_fixingTime_S4[i]
            Tfix_S5 += List_fixingTime_S5[i]
            Tfix_S6 += List_fixingTime_S6[i]
            
    List_finishProduct_Week.append(Good)      #good   WEEK
    List_rejectProduct_Week.append(Bad)   #Reject WEEK
    
    List_Ocupancy_S1_Week.append(Ocupancy_S1)
    List_Ocupancy_S2_Week.append(Ocupancy_S2)
    List_Ocupancy_S3_Week.append(Ocupancy_S3)
    List_Ocupancy_S4_Week.append(Ocupancy_S4)
    List_Ocupancy_S5_Week.append(Ocupancy_S5)
    List_Ocupancy_S6_Week.append(Ocupancy_S6)
    
    List_DownTime_S1_Week.append(Downtime_S1)
    List_DownTime_S2_Week.append(Downtime_S2)
    List_DownTime_S3_Week.append(Downtime_S3)
    List_DownTime_S4_Week.append(Downtime_S4)
    List_DownTime_S5_Week.append(Downtime_S5)
    List_DownTime_S6_Week.append(Downtime_S6)
    
    List_fixingTime_S1_Week.append(Tfix_S1)
    List_fixingTime_S2_Week.append(Tfix_S2)
    List_fixingTime_S3_Week.append(Tfix_S3)
    List_fixingTime_S4_Week.append(Tfix_S4)
    List_fixingTime_S5_Week.append(Tfix_S5)
    List_fixingTime_S6_Week.append(Tfix_S6)
    
    #Brakedown MONTHS
    Good = 0
    Bad = 0

    Ocupancy_S1 = 0
    Ocupancy_S2 = 0
    Ocupancy_S3 = 0
    Ocupancy_S4 = 0
    Ocupancy_S5 = 0
    Ocupancy_S6 = 0
    
    Downtime_S1 = 0
    Downtime_S2 = 0
    Downtime_S3 = 0
    Downtime_S4 = 0
    Downtime_S5 = 0
    Downtime_S6 = 0
    
    Tfix_S1 = 0
    Tfix_S2 = 0
    Tfix_S3 = 0
    Tfix_S4 = 0
    Tfix_S5 = 0
    Tfix_S6 = 0
    
    chek = 1
    for i in range(0,weeks):
        if chek <= 4:
            Good += List_finishProduct_Week[i]
            Bad += List_rejectProduct_Week[i]
            
            Ocupancy_S1 += List_Ocupancy_S1_Week[i]
            Ocupancy_S2 += List_Ocupancy_S2_Week[i]
            Ocupancy_S3 += List_Ocupancy_S3_Week[i]
            Ocupancy_S4 += List_Ocupancy_S4_Week[i]
            Ocupancy_S5 += List_Ocupancy_S5_Week[i]
            Ocupancy_S6 += List_Ocupancy_S6_Week[i]
            
            Downtime_S1 += List_DownTime_S1_Week[i]
            Downtime_S2 += List_DownTime_S2_Week[i]
            Downtime_S3 += List_DownTime_S3_Week[i]
            Downtime_S4 += List_DownTime_S4_Week[i]
            Downtime_S5 += List_DownTime_S5_Week[i]
            Downtime_S6 += List_DownTime_S6_Week[i]
            
            Tfix_S1 += List_fixingTime_S1_Week[i]
            Tfix_S2 += List_fixingTime_S2_Week[i]
            Tfix_S3 += List_fixingTime_S3_Week[i]
            Tfix_S4 += List_fixingTime_S4_Week[i]
            Tfix_S5 += List_fixingTime_S5_Week[i]
            Tfix_S6 += List_fixingTime_S6_Week[i]
            
            chek += 1
        else:
            chek = 2
            #Save products
            List_finishProduct_Month.append(Good)
            List_rejectProduct_Month.append(Bad)
            #Save Ocupancy
            List_Ocupancy_S1_Month.append(Ocupancy_S1)
            List_Ocupancy_S2_Month.append(Ocupancy_S2)
            List_Ocupancy_S3_Month.append(Ocupancy_S3)
            List_Ocupancy_S4_Month.append(Ocupancy_S4)
            List_Ocupancy_S5_Month.append(Ocupancy_S5)
            List_Ocupancy_S6_Month.append(Ocupancy_S6)
            #Save Downtime
            List_DownTime_S1_Month.append(Downtime_S1)
            List_DownTime_S2_Month.append(Downtime_S2)
            List_DownTime_S3_Month.append(Downtime_S3)
            List_DownTime_S4_Month.append(Downtime_S4)
            List_DownTime_S5_Month.append(Downtime_S5)
            List_DownTime_S6_Month.append(Downtime_S6)
    
            List_fixingTime_S1_Month.append(Tfix_S1)
            List_fixingTime_S2_Month.append(Tfix_S2)
            List_fixingTime_S3_Month.append(Tfix_S3)
            List_fixingTime_S4_Month.append(Tfix_S4)
            List_fixingTime_S5_Month.append(Tfix_S5)
            List_fixingTime_S6_Month.append(Tfix_S6)
            
            Good = 0
            Bad = 0

            Ocupancy_S1 = 0
            Ocupancy_S2 = 0
            Ocupancy_S3 = 0
            Ocupancy_S4 = 0
            Ocupancy_S5 = 0
            Ocupancy_S6 = 0
            
            Downtime_S1 = 0
            Downtime_S2 = 0
            Downtime_S3 = 0
            Downtime_S4 = 0
            Downtime_S5 = 0
            Downtime_S6 = 0
            
            Tfix_S1 = 0
            Tfix_S2 = 0
            Tfix_S3 = 0
            Tfix_S4 = 0
            Tfix_S5 = 0
            Tfix_S6 = 0
            
            Good += List_finishProduct_Week[i]
            Bad += List_rejectProduct_Week[i]
            
            Ocupancy_S1 += List_Ocupancy_S1_Week[i]
            Ocupancy_S2 += List_Ocupancy_S2_Week[i]
            Ocupancy_S3 += List_Ocupancy_S3_Week[i]
            Ocupancy_S4 += List_Ocupancy_S4_Week[i]
            Ocupancy_S5 += List_Ocupancy_S5_Week[i]
            Ocupancy_S6 += List_Ocupancy_S6_Week[i]
            
            Downtime_S1 += List_DownTime_S1_Week[i]
            Downtime_S2 += List_DownTime_S2_Week[i]
            Downtime_S3 += List_DownTime_S3_Week[i]
            Downtime_S4 += List_DownTime_S4_Week[i]
            Downtime_S5 += List_DownTime_S5_Week[i]
            Downtime_S6 += List_DownTime_S6_Week[i]
            
            Tfix_S1 += List_fixingTime_S1_Week[i]
            Tfix_S2 += List_fixingTime_S2_Week[i]
            Tfix_S3 += List_fixingTime_S3_Week[i]
            Tfix_S4 += List_fixingTime_S4_Week[i]
            Tfix_S5 += List_fixingTime_S5_Week[i]
            Tfix_S6 += List_fixingTime_S6_Week[i]
            
    List_finishProduct_Month.append(Good)      #good   MONTH
    List_rejectProduct_Month.append(Bad)       #Reject MONTH
    
    List_Ocupancy_S1_Month.append(Ocupancy_S1)
    List_Ocupancy_S2_Month.append(Ocupancy_S2)
    List_Ocupancy_S3_Month.append(Ocupancy_S3)
    List_Ocupancy_S4_Month.append(Ocupancy_S4)
    List_Ocupancy_S5_Month.append(Ocupancy_S5)
    List_Ocupancy_S6_Month.append(Ocupancy_S6)
    
    List_DownTime_S1_Month.append(Downtime_S1)
    List_DownTime_S2_Month.append(Downtime_S2)
    List_DownTime_S3_Month.append(Downtime_S3)
    List_DownTime_S4_Month.append(Downtime_S4)
    List_DownTime_S5_Month.append(Downtime_S5)
    List_DownTime_S6_Month.append(Downtime_S6)
    
    List_fixingTime_S1_Month.append(Tfix_S1)
    List_fixingTime_S2_Month.append(Tfix_S2)
    List_fixingTime_S3_Month.append(Tfix_S3)
    List_fixingTime_S4_Month.append(Tfix_S4)
    List_fixingTime_S5_Month.append(Tfix_S5)
    List_fixingTime_S6_Month.append(Tfix_S6)
    
    #Total Production Data
    for i in range(0,days):
        produccion = finishProduct_Day[i] + rejectProduct_Day[i]
        List_Production.append(produccion)
    for i in range(0,weeks):
        produccion = List_finishProduct_Week[i] + List_rejectProduct_Week[i]
        List_Production_Week.append(produccion)
    for i in range(0,months):
        produccion = List_finishProduct_Month[i] + List_rejectProduct_Month[i]
        List_Production_Month.append(produccion)
    
    #---------------------------------------------------------------------------------- JSON
    x = {
        "Graph1":{
            "weekly": {
                "finish": List_finishProduct_Week, 
                "reject": List_rejectProduct_Week
                },
            "monthly": {
                "finish": List_finishProduct_Month, 
                "reject": List_rejectProduct_Month
                }
            },
        "Graph2":{
            "monthly": {
                "fixingTime_S1": List_fixingTime_S1_Month,
                "fixingTime_S2": List_fixingTime_S2_Month,
                "fixingTime_S3": List_fixingTime_S3_Month,
                "fixingTime_S4": List_fixingTime_S4_Month,
                "fixingTime_S5": List_fixingTime_S5_Month,
                "fixingTime_S6": List_fixingTime_S6_Month
                }
            },
        "Graph3":{
            "weekly": {
                "Ocupancy_S1": List_Ocupancy_S1_Week, 
                "Ocupancy_S2": List_Ocupancy_S2_Week, 
                "Ocupancy_S3": List_Ocupancy_S3_Week, 
                "Ocupancy_S4": List_Ocupancy_S4_Week, 
                "Ocupancy_S5": List_Ocupancy_S5_Week, 
                "Ocupancy_S6": List_Ocupancy_S6_Week
                },
            "monthly": {
                "Ocupancy_S1": List_Ocupancy_S1_Month, 
                "Ocupancy_S2": List_Ocupancy_S2_Month, 
                "Ocupancy_S3": List_Ocupancy_S3_Month, 
                "Ocupancy_S4": List_Ocupancy_S4_Month, 
                "Ocupancy_S5": List_Ocupancy_S5_Month, 
                "Ocupancy_S6": List_Ocupancy_S6_Month
                }
            },
        "Graph4":{
            "weekly": {
                "DownTime_S1": List_DownTime_S1_Week, 
                "DownTime_S2": List_DownTime_S2_Week, 
                "DownTime_S3": List_DownTime_S3_Week, 
                "DownTime_S4": List_DownTime_S4_Week, 
                "DownTime_S5": List_DownTime_S5_Week, 
                "DownTime_S6": List_DownTime_S6_Week
                },
            "monthly": {
                "DownTime_S1": List_DownTime_S1_Month, 
                "DownTime_S2": List_DownTime_S2_Month, 
                "DownTime_S3": List_DownTime_S3_Month, 
                "DownTime_S4": List_DownTime_S4_Month, 
                "DownTime_S5": List_DownTime_S5_Month, 
                "DownTime_S6": List_DownTime_S6_Month
                }
            },
        "Graph5":{
            "daily": {
                "production": List_Production
                },
            "weekly": {
                "production": List_Production_Week
                },
            "monthly": {
                "production": List_Production_Month
                }
            },
        }
    
    # convert into JSON:
    y = json.dumps(x)
    
    with open('DataOutput.json', 'w') as f:
        f.write(y)
    

#print('NumOfProd: %.2f'% (numOfProd))
#print('Finished: %.2f'% (finishedProd))

#printStations()
#printDevices()
#printGeneral()
printMonthly()

    



