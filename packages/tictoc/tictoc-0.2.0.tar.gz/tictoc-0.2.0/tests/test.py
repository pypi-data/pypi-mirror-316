import pytest
from tictoc import tic,toc
import time
import math

class testFunctionality:
    def testBasic(self):
        tic()
        print("test")
        results = toc()
        assert results.seconds > 0

    def testMultipleGlobalCalls(self):
        tic()
        print("test")
        results = toc()
        print("test2")
        results2 = toc()

        assert results.seconds < results2.seconds

    def testMultipleCalls(self):
        first = tic()
        print("test")
        second = tic()
        print("test2")
        secondResult = toc(second).seconds
        firstResult = toc(first).seconds

        assert firstResult > secondResult


class testInvalid:
    def testNonTicInputForToc(self):
        with pytest.raises(Exception):
            tic()
            print("test")
            toc(1)

@pytest.mark.parametrize("sleepTime", [0.05, 0.5, 1])
class testAccuracy:
    @pytest.fixture(scope="class")
    def tol(self):
        return 0.0006

    def testSingleCall(self, sleepTime, tol):
        tic()
        time.sleep(sleepTime)
        results = toc()
        assert (results.seconds < sleepTime+tol)

    def testMultipleGlobalCalls(self, sleepTime, tol):
        tic()
        time.sleep(sleepTime)
        toc()
        time.sleep(sleepTime)
        results = toc()
        assert (results.seconds < (sleepTime * 2)+tol)

    def testMultipleCalls(self, sleepTime, tol):
        first = tic()
        time.sleep(sleepTime)
        second = tic()
        time.sleep(sleepTime)
        results2 = toc(second)
        results = toc(first)
        assert (results.seconds < (sleepTime * 2)+tol)
        assert (results2.seconds < sleepTime+tol)

class testConsistency:
    def testMicros(self):
        tic()
        print("test")
        results = toc()
        assert results.micros == (math.floor(results.nanos * pow(10, -3)))

    def testMillis(self):
        tic()
        print("test")
        results = toc()
        assert results.millis == (math.floor(results.nanos * pow(10, -6)))

    def testSeconds(self):
        tic()
        print("test")
        results = toc()
        assert results.seconds == round(
            (results.nanos * pow(10, -9)), 9
        )  # f64 vs u128, hence the round
