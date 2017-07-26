# binPack

binPack 

	Combinatorially optimizes volumes into containers, from most optimal to least optimal.
	Can be used as a base for rectifying adjacency issues in technical applications, 
	such as chemical tanker stowage. 

Usage

	EXAMPLE:

	tanksVolValue   = [626, 639, 1209]
	prodsVolValue = [10,2000,30, 500, 1000, 2000]

	# Instatiate object with default params
	binpack = binPack.binPack()
	
	# Number of outcomes requested
	binpack.numberOfResultsRequested = 2

	# Time allowed to find outcome, default = 10 seconds
        binpack.maximumTimeAllowedInSeconds = 10

	# Whether optimizes based on maximum tankage or maximum volume, default is False
	binpack.tankTrueOrVolumeFalse = False

	# Calculate a pack with tVV, pVV
	result = binpack.getPack(tanksVolValue, prodsVolValue)
	pprint(result)

Enter script dependencies

	Python 3.4, all dependencies included in standard library
