import argparse
import numpy as np


def swap_rows(matrix, j1, j2):
    temp = matrix[j1].copy()
    matrix[j1] = matrix[j2]
    matrix[j2] = temp


def swap_columns(matrix, j1, j2):
    for i in range(len(matrix)):
        temp = matrix[i][j1]
        matrix[i][j1] = matrix[i][j2]
        matrix[i][j2] = temp


def signify_sys(matrix):
    """get rid of all 0 rows of the system, raises an exception if there is a contradiction"""
    res_matrix = []
    for row in matrix:
        if row[:-1].any():  # if the system row isn't all 0
            res_matrix.append(list(row))
        elif row[-1] != 0:  # all the system row is 0 and the constant != 0: contradiction
            raise AssertionError()
    return np.array(res_matrix)  # return the significant matrix of the system


def echelon_sys(matrix):
    # first part of the algorithm: upper triangular
    for j in range(len(matrix[0]) - 1):  # go through the columns
        if matrix[j][j] == 0.0:
            for k in range(j + 1, len(matrix)):  # go through the remaining column
                if matrix[k][j] != 0:  # there is a non-0 elem bellow
                    print(f"R{j + 1} <-> R{k + 1}")
                    swap_rows(matrix, j, k)
                    break
        if matrix[j][j] == 0.0:  # there were no non-0 elem bellow
            for k in range(j + 1, len(matrix[0]) - 1):  # go through the remaining row
                if matrix[j][k] != 0:  # there is a non-0 elem to the right
                    print(f"C{j + 1} <-> C{k + 1}")
                    swap_columns(matrix, j, k)
                    break
        if matrix[j][j] == 0.0:  # there were no non-0 elem bellow or to the right
            for k1 in range(j + 1, len(matrix[0]) - 1):  # go through the remaining row
                for k2 in range(j + 1, len(matrix)):  # go through the remaining column
                    if matrix[k2][k1] != 0:  # there is a non-0 elem
                        swap_columns(matrix, j, k1)
                        swap_rows(matrix, j, k2)
                        print(f"R{j + 1} <-> R{k2 + 1}")
                        print(f"C{j + 1} <-> C{k1 + 1}")
                        break
        if matrix[j][j] == 0.0:  # the rest of the matrix is all 0
            break
        elif matrix[j][j] != 1.0:
            print(f"{np.round(1 / matrix[j][j], 4)} * R{j + 1} -> R{j + 1}".replace(")", "").replace("(", "").replace(".0", ""))
            matrix[j] = matrix[j] / matrix[j][j]
        for i in range(j + 1, len(matrix)):  # go through the rows downwards
            if matrix[i][j] == 0.0:
                continue
            print(f"-{np.round(matrix[i][j])} * R{j + 1} + R{i + 1} -> R{i + 1}".replace(")", "").replace("(", "").replace(".0", "").replace("--", ""))
            matrix[i] = matrix[i] - matrix[i][j] * matrix[j]
    # check if the sys has one or infinite solutions
    old_matrix = matrix
    matrix = signify_sys(matrix)
    if len(matrix) < len(matrix[0]) - 1:
        raise KeyboardInterrupt
    # second part of the algorithm: diagonal
    for j in range(len(matrix[0]) - 2, -1, -1):  # go through the columns backwards
        for i in range(j - 1, -1, -1):  # go through the rows upwards
            print(f"-{np.round(matrix[i][j], 4)} * R{j + 1} + R{i + 1} -> R{i + 1}".replace(")", "").replace("(", "").replace(".0", "").replace("--", ""))
            matrix[i] = matrix[i] - matrix[i][j] * matrix[j]
    return matrix


# setting the argument parsing
parser = argparse.ArgumentParser()
parser.add_argument("--infile")
parser.add_argument("--outfile")
args = parser.parse_args()
# read the system of equations
with open(args.infile, "r") as file:
    n, m = map(int, file.readline().strip().split())
    sys = file.read()
    equations = np.array([[complex(x) if "j" in sys else float(x) for x in eq.split()] for eq in sys.strip().split("\n")])
# echelon the system
with open(args.outfile, "w") as file:
    try:
        res = tuple(str(np.round(row[-1], 4)).replace(")", "").replace("(", "") for row in echelon_sys(equations))
        print(f"The solution is: {res}".replace("'", ""))
        file.write("\n".join(map(str, res)))
    except AssertionError:
        print("No solutions")
        file.write("No solutions")
    except (KeyboardInterrupt, IndexError):
        print("Infinitely many solutions")
        file.write("Infinitely many solutions")
    print(f"Saved to {args.outfile}")
