import numpy as np
import random 
import math
import matplotlib.pyplot as plt
import time

class Group:
    def __init__(self,linearr,botpos,grplen):
        self.linearr = [[list(j) for j in i] for i in linearr]
        self.botpos = botpos
        self.grplen = grplen
        #print("Lines are : {}".format(self.linearr))
        self.fitness = 0
        self.genes = []
    
    def calCost(self):
        st_en_inversion_flag = False
        def eucledian_dist(xst,yst,xen,yen):
            return np.sqrt( ((xst-xen)**2) + ((yst-yen)**2) )
        

        initcost = 0
        for line in self.linearr:
            xst = line[0][0]
            yst = line[0][1]
            xen = line[1][0]
            yen = line[1][1]
            linedist = eucledian_dist(xst,yst,xen,yen)
            self.genes.append(line)
            initcost+=linedist
        for i in range(1,len(self.linearr)):
            pr_line = self.linearr[i-1]
            cur_line = self.linearr[i]
            initcost+= eucledian_dist(pr_line[1][0],pr_line[1][1],cur_line[1][0],cur_line[1][0])
        self.fitness = 1/initcost
        #print(self.fitness)
        
    def crossover(self,partner):
        self.calCost()
        child = Group(self.linearr,self.botpos,len(self.linearr))
        slicept = random.randint(0,self.grplen)
        try:
            for i in range(self.grplen):
                if len(partner.genes)==len(self.genes):
                    if i<slicept:
                        child.genes.append(self.genes[i])
                        #print("selfgenes")
                    else:
                        child.genes.append(partner.genes[i])
                        #print("partnergenes")
                else:
                    if i<slicept:
                        child.genes.append(self.genes[i])
                        #print("selfgenes")
                    else:
                        child.genes.append(partner.genes[i])
                       # print("partnergenes")
            #print("The genes appended at crossover fun is {}".format(child.genes))
            return child
        except IndexError as I:
            #print("index is {}, gene length is {}".format(i,(partner.genes)))
            return child


       
                
    
class Population:
    def __init__(self,lineset,botpos,mutrate):
        self.lineset = lineset
        self.botpos = botpos
        self.mutrate = mutrate
        #print("Lineset is : {}".format(self.lineset))

        self.population = []
        self.fittest_element = None
        self.matepool = []
        self.group = np.empty((0,2,2),float)

        self.max_fitness = 0
        self.finish_state = False

    def group_gen(self):
        self.group = np.empty((0,2,2),float)
        self.group = [self.group for i in range(len(self.botpos))]
        random.shuffle(self.lineset)
        #print(self.lineset)
        for index, val in enumerate(self.lineset):
            n = index % len(self.botpos)
            self.group[n] = np.append(self.group[n], np.array([val]), axis = 0)
    
    def popInit(self):
        self.group_gen()
        for index,grp in enumerate(self.group):
            linearr = []
            botn = self.botpos[index]
            for lines in grp:
                linearr.append(lines)
            g = Group(linearr,botn,len(linearr))
            g.calCost()
            self.population.append( g )

    def popInitITER(self):
        self.group_gen()
        for index,grp in enumerate(self.group):
            linearr = []
            botn = self.botpos[index]
            for lines in grp:
                linearr.append(lines)
            g = Group(linearr,botn,len(linearr))
            g.calCost()
            self.population[index] =  g 

    def selection(self):
        max_fitness = 0
        for i in range(len(self.population)):
            if self.population[i].fitness>max_fitness:
                self.max_fitness = self.population[i].fitness
                self.fittest_element = self.population[i]
        for i in range(len(self.population)):
            normfac = math.floor((self.population[i].fitness)*1000)
            for j in range(0,normfac):
                self.matepool.append(self.population[i])
        

    def master(self):
        for i in range(len(self.population)):
            index_a = math.floor( random.randint(1,len(self.matepool)) )
            index_b = math.floor( random.randint(1,len(self.matepool)) )
            partner_a = self.matepool[index_a-1]
            partner_b = self.matepool[index_b-1]
            child = partner_a.crossover(partner_b)
            #child.calCost()
            #self.__init__(self.lineset, self.botpos, self.mutrate)
            #print("Child genes are {}".format(child.genes))
            self.population[i] = child

"""
Only error in crossover fun creating empty genes
"""

if __name__ == "__main__":
    lineSet = [ [[1,11], [11,1]] , [[2,22], [22,2]] , [[3,33], [33,3]] , [[4,44], [44,4]] , [[5,55], [55,5]] ]
    botpos = [[0,1] , [70,2] , [2,60]] 

    
    #pop.group_gen()
    pop = Population(lineSet,botpos,0.1)
    pop.popInit()
    while True:
        
        pop.popInitITER()
        pop.selection()
        pop.master()
        time.sleep(0.2)
        print("\npopulation genes are : {}\n".format([pop.population[i].genes for i in range(len(pop.population))]))
        #print(len(pop.population))
    
    clrmap = ["g","r","b"]
    for index,grp in enumerate(pop.group):
            startarr = []
            endarr = []
            botn = botpos[index]
            for lines in grp:
                plt.plot([lines[0][0],lines[0][1]],[lines[1][0],lines[1][0]],c=clrmap[index])
    [plt.scatter(i[0],i[1],c=clrmap[ind]) for ind,i in enumerate(botpos)]
    plt.show()
        
    #print([i.fitness for i in pop.population])
    #print(pop.group)
    

