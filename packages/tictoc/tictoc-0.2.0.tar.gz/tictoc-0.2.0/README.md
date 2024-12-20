# Fast, simple and accurate Python timing. Written in Rust.

![badge](https://img.shields.io/pypi/dm/tictoc)

## Installation
Install with [pip](https://pypi.org/project/pip).
```bash
$ python -m pip install tictoc
```

## Usage
Import. 
```python
from tictoc import tic,toc
```
Begin timing with `tic()`, and stop with `toc()`.
```python
tic()
# some code
toc()
```
A call to `tic()` can be followed with multiple `toc()` calls. Each will print the time elapsed since the most recent `tic()` call.
```python
tic()
time.sleep(3)
toc()
# >>> The elapsed time was 3.000132333 seconds.
time.sleep(3)
toc()
# >>> The elapsed time was 6.000383124 seconds.
```
For more complex timing operations, you can assign the output of `tic()` and pass it as an input to `toc()`.
> [!NOTE]
> This syntax cannot be used interchangeably with the default syntax above. Any call to `tic()` resets the global timer.
```python
firstTic = tic()
time.sleep(3)
secondTic = tic()
time.sleep(1)
toc(firstTic)
# >>> The elapsed time was 4.000317251 seconds.
time.sleep(3)
toc(secondTic)
# >>> The elapsed time was 4.000312568 seconds.
```
Any call to `toc()` will print the elapsed time in seconds. You can save the results with full precision by assigning the output of `toc()`.
```python
tic()
# some code
results = toc()
```
The available units are:
```python
results.nanos   # u128
results.micros  # u128
results.millis  # u128
results.seconds # f64
```

## Full example
```python
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
``` 
