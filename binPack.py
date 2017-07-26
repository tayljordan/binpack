import itertools
import time
import random
from copy import deepcopy
import math
import string
from pprint import pprint


# Define the binPack class
class binPack(object):
    # Write the constructor so that the object is initialized with some default constants
    # These can be changed after instantiation
    def __init__(self, factor=.05, iterations=10000, maximumTimeAllowedInSeconds=10,
                 numberOfResultsRequested=5, tankTrueOrVolumeFalse=False):

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
        allTankVolAvail = sorted(allTankVolAvail, reverse=True)

        # The next two iterations will determine length of
        # Combinations i.e. (1,2) where L = 2, vs. (2,3,4) where L = 3, vs (4,5,6,7) where L = 4, etc.

        # Number of combinations to BEGIN with. represents at least one sampling index, in this case 1
        r0 = 1
        while True:
            x = sum(allTankVolAvail[r0:]) - oneProductVolume
            print(x)
            print('r0', r0)
            if x >= 0:
                break

            else:
                r0 += 1

            if r0 > 20:
                return IndexError

        # Number of combinations to END with. represents at least one sampling index, in this case 1
        r1 = 1
        while True:
            # Sum of first, second, third index of sum(sorted) tank values is subtracted from cargo element (say, 500m3)
            x = oneProductVolume - sum(allTankVolAvail[r1:])
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
                r = int(tC[2])

            else:
                # Obtains a list if tank combination candidates, for small volumes
                tC = self.__scSmallVolume(tV)
                r = 2

            # Get the values and indexes from scLargeVolume and scSmallVolume
            t0 = tC[0];
            e0 = tC[1]
            # Get list with values equal to or greater than element volume
            mV = [i for i in t0 if i >= element]
            # Pare down the index list (e0) to match the volume list
            e0 = e0[(len(e0) - len(mV)):]
            iR = random.randint(0, r);
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

        tR = 1;
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
                    unique_tanks.append([a, prodsVolKey])
                    unique_tanks_volume.append(sum(tVV))
                    unique_tanks_number.append(len(tanksVolName))
                    leftOverTanks.append(tanksVolName)
                    leftOverVolume.append(tVV)

            except (IndexError, TypeError):
                pass

            # Track the number of iterations as well as the time the iterations have elapsed for.
            # Use these to timeout if computation takes too long.
            tR += 1
            t1 = time.time()
            timeNow = t1 - t0

            numberOfUniqueTanks = len(unique_tanks)

            # Trigger timeout
            if (tR >= self.iterations) or (timeNow >= self.maximumTimeAllowedInSeconds) \
                    or (numberOfUniqueTanks >= self.numberOfResultsRequested):
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

        # Return a dictionary containing the results
        return {'alphanumeric assigned': [dP], 'stow': unique_tanks, 'remaining volume (tanks)': unique_tanks_volume,
                'remaining tanks (total)': unique_tanks_number, 'remaining tanks (leftover)': leftOverTanks,
                'remaining volume (total)': leftOverVolume}


# Nice way to make your code into an importable module.
# This will only run when being called as itself, i.e. 'python binPack.py'
# But not as 'import binPack' for use within another module or script.
# This style is good for including tests and example functionality.
# if __name__ == '__main__':
#     tanksVolValue = [626, 639, 1209, 1222]
#     prodsVolValue = [10, 900, 60]
#
#     # Instatiate object with default params
#     binpack = binPack()
#
#     # Change the default params. Any can be changed in this way.
#     binpack.numberOfResultsRequested = 2
#
#
#     # Calculate a pack with tVV, pVV
#     result = binpack.getPack(tanksVolValue, prodsVolValue)
#     print
#     'Iteration 1: 5 results'
#     pprint(result)
#
#     # Change the default params. Any can be changed in this way.
#     # binpack.numberOfResultsRequested = 1
#
#     # # Calculate a pack with tVV, pVV
#     # result = binpack.getPack(tanksVolValue, prodsVolValue)
#     # print
#     # 'Iteration 1: 1 result'
#     # pprint(result)
