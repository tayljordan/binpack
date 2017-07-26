# binPack

Enter your project goal and description here, as well as a short blip on how to use it if others wish

	EXAMPLE:

	tanksVolValue   = [626, 639, 1209]
	prodsVolValue = [10,2000,30, 500, 1000, 2000]

	# Instatiate object with default params
	binpack = binPack.binPack()

	# Change the default params. Any can be changed in this way.
	binpack.numberOfResultsRequested = 2

	# Calculate a pack with tVV, pVV
	result = binpack.getPack(tanksVolValue, prodsVolValue)
	pprint(result)

Enter script dependencies

	Python 3.4, all dependencies included in standard library
