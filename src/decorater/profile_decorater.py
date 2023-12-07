"""
"""
import cProfile
from os import mkdir, path
import pstats
import sys


def profiler(func):
    """
    This function is able to profile a specific function in our code.
    Here we sort on the cumtime. because this is the most accurate time
    for us. This function will only be actived when using:
    python3 app.py --profile
    in the command line.
    :param func: this is a function where you want to use the
    profiler on
    :return: every function that has the profiler connected to it,
    will get a specific .prof file. In this file we can see the running
    time for every thing within this function
    """
    def inner(*args, **kwargs):

        # if there are 2 or more command line arg, and one is --profile
        if len(sys.argv) > 1 and "--profile" in sys.argv:
            # cprofile is called
            c_profiler = cProfile.Profile()
            c_profiler.enable()
            result = func(*args, **kwargs)
            c_profiler.disable()

            # profile data will be sorted on most cumtime
            stats = pstats.Stats(c_profiler).strip_dirs().sort_stats('cumtime')

            # get the function and function file
            function_name = func.__name__
            function_file_name = path.basename(func.__globals__['__file__'])

            # make the cprofiling folder when not existing
            if not path.exists("cprofiling"):
                mkdir("cprofiling")

            # put the profile data in a file with the function name
            stats.dump_stats(path.join("cprofiling", f"{function_file_name}-{function_name}.prof"))

            return result

        return func(*args, **kwargs)
    return inner
