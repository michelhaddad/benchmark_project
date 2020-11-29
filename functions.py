from time import *
import numpy as np
import xml.sax
import simpy
import random
import time
from skimage.filters import gaussian
from moviepy.editor import VideoFileClip

# Set the seed to apply same operations on all tests
np.random.seed(10)


def copy_matrix(dim, vectorized=False):
    if vectorized:

        # Vectorized Copy

        a = np.random.rand(dim, dim, 3)

        start = time.time()
        a[:, :, 0] = a[:, :, 1]
        a[:, :, 2] = a[:, :, 0]
        a[:, :, 1] = a[:, :, 2]

        finish = time.time()
        print('Time for vectorized copy: ', finish - start, 's')
        return finish - start

    else:

        # Copy with loop

        a = np.random.rand(dim, dim, 3)

        start = time.time()
        for i in range(dim):
            for j in range(dim):
                a[i, j, 0] = a[i, j, 1]
                a[i, j, 2] = a[i, j, 0]
                a[i, j, 1] = a[i, j, 2]

        finish = time.time()
        print('Time for copy with loops: ', finish - start, 's')
        return finish - start


def mat_mult(dim1, dim2, dim3):
    a = np.random.rand(dim1, dim2)
    b = np.random.rand(dim2, dim3)

    start = time.time()

    c = np.dot(a, b)

    finish = time.time()
    print('Time to calculate', 'c' + str(np.shape(c)), '=', 'a' + str(np.shape(a)), '*', 'b' + str(np.shape(b)), 'is',
          finish - start, 's')
    return finish - start


def n_queens():
    N = 5000

    # A utility function to check if a queen can
    # be placed on board[row][col]. Note that this
    # function is called when "col" queens are
    # already placed in columns from 0 to col -1.
    # So we need to check only left side for
    # attacking queens
    def is_safe(board, row, col):

        # Check this row on left side
        for i in range(col):
            if board[row][i] == 1:
                return False

        # Check upper diagonal on left side
        for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
            if board[i][j] == 1:
                return False

        # Check lower diagonal on left side
        for i, j in zip(range(row, N, 1), range(col, -1, -1)):
            if board[i][j] == 1:
                return False

        return True

    def solve_nq_util(board, col):
        # base case: If all queens are placed
        # then return true
        if col >= N:
            return True

        # Consider this column and try placing
        # this queen in all rows one by one
        for i in range(N):

            if is_safe(board, i, col):
                # Place this queen in board[i][col]
                board[i][col] = 1

                # recur to place rest of the queens
                if solve_nq_util(board, col + 1):
                    return True

                # If placing queen in board[i][col
                # doesn't lead to a solution, then
                # queen from board[i][col]
                board[i][col] = 0

        # if the queen can not be placed in any row in
        # this colum col then return false
        return False

    # This function solves the N Queen problem using
    # Backtracking. It mainly uses solve_nq_util() to
    # solve the problem. It returns false if queens
    # cannot be placed, otherwise return true and
    # placement of queens in the form of 1s.
    # note that there may be more than one
    # solutions, this function prints one of the
    # feasible solutions.
    def solve_nq():
        board = [[0] * 5000] * 5000

        if not solve_nq_util(board, 0):
            return False

        return True

    # driver program to test above function

    start = time.time()

    solve_nq()

    finish = time.time()

    print('Time to solve the N Queen problem is', finish - start, 's')
    return finish - start


