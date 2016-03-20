
# coding: utf-8

# In[21]:

def make_surface(fig):
     
    #Makes the graph surface based on the functino given
    ax = fig.gca(projection='3d')
    x = np.arange(-2.5, 2.5, .2)
    y = np.arange(-2.5, 2.5, .2)
    x, y = np.meshgrid(x, y)
    r = np.sqrt((x**2) + (y**2))
    z = ((np.sin((x**2) + 3*(y**2))) / ((0.1 + (r**2))) + (x**2) + 5*(y**2))*(np.exp(1-(r**2)) / 2)
    surf=ax.plot_wireframe(x, y, z, rstride=1, cstride=1)
    #surf = ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)

    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

    #fig.colorbar(surf, shrink=0.5, aspect=5)


# In[48]:

def get_function(x = 1, y = 1):
    
    if(x=="None" or y=="None"):
        function="None"
    else:
        r = math.sqrt(math.pow(x, 2) + math.pow(y, 2))
        function = ((math.sin(math.pow(x, 2) + 3*math.pow(y, 2))) / (0.1 + math.pow(r, 2))) + (math.pow(x, 2) + 5*math.pow(y, 2))*(math.exp(1-(math.pow(r, 2))) / 2)
    return function


# In[49]:

def hill_climb(function_to_optimize, step_size, xmin, xmax, ymin, ymax):

    fig = plt.figure()

    curx=random.uniform(xmin, xmax)
    cury=random.uniform(ymin, ymax)
    curz=function_to_optimize(curx, cury)
    
    newx=curx
    newy=cury
    newz=curz
    foundmax=False

    ax = fig.gca(projection='3d')
    
    while foundmax != True:
        
        #Looks at random direction for x
        for x in range(-1,3):
            if(x==2):
                if(newz==curz):
                    foundmax=True
                curx=newx
                cury=newy
                curz=newz
                
                break
            tempx=curx
            tempx+=x*step_size
            
            #Looks at random direction for y
            for y in range(-1, 2):
                tempy=cury
                tempy+=y*step_size
                
                #Checks if in bounds and is going down
                if(tempx>xmin and tempx<xmax and tempy>ymin and tempy<ymax and function_to_optimize(tempx,tempy)<newz):
                    newx=tempx
                    newy=tempy
                    newz=function_to_optimize(newx,newy)
                    
                    #if (fig!=None):
                    ax.scatter(newx, newy, newz, c='r')
                    
  
    #return coordinates 
    return {'x':curx, 'y':cury, 'fig':fig}



# In[50]:

def hill_climb_random_restart(function_to_optimize, step_size, num_restarts, xmin, xmax, ymin, ymax):
    
    fig = plt.figure()
    
    results=[]
    
    if(num_restarts>0):
        for x in range(0,num_restarts):
            curx=random.uniform(xmin, xmax)
            cury=random.uniform(ymin, ymax)
            curz=function_to_optimize(curx, cury)

            newx=curx
            newy=cury
            newz=curz
            foundmax=False

            ax = fig.gca(projection='3d')

            while foundmax != True:

                #Gets random direction for x
                for x in range(-1,3):
                    if(x==2):
                        if(newz==curz):
                            foundmax=True
                        curx=newx
                        cury=newy
                        curz=newz

                        break
                    tempx=curx
                    tempx+=x*step_size

                    #Gets random direction for y
                    for y in range(-1, 2):
                        tempy=cury
                        tempy+=y*step_size

                        #Checks if in bounds and is going down
                        if(tempx>xmin and tempx<xmax and tempy>ymin and tempy<ymax and function_to_optimize(tempx,tempy)<newz):
                            newx=tempx
                            newy=tempy
                            newz=function_to_optimize(newx,newy)

                            #if (fig!=None):
                            ax.scatter(newx, newy, newz, c='r')

                results.append({'x':curx, 'y':cury})
        
        
        best_coord={'x':results[0]['x'], 'y':results[0]['y']}
        cur_result=function_to_optimize(best_coord['x'],best_coord['y'])


        #Goes through all hill climbing results
        for data in results:
            temp_result=function_to_optimize(data['x'],data['y'])

            #Compares and looks for best result
            if(temp_result<cur_result):
                best_coord['x']=data['x']
                best_coord['y']=data['y']
                cur_result=function_to_optimize(best_coord['x'],best_coord['y'])


        best_coord['fig']=fig        
    
    else:
        best_coord={'x':"None", 'y':"None", 'fig':fig}
        
    return best_coord


# In[51]:

def simulated_annealing(function_to_optimize, step_size, max_temp, xmin, xmax, ymin, ymax):
    
    fig = plt.figure()
    
    T=max_temp
    

    curx=random.uniform(xmin, xmax)
    cury=random.uniform(ymin, ymax)
    bestx=curx
    besty=cury
    
    ax = fig.gca(projection='3d')
    
    #P(move)=e^((f(B)-f(A))/T)
    #P=math.pow(math.e,(function_to_optimize(new_coord['x'],new_coord['y'])-function_to_optimize(cur_coord['x'],cur_coord['y'])/T))
    
    while T>0:
        
        #Gets random x coordinate based on temperature
        adjacentx=random.randint(-1,1)
        deviation=random.uniform(0, T)
        tempx=curx
        tempx+=adjacentx*deviation
           
        #Gets random y coordinate based on temperature
        adjacenty=random.randint(-1,1)
        deviation=random.uniform(0, T)
        tempy=cury
        tempy+=adjacenty*deviation
        
        #Checks if within bounds
        if(tempx>xmin and tempx<xmax and tempy>ymin and tempy<ymax):
            if (function_to_optimize(tempx,tempy)<function_to_optimize(bestx,besty)):
                bestx=tempx
                besty=tempy
            
            P=math.e**(function_to_optimize(tempx,tempy)-function_to_optimize(curx, cury)/T)
                      
            if (P>=random.uniform(0, 1)):
                curx=tempx
                cury=tempy
                curz=function_to_optimize(curx, cury)
                
                #Adds points to graph
                ax.scatter(curx, cury, curz, c='r')

        T-=step_size
    
   
                               
    return {'x':bestx, 'y':besty, 'fig':fig}


# In[56]:

def main():
        
    hillclimb=hill_climb(get_function ,.1,-2.5,2.5,-2.5,2.5)
    hillclimbwrandom=hill_climb_random_restart(get_function ,.1,1,-2.5,2.5,-2.5,2.5)
    annealng=simulated_annealing(get_function, 0.001, 3, -2.5, 2.5, -2.5, 2.5)
    
    make_surface(hillclimb['fig'])
    make_surface(hillclimbwrandom['fig'])
    make_surface(annealng['fig'])
    
    plt.show()

    
    print("HillClimb coord: (X:",hillclimb['x'],"Y:",hillclimb['y'],")")
    print("HillClimb z value:",get_function(hillclimb['x'],hillclimb['y']),"\n")
    
    print("HillClimb w/ random restarts coord: (X:",hillclimbwrandom['x'],"Y:",hillclimbwrandom['y'],")")
    print("HillClimb w/ random restarts z value:",get_function(hillclimbwrandom['x'],hillclimbwrandom['y']),"\n")
    
    print("Annealing coord: (X:",annealng['x'],"Y:",annealng['y'],")")
    print("Annealing z value:",get_function(annealng['x'],annealng['y']))
    


# In[57]:

import math
import random
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np

main()


# In[ ]:




# In[ ]:



