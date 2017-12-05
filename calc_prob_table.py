

"""
Description: This function calculates the suspect AS probability table.
Inputs: suspectAS - a dictionary with key equal to suspect AS, and value 
                    equal to the number of paths that suspect AS compromised.
        exitToDest - a dictionary of AS paths containing all paths from 
                      all exit nodes to all destinations.  Key is in the form [exitAS:destIP].
                      Value is in the form [AS1,AS2,...ASN].
         total - total number of compromised paths
"""
def calcProb(suspectAS,exitToDest,total):
        
        exitProbability={}
        numOfservers=200 #Number of destination servers in shadow config, or how many paths the exit node made in total in the exitToServerPaths.txt
         
        susAS = open('susASes.txt','a')
        
        for AS in suspectAS:
          
            susAS.write(str(suspectAS.get(AS)/(total))+' '+AS+'\n')
            
        susAS.close()
        
        for exit in exitToDest:
            for AS in suspectAS:
                exitAS = exit.strip().split(":")
                if AS in exitToDest.get(exit):
                    
                    if exitAS[0]+":"+AS in exitProbability:
                        exitProbability[exitAS[0]+":"+AS] += 1
                    else:
                        exitProbability[exitAS[0]+":"+AS] = 1
                else:
                    if exitAS[0]+":"+AS not in exitProbability:
                        exitProbability[exitAS[0]+":"+AS] = 0
        
        for x in exitProbability:
            exitProbability[x] = exitProbability.get(x) / numOfservers
        
        sorted_x = sorted(exitProbability.items(), key=operator.itemgetter(0))
        
        w = open("exitProbabilities.txt", 'w+b')
        for x in sorted_x:
            y = x[0].strip().split(":")
            w.write (y[0]+" "+y[1]+" "+str(x[1])+"\n")
        
        return total

def main():
    print "test"

if __name__ == "__main__":
    main()