def xml_parsing():
    class MovieHandler(xml.sax.ContentHandler):
        def __init__(self):
            self.CurrentData = ""
            self.type = ""
            self.format = ""
            self.year = ""
            self.rating = ""
            self.stars = ""
            self.description = ""

        # Call when an element starts
        def start_element(self, tag, attributes):
            self.CurrentData = tag
            if tag == "movie":
                print("*****Movie*****")
                title = attributes["title"]
                print("Title:", title)

        # Call when an elements ends
        def end_element(self):
            if self.CurrentData == "type":
                print("Type:", self.type)
            elif self.CurrentData == "format":
                print("Format:", self.format)
            elif self.CurrentData == "year":
                print("Year:", self.year)
            elif self.CurrentData == "rating":
                print("Rating:", self.rating)
            elif self.CurrentData == "stars":
                print("Stars:", self.stars)
            elif self.CurrentData == "description":
                print("Description:", self.description)
            self.CurrentData = ""

        # Call when a character is read
        def characters(self, content):
            if self.CurrentData == "type":
                self.type = content
            elif self.CurrentData == "format":
                self.format = content
            elif self.CurrentData == "year":
                self.year = content
            elif self.CurrentData == "rating":
                self.rating = content
            elif self.CurrentData == "stars":
                self.stars = content
            elif self.CurrentData == "description":
                self.description = content

    parser = xml.sax.make_parser()

    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    # override the default ContextHandler
    Handler = MovieHandler()
    parser.setContentHandler(Handler)

    start = time.time()

    for i in range(100):
        parser.parse("movies.xml")

    finish = time.time()

    print('Time to parse the movies.xml file is', finish - start, 's')
    return finish - start


def bank_simulation():
    RANDOM_SEED = 42
    NEW_CUSTOMERS = 300000  # Total number of customers
    INTERVAL_CUSTOMERS = 10.0  # Generate new customers roughly every x seconds
    MIN_PATIENCE = 60  # Min. customer patience
    MAX_PATIENCE = 300  # Max. customer patience

    def source(env, number, interval, counter):
        """Source generates customers randomly"""
        for i in range(number):
            c = customer(env, 'Customer%02d' % i, counter, time_in_bank=12.0)
            env.process(c)
            t = random.expovariate(1.0 / interval)
            yield env.timeout(t)

    def customer(env, name, counter, time_in_bank):
        """Customer arrives, is served and leaves."""
        arrive = env.now
        # print('%7.4f %s: Here I am' % (arrive, name))

        with counter.request() as req:
            patience = random.uniform(MIN_PATIENCE, MAX_PATIENCE)
            # Wait for the counter or abort at the end of our tether
            results = yield req | env.timeout(patience)

            wait = env.now - arrive

            if req in results:
                # We got to the counter
                # print('%7.4f %s: Waited %6.3f' % (env.now, name, wait))

                tib = random.expovariate(1.0 / time_in_bank)
                yield env.timeout(tib)
                # print('%7.4f %s: Finished' % (env.now, name))

            else:
                pass
                # We reneged
                # print('%7.4f %s: RENEGED after %6.3f' % (env.now, name, wait))

    # Setup and start the simulation
    random.seed(RANDOM_SEED)
    env = simpy.Environment()

    # Start processes and run
    counter = simpy.Resource(env, capacity=1)
    env.process(source(env, NEW_CUSTOMERS, INTERVAL_CUSTOMERS, counter))
    start = time.time()
    env.run()
    finish = time.time()

    print('Time to run the Bank Simulation is', finish - start, 's')
    return finish - start


def blurr_video():
    def blur(image):
        """ Returns a blurred version of the image """
        return gaussian(image.astype(float), sigma=2)

    start = time.time()
    clip = VideoFileClip("wee.mp4")
    clip_blurred = clip.fl_image(blur)
    clip_blurred.write_videofile("blurred_weeee.mp4", temp_audiofile="")
    finish = time.time()
    print('Time to blur the video is', finish - start, 's')
    return finish - start


def get_ordered_runtimes():
    function_run_times = [copy_matrix(1000), copy_matrix(5000, True), mat_mult(5000, 5000, 5000), n_queens(),
                          xml_parsing(), bank_simulation(), blurr_video()]
    for i in range(len(function_run_times)):
        function_run_times[i] = round(function_run_times[i], 5)
    return function_run_times
