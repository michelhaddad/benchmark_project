from time import *
from numpy import *
import numpy as np
import xml.sax



def copy_matrix(dim, vectorized = False):

    if (vectorized):

        # Vectorized Copy
        # ----------------
        a = random.rand(dim, dim, 3)

        start = clock()
        a[:, :, 0] = a[:, :, 1]
        a[:, :, 2] = a[:, :, 0]
        a[:, :, 1] = a[:, :, 2]

        finish = clock()
        print('Time for vectorized copy: ', finish - start, 's')

    else:

        # Copy with loop
        # ----------------
        a = random.rand(dim, dim, 3)

        start = clock()
        for i in range(dim):
            for j in range(dim):
                a[i, j, 0] = a[i, j, 1]
                a[i, j, 2] = a[i, j, 0]
                a[i, j, 1] = a[i, j, 2]

        finish = clock()
        print('Time for copy with loops: ', finish - start, 's')


def mat_mult(dim1, dim2, dim3):

    a = random.rand(dim1, dim2)
    b = random.rand(dim2, dim3)

    start = clock()

    c = dot(a, b)

    finish = clock()
    print('Time for', 'c'+str(shape(c)), '=', 'a'+str(shape(a)), 'b'+str(shape(b)), 'is', finish - start, 's')


def n_queens():
    # Python program to solve N Queen
    # Problem using backtracking

    global N
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
                if solve_nq_util(board, col + 1) == True:
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
        board = [[0]*5000]*5000

        if solve_nq_util(board, 0) == False:
            return False

        return True


    # driver program to test above function

    start = clock()

    solve_nq()

    finish = clock()

    print('Time to solve the N Queen problem is', finish - start, 's')


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
        def end_element(self, tag):
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


    start = clock()

    parser.parse("movies.xml")

    finish = clock()

    print('Time to parse the movies.xml file is', finish - start, 's')



if __name__ == "__main__":

    #   ./functions.py

    copy_matrix(1000)
    print('\n')
    copy_matrix(5000, True)
    print('\n')
    # mat_mult(1000, 1000, 1000)
    print('\n')
    # n_queens()
    print('\n')
    xml_parsing()

