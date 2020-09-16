# File: matrix.py
# Author: Dylan Lebedin
# Date: 4/4/2020
# Email: djl3416@rit.edu
# Description: This file shows the proper implementation of a matrix class.

import math
from math import sqrt
import numbers

def zeroes(height, width):
        """
        Creates a matrix of zeroes.
        """
        g = [[0.0 for _ in range(width)] for __ in range(height)]
        return Matrix(g)

def identity(n):
        """
        Creates a n x n identity matrix.
        """
        I = zeroes(n, n)
        for i in range(n):
            I.g[i][i] = 1.0
        return I
    
def dot_product(v1, v2):
    """
    Calculates the dot product between two vectors
    """
    if len(v1) != len(v2):
        print("error! Vectors must have same length")
        
    result = 0
    for i in range(len(v1)):
        value_1 = v1[i]
        value_2 = v2[i]
        result += value_1 * value_2
        
    return result

def get_row(matrix, row):
    """
    Grabs the specific row of the matrix
    """
    return matrix[row]

def get_column(matrix, column_number):
    """ 
    Grabs the specific column of the matrix
    """
    column = []
    for r in range(len(matrix)):
        column.append(matrix[r][column_number])
        
    return column

class Matrix(object):

    # Constructor
    def __init__(self, grid):
        self.g = grid # matrix
        self.h = len(grid) # number of rows
        self.w = len(grid[0]) # number columns

    #
    # Primary matrix math methods
    #############################
 
    def determinant(self):
        """
        Calculates the determinant of a 1x1 or 2x2 matrix.
        """
        if not self.is_square():
            raise(ValueError, "Cannot calculate determinant of non-square matrix.")
        if self.h > 2:
            raise(NotImplementedError, "Calculating determinant not implemented for matrices largerer than 2x2.")
        
        # if 1x1 matrix return only element as determinant
        if self.h == 1:
            return self.g[0][0]
        # if 2x2 matrix return ad-bc as determinant
        elif self.h == 2:
            return (self.g[0][0] * self.g[1][1]) - (self.g[0][1] * self.g[1][0]) 

    def trace(self):
        """
        Calculates the trace of a matrix (sum of diagonal entries).
        """
        if not self.is_square():
            raise(ValueError, "Cannot calculate the trace of a non-square matrix.")

        #initialize the result variable
        result = 0
        for r in range (self.h):
            for c in range (self.w):
                if r == c:
                    # add the matrix values where the row and column values are the same
                    result += self.g[r][c] 
        #return result
        return result

    def inverse(self):
        """
        Calculates the inverse of a 1x1 or 2x2 Matrix.
        """
        if not self.is_square():
            raise(ValueError, "Non-square Matrix does not have an inverse.")
        if self.h > 2:
            raise(NotImplementedError, "inversion not implemented for matrices larger than 2x2.")

        inverse = []
        
        if self.h == 1:
            inverse.append([1/ self.g[0][0]])
        elif self.h == 2:
            # if the matrix is 2x2, check if the matrix is invertible
            if self.g[0][0] * self.g[1][1] == self.g[0][1] * self.g[1][0]:
                raise(ValueError, "Matrix is not invertible.")
            else:
                # Calculate the inverse of the square 1x1 or 2x2 matrix
                a = self.g[0][0]
                b = self.g[0][1]
                c = self.g[1][0]
                d = self.g[1][1]
                
                factor = self.determinant()
                
                inverse = [[d, -b], [-c, a]]
                
                for i in range(self.h):
                    for j in range(self.w):
                        inverse[i][j] = (1/factor) * inverse[i][j]
        return Matrix(inverse)

    def T(self):
        """
        Returns a transposed copy of this Matrix.
        """
        matrix_transpose = []
        # loop through columns on outside loop
        for c in range (self.w):
            new_row = []
            # loop through columns on inner loop
            for r in range(self.h):
                # column values will be filled by what were each row before
                new_row.append(self.g[r][c])
            matrix_transpose.append(new_row)
        
        return Matrix(matrix_transpose)

    def is_square(self):
        return self.h == self.w

    #
    # Begin Operator Overloading
    ############################
    def __getitem__(self,idx):
        """
        Defines the behavior of using square brackets [] on instances
        of this class.

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > my_matrix[0]
          [1, 2]

        > my_matrix[0][0]
          1
        """
        return self.g[idx]

    def __repr__(self):
        """
        Defines the behavior of calling print on an instance of this class.
        """
        s = ""
        for row in self.g:
            s += " ".join(["{} ".format(x) for x in row])
            s += "\n"
        return s

    def __add__(self,other):
        """
        Defines the behavior of the + operator
        """
        if self.h != other.h or self.w != other.w:
            raise(ValueError, "Matrices can only be added if the dimensions are the same") 
            
        # initialize the matrix to hold the results
        matrixSum = []
        
        #matrix to hold a row for appending sums of each element
        row = []
        #For loop within a for loop to iterate over the matrices
        for r in range(self.h):
            row = [] #reset the list
            for c in range(self.w):
                row.append(self.g[r][c] + other.g[r][c]) #adding the matrices
            matrixSum.append(row)
            
        return Matrix(matrixSum)            

    def __neg__(self):
        """
        Defines the behavior of - operator (NOT subtraction)

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > negative  = -my_matrix
        > print(negative)
          -1.0  -2.0
          -3.0  -4.0
        """
        
        # initialize matrix full of zeroes
        matrix_neg = zeroes(self.h, self.w)
        for i in range (self.h):
            for j in range (self.w):
                # fill empty matrix with negative values of self.g
                matrix_neg[i][j] = -1 * self.g[i][j]
                
        return matrix_neg

    def __sub__(self, other):
        """
        Defines the behavior of - operator (as subtraction)
        """
        if self.h != other.h or self.w != other.w:
            raise(ValueError, "Matrices can only be subtracted if the dimensions are the same")
        
        # initialize the matrix to hold the results
        matrixDiff = []
        
        #matrix to hold a row for appending differences of each element
        row = []
        #For loop within a for loop to iterate over the matrices
        for r in range(self.h):
            row = [] #reset the list
            for c in range(self.w):
                row.append(self.g[r][c] - other.g[r][c]) #subtracting the matrices
            matrixDiff.append(row)
            
        return Matrix(matrixDiff)

    def __mul__(self, other):
        """
        Defines the behavior of * operator (matrix multiplication)
        """
        # Check to see if the matrices are of m x n and n x p dimensions
        if self.w != other.h:
            raise(ValueError, "Matrices can only be multiplied if the number of columns in the first matrix \
            and the number of rows in the second matrix are equal")
            
        # create an empty matrix of size m x p
        product = zeroes(self.h, other.w)
        for i in range(product.h):
            for j in range(product.w):
                product[i][j] = sum([self[i][k] * other[k][j] for k in range (self.w)])
        return product

    def __rmul__(self, other):
        """
        Called when the thing on the left of the * is not a matrix.

        Example:

        > identity = Matrix([ [1,0], [0,1] ])
        > doubled  = 2 * identity
        > print(doubled)
          2.0  0.0
          0.0  2.0
        """
        if isinstance(other, numbers.Number):
            pass
            
            matrix_one = []
            for i in range (self.h):
                row = []
                for j in range (self.w):
                    # fill empty matrix with scaled values of self.g
                    row.append(other * self[i][j])
                matrix_one.append(row)
            return Matrix(matrix_one)
            