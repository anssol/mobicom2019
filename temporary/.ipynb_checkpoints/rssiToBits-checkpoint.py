from __future__ import generators
import numpy as np
import csv
from matplotlib import pyplot as plt
import glob
import pandas as pd
#from avgRssi import meanRssi

##################### FUNCTIONS #####################
def generatePreambleSequence(preamble, samplesPerBit):
    preambleSequence = np.array([])
    for i in range(0, len(preamble)):
        preambleSequence = np.append(preambleSequence, [preamble[i]] * int(samplesPerBit))
    return preambleSequence.astype(int)

def generatePreambleSequence_2(preamble, samplesPerBit, numberOfOnes):
    preambles = [[]]*len(numberOfOnes)
    for i in range(0, len(numberOfOnes)):
        preambleSequence = np.array([])
        if numberOfOnes[i] % 2 == 0:  
            for j in range(0, len(preamble)):
                index = i/2
                preambleSequence = np.append(preambleSequence, [preamble[j]] * int((numberOfOnes[i]/2)))
        else:
            for j in range(0, len(preamble)):
                preambleSequence = np.append(preambleSequence, [preamble[j]] * int(((numberOfOnes[i]-1)/2)))
            preambleSequence = preambleSequence.astype(int)
            one_index = np.where(preambleSequence == 1)[0]
            preambleSequence[one_index - 1] = 1
        preambles[i] = preambleSequence.astype(int)

    return preambles

# Helper
def getPreambleLength(binaryVals, timeFrame):
    ones = np.where(binaryVals['r1'] == 1)[0]
    times = np.asarray(timeFrame['r1_time'])
    bitTime = times[ones]
    transitions = np.where(bitTime[1:] - bitTime[:-1] > 0.0015)[0]
    numberOfOnes = np.array([])
    for i in range(0, len(transitions)-1):
        numbers = len(bitTime[transitions[i] + 1 : transitions[i+1] + 1])
        numberOfOnes = np.append(numberOfOnes, numbers)
    #print(numberOfOnes.astype(int))
    return numberOfOnes.astype(int)

def generateStringArray(preambles):
    arr = []
    for i in preambles:
        result2 = [str(x) for x in i]
        result2 = ' '.join(result2)
        arr.append(result2)
    return np.array(arr)

def strToInt(uniqueVals):
    vals = [[]]*len(uniqueVals)
    for i in range(0,len(uniqueVals)):
        temp = uniqueVals[i].split(",")
        temp = uniqueVals[i].split()
        integers = [int(x) for x in temp]
        vals[i] = np.array(integers)
    return vals

def KnuthMorrisPratt(text, pattern):

    '''Yields all starting positions of copies of the pattern in the text.
    Calling conventions are similar to string.find, but its arguments can be
    lists or iterators, not just strings, it returns all matches, not just
    the first one, and it does not need the whole text in memory at once.
    Whenever it yields, it will have read the text exactly up to and including
    the match that caused the yield.'''
# allow indexing into pattern and protect against change during yield
    pattern = list(pattern)

    # build table of shift amounts
    shifts = [1] * (len(pattern) + 1)
    shift = 1
    for pos in range(len(pattern)):
        while shift <= pos and pattern[pos] != pattern[pos-shift]:
            shift += shifts[pos-shift]
        shifts[pos+1] = shift

    # do the actual search
    startPos = 0
    matchLen = 0
    for c in text:
        while matchLen == len(pattern) or \
              matchLen >= 0 and pattern[matchLen] != c:
            startPos += shifts[matchLen]
            matchLen -= shifts[matchLen]
        matchLen += 1
        if matchLen == len(pattern):
            yield startPos

# With Preamble
def extractBits(sequences, preambleSequence, samplesPerBit, nbits):
    stream = [[]]*len(sequences)
    compressedStream = [[]]*len(sequences)
    bitStream = []
    k = 0
    try:
        for i in sequences:
            stream[k] = rssiVals[i:i+len(preambleSequence)+int(nbits*samplesPerBit)]
            # Compress the bits to nBit-format
            for j in range(0, 4+nbits):
                bit = stream[k][j + j*samplesPerBit]
                bitStream.append(bit)
            compressedStream[k] = bitStream
            bitStream = []
            k += 1
    except:
        pass
    return stream, compressedStream

# No preamble
def extractDataBits(sequences, preambleSequence, samplesPerBit, nbits):
    stream = [[]]*len(sequences)
    compressedStream = [[]]*len(sequences)
    bitStream = []
    k = 0
    try:
        for i in sequences:
            stream[k] = rssiVals[i+len(preambleSequence):i+len(preambleSequence)+int(nbits*samplesPerBit)-1]
            # Compress the bits to nBit-format
            for j in range(0, nbits):
                bit = stream[k][j + j*samplesPerBit]
                bitStream.append(bit)
            compressedStream[k] = bitStream
            bitStream = []
            k += 1
    except:
        pass
    return stream, compressedStream

# Move to another file later ##
def bool2int(x):
    y = 0
    for i,j in enumerate(x):
        y += j << i
    return y

def getIdentifiers(decimalArray):
    idArray = []
    k = 0
    for i in decimalArray:
        if i == 1:
            #idArray = np.append(idArray, '1')

            idArray.append(tuple([1, k]))
        elif i == 2:
            #idArray = np.append(idArray, '2')

            idArray.append(tuple([2, k]))
        elif i == 3:
            #idArray = np.append(idArray, '12')
            idArray.append(tuple([12, k]))
        elif i == 4:
            #idArray = np.append(idArray, '3')

            idArray.append(tuple([3, k]))
        elif i == 6:
            idArray.append(tuple([23, k]))

        elif i == 8:
            #idArray = np.append(idArray, '4')
            idArray.append(tuple([4, k]))
        k += 1
    #return idArray.astype(int)
    return idArray

# Do reverse search to find start of the preamble index 
def getStartIndexes(binaryVals, sequences):
    startIndexes = np.array([])
    for i in sequences:
        for j in range(i, i-80, -1):
            # Find start of preamble
            if (binaryVals[j] == 0):
                # Start of preamble occurs at index 'j+1'
                startIndexes = np.append(startIndexes, j+1)
                break
    return startIndexes.astype(int)

#################### END OF FUNCTIONS #####################
