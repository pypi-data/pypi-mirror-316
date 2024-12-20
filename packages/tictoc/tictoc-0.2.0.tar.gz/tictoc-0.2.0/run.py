import time
from tictoc import tic,toc

tic()         # start timing
time.sleep(3) # sleep for 3 seconds
toc()         # stop timing
# >>> The elapsed time was 3.000132333 seconds.

firstTic = tic()
time.sleep(3)
secondTic = tic()
time.sleep(1)
toc(firstTic)
# >>> The elapsed time was 4.000317251 seconds.
time.sleep(3)
toc(secondTic)
# >>> The elapsed time was 4.000312568 seconds.

tic()
results = toc()
print(results.nanos)
# >>> 2825 
