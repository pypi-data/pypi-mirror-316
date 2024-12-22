class Matrix:
    """
    Simple matrix class

    :param matrix: 2D list representing a matrix
    :type matrix: list
    :param validate: Validate the 2D list passed in as matrix (defaults to True)
    :type validate: bool, optional
    :ivar rows: Number of rows in the matrix
    :type rows: int
    :ivar columns: Number of columns in matrix
    :type columns: int
    """

    def __init__(self, matrix, validate=True):
        """
        Matrix Constructor
        """

        if validate:
            self.validate(matrix)

        self.matrix = matrix
        self.rows = len(matrix)
        self.columns = len(matrix[0])


    @staticmethod
    def validate(matrix):
        """
        Validates if the 2D list passed into the constructor is a valid matrix

        :param matrix:
        :type matrix: 2D list
        :raises TypeError: If matrix parameter is not a 2D list
        :raises ValueError: If all rows are not the same length
        :return: Returns True if validations passed else raises an exception
        :rtype: bool
        """

        if type(matrix) != list:
            raise TypeError(f'Expected matrix to be of type {list}. Received {type(matrix)}')

        column_length = None

        for row in matrix:
            if type(row) != list:
                raise TypeError(f'Expected matrix row to be of type {list}. Received {type(row)}')

            if column_length is None:
                column_length = len(row)

            if len(row) != column_length:
                raise ValueError(f'Matrix rows are not the same length. {len(row)} != {column_length}')

    @staticmethod
    def zero(size, dtype=float):
        """
        Creates a matrix of dtype zeros using the dimensions specified in size

        :param size: Tuple container the row end column length e.g. (row, column)
        :type size: tuple
        :param dtype: data type of the matrix elements (defaults to Float)
        :type dtype: type, optional
        :raises TypeError: If size is not a tuple of ints
        :return: A 2D matrix of zeros of type dtype with the dimensions defined in the size tuple
        """

        if type(size) != tuple:
            raise TypeError(f'Expected {tuple} of (rows, columns). Received {type(size)}')

        if type(size[0]) != int or type(size[1]) != int:
            raise TypeError(f'Expected {tuple} of ({int}, {int}). Received {type(size[0]), type(size[1])}')

        return Matrix([ [dtype(0)] * size[1] for _ in range(size[0])])

    def transpose(self):
        """
        Returns the transpose of the current matrix

        :return: Transpose of current matrix
        :rtype Matrix
        """

        transposed_matrix = self.zero((self.columns, self.rows), dtype=int)

        for row in range(transposed_matrix.rows):
            for column in range(transposed_matrix.columns):
                transposed_matrix[row][column] = self.matrix[column][row]

        return transposed_matrix

    def __mul__(self, other):
        """
        Multiplies this matrix with another matrix.

        The method checks if the matrices are compatible for multiplication
        (i.e., the number of columns in the first matrix must be equal to
        the number of rows in the second matrix). If the matrices are compatible,
        it performs the multiplication and returns a new matrix.

        :param other: The matrix to multiply with.
        :type other: Matrix
        :raises TypeError: If the other operand is not of type Matrix.
        :raises ValueError: If the matrices have incompatible dimensions for multiplication.
        :return: A new Matrix instance representing the product of the two matrices.
        :rtype: Matrix
        """

        if type(other) != type(self):
            raise TypeError(f'Cannot multiply {type(Matrix)} with {type(other)}')

        if self.columns != other.rows:
            raise ValueError(f'Cannot multiply matrix[{self.rows}][{self.columns}] by matrix[{other.rows}][{other.columns}]')

        new_matrix = self.zero((self.rows, other.columns), dtype=type(self.matrix[0][0]))

        for row in range(self.rows):
            for column in range(other.columns):
                for i in range(self.columns):
                    new_matrix[row][column] += self.matrix[row][i] * other.matrix[i][column]

        return new_matrix

    def __getitem__(self, index):
        """
        Returns the element in the matrix based on the index.

        :param index: index of the element you want to access
        :return: The row at the specified index of the element in [row][column] if chained together
        :rtype: list, type
        """

        if type(index) != int:
            raise TypeError(f'matrix[{type(index)}] is not a valid index. Expected matrix[{int}]')

        return self.matrix[index]

    def __str__(self):
        """
        Returns a string of the values and visualization of the matrix dimensions by creating
        a string of each row in the matrix seperated by a new line.

        :return: a string of each row in the matrix seperated by a new line
        :rtype: str
        """

        string = ''

        for row in self.matrix:
            string += str(row) + '\n'

        return string
