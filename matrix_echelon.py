from fractions import Fraction
import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

def fr2str(a):
    if a.denominator == 1:
        return str(a.numerator)
    else:
        return str(a.numerator)+"/"+str(a.denominator)

def log(msg = "", endl = "\n"):
    print(msg, end=endl)

    with open("matrix_soln.txt", "a") as f:
        f.write(str(msg))
        f.write(endl)

def show(matrix):
    for row in matrix:
        log("    ", endl = "[ ")
        for a in row:
            log(fr2str(a), endl = " ")
        log("]")
    log()

def to_last(matrix, row):
    for k in range(len(matrix)-1, row, -1):
        if matrix[k][row] != Fraction(0):
            log("R"+str(row+1)+" <-> R"+str(k+1))
            matrix[row], matrix[k] = matrix[k], matrix[row]
            break
    return matrix

n = int(input("Enter number of columns: "))
m = int(input("Enter number of rows: "))

# Read matrix from file
matrix = []
with open("matrix.txt", "r") as f:
    for line in f:
        matrix.append(list(map(Fraction, line.split())))

# Initialize Solution file
with open("matrix_soln.txt", "w") as f:
    f.write("")

# Print read Matrix
log("Matrix:")
show(matrix)

log("Steps:\n")

# Convert matrix to Echelon form
for i in range(m):
    change = 0
    if matrix[i][i] == Fraction(0):
        for k in range(m-1, i, -1):
            if matrix[k][i] != Fraction(0):
                log("R"+str(i+1)+" <-> R"+str(k+1))
                matrix[i], matrix[k] = matrix[k], matrix[i]
                change = 1
                break
        show(matrix)
        if change == 0:
            continue
    for j in range(i + 1, m):
        if matrix[j][i] != Fraction(0):
            k = matrix[j][i] / matrix[i][i]
            log("R"+str(j+1)+" -> R"+str(j+1)+" - "+fr2str(k)+"*R"+str(i+1))
            for l in range(n):
                matrix[j][l] -= k * matrix[i][l]
    show(matrix)

log("Echelon form:")
show(matrix)

# Convert matrix to row reduced form

# Make pivot elements 1
pivot = []
for i in range(m):
    for j in range(n):
        if matrix[i][j] != 0:
            pivot.append((i, j))
            t = matrix[i][j]
            log("R"+str(i+1)+" -> R"+str(i+1)+" /"+fr2str(t))
            for l in range(j, n):
                matrix[i][l] /= t
            break

log("Pivot is 1:")
show(matrix)

# Make all other elements 0 in pivoted columns
while len(pivot) > 0:
    a, b = pivot.pop()
    for i in range(a):
        t = matrix[i][b]
        log("R"+str(i+1)+" -> R"+str(i+1)+" - "+fr2str(t)+"*R"+str(a+1))
        for j in range(b, n):
            matrix[i][j] -= t * matrix[a][j]
    show(matrix)

# Convert to Echelon form
for i in range(m):
    if all(x == Fraction(0) for x in matrix[i]):
        matrix = to_last(matrix, i)

# Print Solution
log("Row reduced Echelon form:")
show(matrix)