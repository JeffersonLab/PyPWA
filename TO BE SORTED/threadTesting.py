from multiprocessing import Pool
import numpy

numToFactor = 976

def isFactor(x):
    result = None
    div = (numToFactor / x)
    if div*x == numToFactor:
        result = (x,div)
    return result

if __name__ == '__main__':
    pool = Pool(processes=4)
    possibleFactors = range(1,int(numpy.floor(numpy.sqrt(numToFactor)))+1)
    print 'Checking ', possibleFactors
    result = pool.map(isFactor, possibleFactors)
    cleaned = [x for x in result if not x is None]
    print 'Factors are', cleaned