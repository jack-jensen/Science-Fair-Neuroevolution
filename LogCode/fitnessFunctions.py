# This little file contains the functions that determine the genomes fitness.

# This function finds the automation's distance from the y-global on a coordinate plane.
# This is something that I am attempting to reduce.
def distanceFromYGlobal(x1, x2):
    return abs((x1 + x2) / 2)

# This function finds how straight the automation is.
# It does this by finding the absolute value of the slope of the line that the automation is on 
# (Euclid's first postulate: Through any 2 points there is a line).
# This is something I am attempting to reduce.
def differenceFromStraight(x1, y1, x2, y2):
    try:
        return abs((y2 - y1) / (x2 - x1))
    except ZeroDivisionError:
        return 50

# This function finds the automation's distance from the x-global on a coordinate plane.
# This is something that I am attempting to increase.
def distanceFromXGlobal(y1, y2):
    return abs((y1 + y2) / 2)