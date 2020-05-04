"""
---> Author : Gautham J.S
@gothWare
"""
import numpy as np
import string
import random
import math
import time
import matplotlib.pyplot as plt

class Object:
    def __init__(self, curr_x, curr_y):
        self.score = 0.0
        self.length = 2
        self.genes = []
        self.mutateFlag = False
        self.curr_x = curr_x
        self.curr_y = curr_y
    
    def newChar(self):
        return "".join(random.choice(string.ascii_letters + " "))

    def newCoordinate(self):
        return [self.curr_x + random.uniform(-3,3) , self.curr_y + random.uniform(-3,3)]


    def geneCoder(self):
        self.genes = self.newCoordinate()


    def fitnessMeas(self,target):
        scr = 0
        scr = np.sqrt( (self.genes[0]-target[0])**2 + (self.genes[1]-target[1])**2 )
        self.score = 5/scr
        return 5/scr

    def crossOver(self,partner):
        baccha = Object(self.genes[0],self.genes[1])
        slicePoint = np.floor(random.randint(0,len(self.genes)))
        for i in range(0,len(self.genes)):
            if i>slicePoint:
                baccha.genes.append(self.genes[i])
            else:
                baccha.genes.append(partner.genes[i])
        return baccha

    def mutate(self,mut_rate):
        for i in range(0,len(self.genes)):
            if random.uniform(0,1) < mut_rate:
                self.genes[i] = self.newCoordinate()[i]
                self.mutateFlag = True






class Population:
    def __init__(self, target, start, mut_rate, maxPop):
        self.maxPop = maxPop
        self.mut_rate = mut_rate
        self.target = target
        self.start = start

        self.population = []
        self.popGenecode = []
        self.matepool = []
        self.fitnessArr = []
        self.prevPopulation = []
        self.generation = 0
        self.finishState = False
        self.fittestPopElement = []

        self.fittest = 0
        self.normFitness = [] 

    def populationInit(self):
        for i in range(0,self.maxPop):
            ob = Object(self.start[0],self.start[1])
            ob.geneCoder()
            self.population.append(ob)
            self.popGenecode.append(ob.genes)
    
    def fitnessChk(self):
        #fitn = []
        for i in range(len(self.population)):
            self.fitnessArr.append(self.population[i].fitnessMeas(self.target))

    
    def selectionProc(self):
        self.fittest = 0.0
        for i in range(0,len(self.target)):
            if self.population[i].score>self.fittest:
                self.fittest = self.population[i].score
                self.fittestPopElement = self.population[i].genes
        
        lower = 0
        upper = 1
        #TO BE TESTED self.population[i].score VAL
        for i in range(0,len(self.population)):
            normFit = math.floor((self.population[i].score)*100)
            self.normFitness.append(normFit)
            for j in range(0,normFit):
                self.matepool.append(self.population[i])

    def sexytime(self):
        for i in range(0,len(self.population)):
            index_a = math.floor( random.randint(1,len(self.matepool)) )
            index_b = math.floor( random.randint(1,len(self.matepool)) )
            index_c = math.floor( random.randint(1,len(self.matepool)) )
            index_d = math.floor( random.randint(1,len(self.matepool)) )
            partner_a = self.matepool[index_a-1]
            partner_b = self.matepool[index_b-1]
            partner_c = self.matepool[index_c-1]
            partner_d = self.matepool[index_d-1]
            child = partner_a.crossOver(partner_b)
            child2 = child.crossOver(partner_c)
            child3 = child2.crossOver(partner_d)
            child3.mutate(self.mut_rate)
            self.population[i] = child3

    
    def finishCheck(self):
        if self.fittest > 5:
            self.finishState=True


if __name__ == "__main__":

    target = [50,50]
    start = [0,0]
    popMax = 20
    mutRate = 0.01
    abstart = start
    pop = Population(target,start,mutRate,popMax)
    pop.populationInit()
    t1 = time.time()
    tstart = time.time() 
    xarr = []
    yarr = []
    refreshIter = 0
    while True:
        pop.fitnessChk()
        pop.selectionProc()
        pop.sexytime()
        pop.finishCheck()
        print("population is : {}, with fitness : {}\n".format(pop.fittestPopElement,pop.fittest))
        xarr.append(pop.fittestPopElement[0])
        yarr.append(pop.fittestPopElement[1])
        tt = time.time()
        if pop.finishState==True:
            t2 = time.time()
            print("Optimal Evolution found in {} s".format(t2-t1))
            break
        if tt-t1>2:
                refreshIter+=1
                t1 = time.time()
                start = [pop.fittestPopElement[0],pop.fittestPopElement[1]]
                pop = Population(target,start,mutRate,popMax)
                pop.populationInit()
                print("Initialized fresh population with fittest element")
        elif tt-tstart>100:
            print("Time limit reached")
            break
    plt.scatter(pop.fittestPopElement[0],pop.fittestPopElement[1],c="r",s = 200,marker="x")
    plt.scatter(xarr,yarr,marker="x")
    plt.scatter(target[0],target[1],s=200)
    plt.scatter(abstart[0],abstart[1],s=200)
    plt.grid()
    plt.show()
    

