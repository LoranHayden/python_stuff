def doit1():
    import string
    string.lower('Python')

import string
def doit2():
    string.lower('Python')

import timeit
t = timeit.Timer(setup='from __main__ import doit1', stmt='doit1()')
t.timeit()
#11.479144930839539
t = timeit.Timer(setup='from __main__ import doit2', stmt='doit2()')
t.timeit()
#4.6661689281463623
