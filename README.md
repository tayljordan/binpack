Summary

Used for placing different size liquids into different sized containers. This question may seem simplistic however it is a classically difficult problem to solve.

In:

    Tank volumes

    Product volumes

Out:

    Possible stowage combinations

Calling the API

Arguments:

    tanksVolValue = [20, 20, 10, 5]

    prodsVolValue = [20, 25]

Tuning arguments:

    s = 3

    r = 1

    Depth = 10

    Processes = 1


Result:

Considering tuning arguments above there are 18 total combinations expressed as a list. Each element in the list contains a variation of the following:

[[20, 25], [7003], {'7003': 10}, [[7002], [7004, 7001]]


Breakdown:

[20, 25] = The product volumes, sorted

[7003] = Remaining tank that is empty and available. The 700 in '700X' has no meaning, it was an identification holdover from early development.

{'7003' : 10} = remaining empty tank(s) and their volumes

[[7002], [7004, 7001]] = The stow. i.e. the first product 20 will fit into the second tank and the second product will fit into the first and last tank.

If given,

7001 = 30

7002 = 20

7003 = 10

7004 = 5

then the first volume (20) will be stowed in 7002 and the second volume (25) will be stowed in 7004 and 7001. 7003 is an available tank.

Limitations

API is limited 20 tanks until the tuning arguments can be definitively implemented. Outcomes are not exhaustive. Additional work will be necessary to unpack additional outcomes and expand the allowable number of tanks and products.
