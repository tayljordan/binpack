import itertools
import time
import random
from copy import deepcopy
import math
import string
from pprint import pprint

# /*******************************************************
#  * Copyright (C) 2017 Jordan L. Taylor tayljordan@gmail.com
#  * 
#  * binPack can not be copied and/or distributed without the express
#  * permission of Jordan L. Taylor
#  *******************************************************/

# Define the binPack class
class binPack(object):
    # Write the constructor so that the object is initialized with some default constants
    # These can be changed after instantiation
    def __init__(self, factor=.05, iterations=10000, maximumTimeAllowedInSeconds=10,
                 numberOfResultsRequested=1, tankTrueOrVolumeFalse=False):

        # Instatiate class variables
        self.factor = factor
        self.iterations = iterations
        self.maximumTimeAllowedInSeconds = maximumTimeAllowedInSeconds
        self.numberOfResultsRequested = numberOfResultsRequested
        self.tankTrueOrVolumeFalse = tankTrueOrVolumeFalse

    # Gets 8 bit identification for table
    # Should always start with a Alpha char.
    def __get8BitAlphaNumeric(self):
        randomString1BitAlpha = ''.join(
            random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(1))
        randomString15BitAlphaNumeric = ''.join(
            random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in
            range(7))
        randomString8 = randomString1BitAlpha + randomString15BitAlphaNumeric

        return randomString8

    def __scLargeVolume(self, allTankVolAvail, oneProductVolume):

        ''' This method will take all remaining tank volumes available and create combinations for a single volume
        It is different from scSmall due to permutative (factorials) effect of itertools.combinations for large volumes

        ARGUMENTS:
        allTankVolAvail = [626, 639, 1209, 1222, 1548,..., 1313, 1313,710, 723,610, 623]
        oneProductVolume = 1343

        RETURN:
        t0 = sum of volumes of combinations:              [610, 623, 626, 639, 710, 723, 732, 746, 1209,..., 2174, 2174]
        e0 = index of combinations (for tank key indexing):    [(18,), (19,), (0,), (1,), (16,),..., (0, 17), (0, 8) (0, 13), (0, 4), (0, 5)]
        '''

        # Sort tank volumes from largest to smallest

        allTankVolumesAvailable_sorted = sorted(
            allTankVolAvail)  # <- this is to determine combination size, for below two iterations

        # the next two iterations will determine length of
        # combinations i.e. (1,2) where L = 2, vs. (2,3,4) where L = 3, vs (4,5,6,7) where L = 4, etc.

        r0 = 1  # <- how many combinations to BEGIN with. represents at least one sampling index, in this case '1' or L = 1 or (3,), (9,), &c.

        while True:
            x = sum(allTankVolumesAvailable_sorted[-r0:]) - oneProductVolume

            if x >= 0:
                break
            else:
                r0 += 1
                pass

            if r0 > 20:
                return IndexError

        r1 = 1  # <- how many combinations to END with. represents at least one sampling index, in this case '1' or (3,), (9,), &c.

        while True:
            x = oneProductVolume - sum(allTankVolumesAvailable_sorted[
                                       :r1])  # <- sum of first, second, third index of sum(sorted) tank values is subtracted from cargo element (say, 500m3)
            if x <= 0:
                break
            else:
                r1 += 1
                continue

        # Master list of combinations. L2 + L3 + L4, etc.
        c0 = []

        # In case there are not enough potential combinations to warrant pairing down of combinations
        step = None

        # Creates an indexing list for final result
        pK = list(range(len(allTankVolAvail)))

        for nK in range(r0, r1 + 1):

            # Facorials calculated, and stepped - if necessary, to ensure that length of combinations is manageable.
            # Pfact figures out the size of itertools.combinations, without actually running it. it uses math.factorial to accomplish.
            # This is necessary to pare down the number of combinations so that computation does not take too long.
            pfact = int(math.factorial(int(len(allTankVolAvail))) / (
            math.factorial(len(allTankVolAvail) - nK) * math.factorial(nK)))

            if pfact > 100:
                step = int(self.factor * pfact)

                # Create the candidates for stow:
            # pK = tank candidates, nK equals length i.e. 1 = (0,) 2 = (1,2) 3 = (2,3,4)
            # Google islice for more information
            combinations = itertools.combinations(pK, nK)
            c1 = list(itertools.islice(combinations, None, None, step))

            # Adds the intertools.comb at L length to the master list of combinations (c0)
            c0 += c1

        t0 = []

        # Create a list that has the sum(values) of the combinations
        for n, i in enumerate(c0):
            t1 = 0
            for i in c0[n]:
                t1 += allTankVolAvail[i]
            t0.append(t1)
        # Sort both index and volume lists by sum(value), in order.
        e0 = [x for (y, x) in sorted(zip(t0, c0))];
        t0 = sorted(t0)

        return t0, e0

    def __scSmallVolume(self, allTankVolumesAvailable):
        ''' ARGUMENTS:
        allTankVolumesAvailable = [626, 639, 1209, 1222, 1548,..., 1313, 1313,710, 723,610, 623]

        RETURN:
        t0 = sum of volumes of combinations:              [610, 623, 626, 639, 710, 723, 732, 746, 1209,..., 2174, 2174]
        e0 = index of combinations (for key indexing):    [(18,), (19,), (0,), (1,), (16,),..., (0, 17), (0, 8) (0, 13), (0, 4), (0, 5)]
        '''

        # Get combinations of the values, with limitations in mind:
        c0 = []
        for n in range(1, 3):
            # Create a n-length vector of length(allTankVolumesAvailable)
            tankVolumes = range(len(allTankVolumesAvailable))
            # Generate combinations in sorted order
            combinations = itertools.combinations(tankVolumes, n)
            # Slice the combos by their sorted order
            slices = itertools.islice(combinations, None)
            # Add to the collection from each iteration
            c0 += list(slices)

        # Create a list that has the sum(values) of the combinations.
        t0 = []
        for n, i in enumerate(c0):
            t1 = 0
            for i in c0[n]:
                t1 += allTankVolumesAvailable[i]
            t0.append(t1)

        # Sort both index and volume lists by sum(value), in order.
        e0 = [x for (y, x) in sorted(zip(t0, c0))]
        t0 = sorted(t0)

        return t0, e0

    def __tSTOW(self, tK, tV, pK, pN, pV):
        '''
        Generates the stow pack. 

        ARGUMENTS:
        tK= Tank Names
        tV= Tank Volumes
        pK= Product Names
        pN= Product Volumes
        pV= Product Values

        RETURNS:
        uT=
        '''

        # Shuffle the product volumes
        pV_sorted = list(zip(pK, pN, pV))
        random.shuffle(pV_sorted)
        pK[:], pN[:], pV[:] = zip(*pV_sorted)
        # Sort the tank volumes
        pK_sorted = sorted(tV)
        # Get the two largest tanks
        pK_largest = sum(pK_sorted[-2:])

        # uT = tank groupings
        uT = []

        for index, element in enumerate(pV):



            if element > pK_largest:

                # Obtain a list of tank combination candidates, for large volumes
                tC = self.__scLargeVolume(tV, element)


            else:
                # Obtains a list if tank combination candidates, for small volumes
                tC = self.__scSmallVolume(tV)

            # randomfactor
            r = 2
            # Get the values and indexes from scLargeVolume and scSmallVolume
            t0 = tC[0];
            e0 = tC[1]
            # Get list with values equal to or greater than element volume
            mV = [i for i in t0 if i >= element]
            # Pare down the index list (e0) to match the volume list
            e0 = e0[(len(e0) - len(mV)):]
            iR = random.randint(0, r)
            assigned = sorted(e0[iR:][0], reverse=True)

            # Temp buffer
            a2 = []

            for i2, e2 in enumerate(assigned): a2.append(tK[e2])

            uT.append(a2)



            for i2, e2 in enumerate(assigned):
                del tK[e2], tV[e2]

        return uT

    def getPack(self, tVV, pVV, prodsVolKey=None):

        # For commingling
        # Create an alphanumeric ID for each product
        if not prodsVolKey:
            prodsVolKey = [self.__get8BitAlphaNumeric() for _ in range(len(pVV))]

        dP = dict(zip(prodsVolKey, pVV))


        # Not for commingling
        prodsVolName = [x + 5001 for x, y in enumerate(pVV)]
        tVNalt = [x + 7001 for x, y in enumerate(tVV)]
        tVValt = tVV

        tR = 1
        t0 = time.time()

        unique_tanks = []
        unique_tanks_volume = []
        unique_tanks_number = []
        leftOverTanks = []
        leftOverVolume = []

        # If there are too many products (len(PVV)), or if there is not enough tank volume (sum(PVV)), abort and return.
        if (sum(pVV) > sum(tVV)) or (len(pVV) > len(tVV)):
            return None

        # Start the optimization process
        while True:

            tanksVolName = deepcopy(tVNalt)
            tVV = deepcopy(tVValt)

            try:
                # Get the tank stow pack
                a = self.__tSTOW(tanksVolName, tVV, prodsVolKey, prodsVolName, pVV)

                if tanksVolName in unique_tanks:
                    pass

                else:
                    # Append the results.
                    unique_tanks.append([a, deepcopy(prodsVolKey)])
                    unique_tanks_volume.append(sum(tVV))
                    unique_tanks_number.append(len(tanksVolName))
                    leftOverTanks.append(tanksVolName)
                    leftOverVolume.append(tVV)

            except (IndexError, TypeError) as e:
                pass

            # Track the number of iterations as well as the time the iterations have elapsed for.
            # Use these to timeout if computation takes too long.
            tR += 1
            t1 = time.time()
            timeNow = t1 - t0

            numberOfUniqueTanks = len(unique_tanks)

            # Trigger timeout
            # if (numberOfUniqueTanks >= self.numberOfResultsRequested):
            #     # print 'operation finished sucessfully'
            #     break

            if (tR >= self.iterations):
                # print 'iteration limit exceeded'
                break

            if (timeNow >= self.maximumTimeAllowedInSeconds):
                # print 'time limit exceeded'
                break

        X = unique_tanks
        Y = unique_tanks_volume
        unique_tanks = [x for (y, x) in sorted(zip(Y, X), reverse=True, key=lambda pair: pair[0])]

        # Assign the results
        if self.tankTrueOrVolumeFalse:
            X = unique_tanks_volume
            Y = unique_tanks_number
            unique_tanks_volume = [x for (y, x) in sorted(zip(Y, X), reverse=True, key=lambda pair: pair[0])]

            X = leftOverVolume
            leftOverVolume = [x for (y, x) in sorted(zip(Y, X), reverse=True, key=lambda pair: pair[0])]

            X = leftOverTanks
            leftOverTanks = [x for (y, x) in sorted(zip(Y, X), reverse=True, key=lambda pair: pair[0])]
            unique_tanks_number = [y for (y, x) in sorted(zip(Y, X), reverse=True, key=lambda pair: pair[0])]

        else:
            X = unique_tanks_number
            Y = unique_tanks_volume
            unique_tanks_number = [x for (y, x) in sorted(zip(Y, X), reverse=True, key=lambda pair: pair[0])]

            X = leftOverVolume
            leftOverVolume = [x for (y, x) in sorted(zip(Y, X), reverse=True, key=lambda pair: pair[0])]

            X = leftOverTanks
            leftOverTanks = [x for (y, x) in sorted(zip(Y, X), reverse=True, key=lambda pair: pair[0])]
            unique_tanks_volume = [y for (y, x) in sorted(zip(Y, X), reverse=True, key=lambda pair: pair[0])]

        # Something went wrong!
        if unique_tanks == ():
            return None

        #The snippet below gets rid of excess / repeat stows

        stow = unique_tanks

        stowCache = []

        stowCacheIndex = []

        # go through the stow, get the stows and indexes of non-repeat

        for num, item in enumerate(stow):

            if item not in stowCache:
                stowCache.append(item)
                stowCacheIndex.append(num)

        # go through the stow again, get the stows and indexes of non-repeat that are lists within lists
        # i.e. [[[7001], [7003, 7002]], ['JMcaiQxc', 'hIay8gGY']] VS [[[7003, 7002], [7001]], ['hIay8gGY', 'JMcaiQxc']]

        repeatCache = []

        for num, item in enumerate(stowCache):
            sCache = sorted(item[0]), sorted(item[1])
            if sCache not in repeatCache:
                repeatCache.append(sCache)
            else:
                stowCacheIndex[num] = 0

        # get rid of marked indexes (0)

        stowCacheIndex = list(set(stowCacheIndex))
        stowCacheIndex.sort()


        unique_tanks = [v for i, v in enumerate(unique_tanks) if i in stowCacheIndex]
        unique_tanks_volume = [v for i, v in enumerate(unique_tanks_volume) if i in stowCacheIndex]
        unique_tanks_number = [v for i, v in enumerate(unique_tanks_number) if i in stowCacheIndex]
        leftOverTanks = [v for i, v in enumerate(leftOverTanks) if i in stowCacheIndex]
        leftOverVolume = [v for i, v in enumerate(leftOverVolume) if i in stowCacheIndex]





        # Return a dictionary containing the results
        return {'alphanumeric assigned': [dP], 'stow': unique_tanks, 'remaining volume (tanks)': unique_tanks_volume,
                'remaining tanks (total)': unique_tanks_number, 'remaining tanks (leftover)': leftOverTanks,
                'remaining volume (total)': leftOverVolume}


# Nice way to make your code into an importable module.
# This will only run when being called as itself, i.e. 'python binPack.py'
# But not as 'import binPack' for use within another module or script.
# This style is good for including tests and example functionality.
if __name__ == '__main__':

    #                7001  7002  7003  7004  7005
    tanksVolValue = [626,   939, 1209, 1222,15]
    prodsVolValue = [10, 2000]
    # prodsVolSet = ['GqNAeWOF', 'ZMzQaj15']

    # Instatiate object with default params
    binpack = binPack()

    # # Calculate a pack with tVV, pVV
    # result = binpack.getPack(tanksVolValue, prodsVolValue)
    # print
    # 'Iteration 1: 5 results'
    # pprint(result)

    # Change the default params. Any can be changed in this way.
    binpack.numberOfResultsRequested = 1
    binpack.iterations = 100
    binpack.tankTrueOrVolumeFalse = False

    # Calculate a pack with tVV, pVV
    result = binpack.getPack(tanksVolValue, prodsVolValue)




    pprint(result)
