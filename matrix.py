# -*- coding:Utf-8 -*
##
## EPITECH PROJECT, 2019
## 102architect_2019
## File description:
## matrice.py
##

class Matrix:

    def __new__(cls, lines, columns):
        if lines <= 0 or columns <= 0:
            raise ValueError("Dimensions not valid")
        return object.__new__(cls)

    def __init__(self, lines, columns):
        self.lines = lines
        self.columns = columns
        self.mat = {}
        for i in range(1, lines + 1):
            for j in range(1, columns + 1):
                self.mat[i, j] = 0

    @classmethod
    def from_2d_list(cls, list_2d):
        total_columns = 0
        for line in list_2d:
            c = len(line)
            if total_columns == 0:
                total_columns = c
            elif c != total_columns:
                raise ValueError("Columns don't have the same length")
        m = cls(len(list_2d), total_columns)
        for i, j in m.coords():
            m[i, j] = list_2d[i - 1][j - 1]
        return m

    @classmethod
    def identity(cls, n):
        m = cls(n, n)
        for i in range(1, n + 1):
            m[i, i] = 1
        return m

    def copy(self):
        l = self.lines + 1
        c = self.columns + 1
        return Matrix.from_2d_list([[self.mat[i, j] for j in range(1, c)] for i in range(1, l)])

    def __repr__(self):
        matrix_str = ""
        for i, j in self.mat:
            value = round(self.mat[i, j], 3)
            if value == 0:
                value = 0
            matrix_str += str(value)
            matrix_str += "\t" if (j < self.columns) else "\n"
        return matrix_str[:-1]

    def __str__(self):
        return repr(self)

    def __getitem__(self, coord):
        if coord in self.mat.keys():
            return self.mat[coord]
        raise KeyError("Coords not found")

    def __setitem__(self, coord, valeur):
        if coord in self.mat.keys():
            self.mat[coord] = valeur
        else:
            raise KeyError("Coords not found")

    def __delitem__(self, coord):
        if coord in self.mat.keys():
            self.mat[coord] = 0
        else:
            raise KeyError("Coords not found")

    def __add__(self, matrix_added):
        if not isinstance(matrix_added, Matrix):
            raise TypeError("Cannot matrix and {}".format(type(matrix_added)))
        if (self.lines != matrix_added.lines) or (self.columns != matrix_added.columns):
            raise ValueError("Matrix don't have the same dimensions")
        new_matrix = Matrix(self.lines, self.columns)
        for coord in self.mat:
            new_matrix[coord] = self.mat[coord] + matrix_added[coord]
        return new_matrix

    def __iadd__(self, matrix_added):
        new_matrix = self + matrix_added
        self.mat = dict(new_matrix.mat)
        return self

    def __mul__(self, value):
        if isinstance(value, (int, float)):
            return self.multiplicate_by_constante(value)
        if not isinstance(value, Matrix):
            raise TypeError("Cannot multiplicate matrix and {}".format(type(value)))
        matrix_mul = value
        if self.columns != matrix_mul.lines:
            error = "Can't multiplicate {0}x{1} matrix with {2}x{3} matrix ({1} != {2})"
            error = error.format(self.lines, self.columns, matrix_mul.lines, matrix_mul.columns)
            raise ValueError(error)
        new_matrix = Matrix(self.lines, matrix_mul.columns)
        for n, p in new_matrix.coords():
            for i, j in zip(range(1, matrix_mul.lines + 1), range(1, self.columns + 1)):
                new_matrix[n, p] += matrix_mul[i, p] * self.mat[n, j]
        return new_matrix

    def __rmul__(self, value):
        if isinstance(value, (int, float)):
            return self.multiplicate_by_constante(value)
        raise TypeError("Cannot multiplicate {} and matrix".format(type(value)))

    def __imul__(self, value):
        new_matrix = self * value
        self.mat = dict(new_matrix.mat)
        return self

    def multiplicate_by_constante(self, k):
        new_matrix = Matrix(self.lines, self.columns)
        for coord in self.mat:
            new_matrix[coord] = self.mat[coord] * k
        return new_matrix

    def transposition(self):
        new_matrix = Matrix(self.columns, self.lines)
        for i, j in self.mat:
            new_matrix[j, i] = self.mat[i, j]
        return new_matrix

    def get_comatrix(self, i, j):
        comatrix = [
            [self.mat[m, n] for n in range(1, self.columns + 1) if n != j] \
            for m in range(1, self.lines + 1) if m != i
        ]
        return Matrix.from_2d_list(comatrix)

    @property
    def determinant(self):
        if self.lines != self.columns:
            raise ValueError(f"I can't have the determinant of {self.lines}x{self.columns} !")
        if self.lines == 1:
            return self[1, 1]
        if self.lines == 2:
            return (self.mat[1, 1] * self.mat[2, 2]) - (self.mat[2, 1] * self.mat[1, 2])
        mat = self.copy()
        determinant = 1
        n = self.lines + 1
        for j in range(1, n - 1):
            k = j
            coeff_max = 0
            for i in range(j + 1, n):
                if abs(coeff_max) < abs(mat[i, j]):
                    k = i
                    coeff_max = mat[i, j]
            if coeff_max == 0:
                determinant = 0
                break
            if k != j:
                for i in range(j, n):
                    mat[j, i], mat[k, i] = mat[k, i], mat[j, i]
                determinant *= -1
            determinant *= coeff_max
            for k in range(j + 1, n):
                coeff = mat[k, j] / coeff_max
                for i in range(1, n):
                    mat[k, i] -= (coeff * mat[j, i])
        determinant *= mat[n - 1, n - 1]
        return determinant

    def invert(self):
        det_mat = self.determinant
        if det_mat == 0:
            raise ValueError("Determinant is null, can't invert matrix")
        if self.lines == 1:
            return Matrix.from_2d_list([[1 / self.mat[1, 1]]])
        new_matrix = Matrix(self.lines, self.columns)
        for i, j in new_matrix.coords():
            new_matrix[i, j] = pow(-1, i + j) * self.get_comatrix(i, j).determinant
        return (1 / det_mat) * new_matrix.transposition()

    def coords(self):
        return self.mat.keys()

    def values(self):
        return self.mat.values()

    def reset(self):
        for coord in self.mat:
            self.mat[coord] = 0
