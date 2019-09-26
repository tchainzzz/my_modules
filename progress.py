import time
import sys

class ProgressTracker():
    def __init__(self, iterable):
        self.iteration_length = len(iterable)
        self.current_iteration = 0

    def register(self, iterable):
        self.iteration_length = len(iterable)

    def start(self):
        self.start = time.time()

    def iteration_done(self):
        self.current_iteration += 1
        if self.current_iteration == self.iteration_length:
            sys.stdout.write("\n")

    def skip_iter(self, inner_loop_sizes):
        if isinstance(inner_loop_sizes, int):
            self.current_iteration += inner_loop_sizes
        elif isinstance(inner_loop_sizes, list):
            self.current_iteration += reduce((lambda x, y: x*y), inner_loop_sizes)
        else:
            raise TypeError("TypeError: expected 'inner_loop_sizes' to be an int or a list but got {}".format(type(inner_loop_sizes)))

    def report(self, message, precision=4):
        message = message.strip()
        if message[-1] is ":":
            message = message[:-1]
        precision_format_string = "{:0." + str(precision) + "f}"
        i = self.current_iteration
        eta = (self.iteration_length-(i+1)) / ((i+1)/(time.time() - self.start))
        hour_indicator = "{:02d}:" if int(eta) > 60 * 60 else "{}"
        printout_format_string = "\r{}: ({}/{}), {:." + str(precision+2) + "s}/s, ETA: " + hour_indicator + "{:02d}:{:02d}"
        sys.stdout.write(printout_format_string.format(
            message,  
            i+1, 
            self.iteration_length, 
            precision_format_string.format((i+1)/(time.time() - self.start)), # iterations per second
            int(eta // 60) // 60, # hours indicator
            int(eta // 60) % 60, # minutes indicator
            int(eta) % 60)) # seconds indicator
