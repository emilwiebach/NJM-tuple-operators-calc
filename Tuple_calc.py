import sympy
from sympy import factor
from sympy import simplify
import copy

N = sympy.Symbol("N")


# This calculator serves to add and multiply tuples of polarizer powers (as introduced in my bachelor's thesis)
# A tuple corresponds to a product of polarizer powers, where the first entry is the exponent for p2, the second for p3 and so on
# A tuple is implemented as a list with integer entries
# A sum of tuples of polarizer powers has to be introduced as a list
# The first entry of the list specifies the lengths of the tuples
# The second a global factor with which each summand in the sum shall be multiplied
# Every other entry has to be a list consisting of a tuple as specified earlier and the corresponding coefficient in the sum
# Exmp: tupsum=[3, 1/(N**2), [[0,0,0], 1], [[1,0,0],N], [[0,1,2], -2*(N-2)]]
# The tuple calculator is then used to compute some NJM operators (as introduced in my bachelor's thesis)
# The NJM operators up to n=4 are calculated and stored according to the notation in my bachelor's thesis
# The NJM operators up to n=3 are written in to a .txt file, that can be copied into LaTex to display them
# The way the NJM operators are labeled is explained in Appendix A of my bachelor's thesis


def extend(tupsum, k):  #
    """
    Extends each tuple in a sum of tuples by k zeroes.

    Args:
        tupsum (list): The sum of tuples in the format [length, global factor, [tuple1, coeffiecient], ...].
        k (int): The number of zeroes by which to extend.
    """
    tupsum[0] = tupsum[0] + k
    for i in range(2, len(tupsum)):
        tupsum[i][0].extend(k * [0])


def tupsumsimplify(tupsum):
    """
    Simplifies a sum of tuples. If the same tuple appears more than once in a sum these entries are combined into one by adding coefficient. Tuples with coefficient zero are omitted.

    Args:
        tupsum (list): The sum of tuples in the format [length, global factor, [tuple1, coeffiecient], ...].
    """
    tupsum[1] = simplify(tupsum[1])
    i = 2
    while i < len(tupsum):
        j = len(tupsum) - 1
        while j > i:
            if tupsum[i][0] == tupsum[j][0]:
                tupsum[i][1] = tupsum[i][1] + tupsum[j][1]
                tupsum.pop(j)
            j = j - 1
        if tupsum[i][1] == 0:
            tupsum.pop(i)
        else:
            tupsum[i][1] = simplify(tupsum[i][1])
        i = i + 1


def scale(tupsum):
    """
    Multiplies each tuple in a sum of tuples by the global factor and setting the global factor to 1.

    Args:
        tupsum (list): The sum of tuples in the format [length, global factor, [tuple1, coeffiecient], ...].
    """
    x = tupsum[1]
    for i in range(2, len(tupsum)):
        tupsum[i][1] = tupsum[i][1] * x
    tupsum[1] = 1


def add(t1, t2):
    """
    Adds two sums of tuples and simplifies the result without manipulating the arguments.

    Args:
        t1 (list): The first sum of tuples in the format [length, global factor, [tuple1, coeffiecient], ...].
        t2 (list): The second sum of tuples in the same format.

    Returns:
        list: The simplified sum of the two sums of tuples in the same format.
    """
    tupsum1 = copy.deepcopy(t1)
    tupsum2 = copy.deepcopy(t2)
    if tupsum1[0] < tupsum2[0]:
        extend(tupsum1, tupsum2[0] - tupsum1[0])
    elif tupsum1[0] > tupsum2[0]:
        extend(tupsum2, tupsum1[0] - tupsum2[0])
    scale(tupsum1)
    scale(tupsum2)
    res = tupsum1 + tupsum2[2: len(tupsum2)]
    tupsumsimplify(res)
    return res


def multtup(t1, t2):
    """
    Multiplies two tuples of the same length without manipulating the arguments.

    Args:
        t1 (list): The first tuple as a list of non-negative integers.
        t2 (list): The second tuple in the same format.

    Returns:
        list: The product of the two tuples in the same format.
    """
    tup1 = copy.deepcopy(t1)
    tup2 = copy.deepcopy(t2)
    res = []
    for i in range(len(tup1)):
        res.append(tup1[i] + tup2[i])
    return res


def multiply(t1, t2):
    """
    Multiplies two sums of tuples without manipulating the arguments.

    Args:
        t1 (list): The first sum of tuples in the format [length, global factor, [tuple1, coeffiecient], ...].
        t2 (list): The second sum of tuples in the same format.

    Returns:
        list: The product of the two sums of tuples in the same format.
    """
    tupsum1 = copy.deepcopy(t1)
    tupsum2 = copy.deepcopy(t2)
    if tupsum1[0] < tupsum2[0]:
        extend(tupsum1, tupsum2[0] - tupsum1[0])
    elif tupsum1[0] > tupsum2[0]:
        extend(tupsum2, tupsum1[0] - tupsum2[0])
    res = [tupsum1[0], factor(tupsum1[1] * tupsum2[1])]
    for i in range(2, len(tupsum1)):
        for j in range(2, len(tupsum2)):
            res.append(
                [multtup(tupsum1[i][0], tupsum2[j][0]), tupsum1[i][1] * tupsum2[j][1]]
            )
    return res


def multiplyandsimplify(tupsum1, tupsum2):
    """
    Multiplies two sums of tuples and simplifies the result without manipulating the arguments.

    Args:
        t1 (list): The first sum of tuples in the format [length, global factor, [tuple1, coeffiecient], ...].
        t2 (list): The second sum of tuples in the same format.

    Returns:
        list: The simplified product of the two sums of tuples in the same format.
    """
    res = multiply(tupsum1, tupsum2)
    tupsumsimplify(res)
    return res


def tuptostr(tup):
    """
    Converts a tuple into a string.

    Args:
        tup (list): The tuple as a list of non-negative integers.

    Returns:
        str: The string containing the tuple.
    """
    res = "("
    for i in range(len(tup)):
        res = res + str(tup[i]) + ","
    res = res[:-1] + ")"
    return res


def tupsumtostr(tupsum):
    """
    Converts a sum of tuples into a string.

    Args:
        tupsum (list): The sum of tuples in the format [length, global factor, [tuple1, coeffiecient], ...].

    Returns:
        str: The string containing the sum of tuples.
    """
    c = 1 / tupsum[1]
    res = "(" + str(tupsum[1]) + ")" + "*("
    for i in range(2, len(tupsum)):
        res = res + "(" + str(tupsum[i][1]) + ")" + "*" + tuptostr(tupsum[i][0]) + "+"
    res = res[:-1] + ")"
    return res


def tupsumtolatex(tupsum):
    """
    Generates a string containing LaTex that can be copied in order to display a sum of tuples.

    Args:
        tupsum (list): The sum of tuples in the format [length, global factor, [tuple1, coeffiecient], ...].

    Returns:
        str: The string containing the LaTex code.
    """
    c = 1 / tupsum[1]
    res = ""
    if c != 1.0:
        res = "\\frac{1}{" + str(c) + "}\\cdot \\left("
    for i in range(2, len(tupsum)):
        res = res + "(" + str(tupsum[i][1]) + ")" + "*" + tuptostr(tupsum[i][0]) + "+"
    if c != 1:
        res = res[:-1] + "\\right)"
    else:
        res = res[:-1]
    res = res.replace("(1)*", "")
    res = res.replace("(-1)*", "-")
    res = res.replace("+-", "-")
    res = res.replace("**", "^")
    res = res.replace("*", "\\cdot ")
    return res


w = (N - 1) / 2


def njm(J, n, c, A):
    """
    Calculates the NJM operator for a given up-down-tableau.

    Args:
        J (list): The NJM operator of the predecessor tableau as a sum of tuples in the format [length, global factor, [tuple1, coeffiecient], ...].
        n (int): The length of the up-down-tableau.
        c (expr): The n-th refined content of the up-down-tableau as a sympy-expression.
        A (list): The refined contents of all the boxes that could have been added or removed in the n-th step instead as a list of sympy-expressions.

    Returns:
        list: The NJM operator for this up-down-tableau as a sum of tuples in the same format.
    """
    x = [0] * (n - 1)
    y = [0] * (n - 1)
    y[n - 2] = 1
    F = copy.deepcopy(J)
    if A != []:
        E = [n - 1, 1 / (c - A[0]), [x, w - A[0]], [y, 1]]
        for i in range(1, len(A)):
            E = multiplyandsimplify(E, [n - 1, 1 / (c - A[i]), [x, w - A[i]], [y, 1]])
        E = multiply(F, E)
        return E
    else:
        extend(F, 1)
        return F


idemp = []
# this list will consist of all NJM operators up to n=3 and a string with their name in it

# The NJM operator for n=1:
J1 = [1, 1, [[0], 1]]
idemp.append(["J1", J1])

# The NJM operators for n=2:
c1_0 = -w
A1_0 = [w + 1, w - 1]
J1_0 = njm(J1, 2, c1_0, A1_0)
idemp.append(["J1_0", J1_0])

c1_2 = w + 1
A1_2 = [-w, w - 1]
J1_2 = njm(J1, 2, c1_2, A1_2)
idemp.append(["J1_2", J1_2])

c1_3 = w - 1
A1_3 = [-w, w + 1]
J1_3 = njm(J1, 2, c1_3, A1_3)
idemp.append(["J1_3", J1_3])

# The NJM operators for n=3:
c1_0_1 = w
A1_0_1 = []
J1_0_1 = njm(J1_0, 3, c1_0_1, A1_0_1)
idemp.append(["J1_0_1", J1_0_1])

c1_2_1 = -w - 1
A1_2_1 = [w + 2, w - 1]
J1_2_1 = njm(J1_2, 3, c1_2_1, A1_2_1)
idemp.append(["J1_2_1", J1_2_1])

c1_2_4 = w + 2
A1_2_4 = [-w - 1, w - 1]
J1_2_4 = njm(J1_2, 3, c1_2_4, A1_2_4)
idemp.append(["J1_2_4", J1_2_4])

c1_2_5 = w - 1
A1_2_5 = [-w - 1, w + 2]
J1_2_5 = njm(J1_2, 3, c1_2_5, A1_2_5)
idemp.append(["J1_2_5", J1_2_5])

c1_3_1 = -w + 1
A1_3_1 = [w + 1, w - 2]
J1_3_1 = njm(J1_3, 3, c1_3_1, A1_3_1)
idemp.append(["J1_3_1", J1_3_1])

c1_3_5 = w + 1
A1_3_5 = [-w + 1, w - 2]
J1_3_5 = njm(J1_3, 3, c1_3_5, A1_3_5)
idemp.append(["J1_3_5", J1_3_5])

c1_3_6 = w - 2
A1_3_6 = [-w + 1, w + 1]
J1_3_6 = njm(J1_3, 3, c1_3_6, A1_3_6)
idemp.append(["J1_3_6", J1_3_6])

# The NJM operators for n=4:
c1_0_1_0 = -w
A1_0_1_0 = [w + 1, w - 1]
J1_0_1_0 = njm(J1_0_1, 4, c1_0_1_0, A1_0_1_0)

c1_0_1_2 = w + 1
A1_0_1_2 = [-w, w - 1]
J1_0_1_2 = njm(J1_0_1, 4, c1_0_1_2, A1_0_1_2)

c1_0_1_3 = w - 1
A1_0_1_3 = [-w, w + 1]
J1_0_1_3 = njm(J1_0_1, 4, c1_0_1_3, A1_0_1_3)

c1_2_1_0 = -w
A1_2_1_0 = [w + 1, w - 1]
J1_2_1_0 = njm(J1_2_1, 4, c1_2_1_0, A1_2_1_0)

c1_2_1_2 = w + 1
A1_2_1_2 = [-w, w - 1]
J1_2_1_2 = njm(J1_2_1, 4, c1_2_1_2, A1_2_1_2)

c1_2_1_3 = w - 1
A1_2_1_3 = [-w, w + 1]
J1_2_1_3 = njm(J1_2_1, 4, c1_2_1_3, A1_2_1_3)

c1_2_4_2 = -w - 2
A1_2_4_2 = [w + 3, w - 1]
J1_2_4_2 = njm(J1_2_4, 4, c1_2_4_2, A1_2_4_2)

c1_2_4_7 = w + 3
A1_2_4_7 = [-w - 2, w - 1]
J1_2_4_7 = njm(J1_2_4, 4, c1_2_4_7, A1_2_4_7)

c1_2_4_8 = w - 1
A1_2_4_8 = [-w - 2, w + 3]
J1_2_4_8 = njm(J1_2_4, 4, c1_2_4_8, A1_2_4_8)

c1_2_5_2 = -w + 1
A1_2_5_2 = [-w - 1, w + 2, w, w - 2]
J1_2_5_2 = njm(J1_2_5, 4, c1_2_5_2, A1_2_5_2)

c1_2_5_3 = -w - 1
A1_2_5_3 = [-w + 1, w + 2, w, w - 2]
J1_2_5_3 = njm(J1_2_5, 4, c1_2_5_3, A1_2_5_3)

c1_2_5_8 = w + 2
A1_2_5_8 = [-w + 1, -w - 1, w, w - 2]
J1_2_5_8 = njm(J1_2_5, 4, c1_2_5_8, A1_2_5_8)

c1_2_5_9 = w
A1_2_5_9 = [-w + 1, -w - 1, w + 2, w - 2]
J1_2_5_9 = njm(J1_2_5, 4, c1_2_5_9, A1_2_5_9)

c1_2_5_10 = w - 2
A1_2_5_10 = [-w + 1, -w - 1, w + 2, w]
J1_2_5_10 = njm(J1_2_5, 4, c1_2_5_10, A1_2_5_10)

c1_3_1_0 = -w
A1_3_1_0 = [w + 1, w - 1]
J1_3_1_0 = njm(J1_3_1, 4, c1_3_1_0, A1_3_1_0)

c1_3_1_2 = w + 1
A1_3_1_2 = [-w, w - 1]
J1_3_1_2 = njm(J1_3_1, 4, c1_3_1_2, A1_3_1_2)

c1_3_1_3 = w - 1
A1_3_1_3 = [-w, w + 1]
J1_3_1_3 = njm(J1_3_1, 4, c1_3_1_3, A1_3_1_3)

c1_3_5_2 = -w + 1
A1_3_5_2 = [-w - 1, w + 2, w, w - 2]
J1_3_5_2 = njm(J1_3_5, 4, c1_3_5_2, A1_3_5_2)

c1_3_5_3 = -w - 1
A1_3_5_3 = [-w + 1, w + 2, w, w - 2]
J1_3_5_3 = njm(J1_3_5, 4, c1_3_5_3, A1_3_5_3)

c1_3_5_8 = w + 2
A1_3_5_8 = [-w + 1, -w - 1, w, w - 2]
J1_3_5_8 = njm(J1_3_5, 4, c1_3_5_8, A1_3_5_8)

c1_3_5_9 = w
A1_3_5_9 = [-w + 1, -w - 1, w + 2, w - 2]
J1_3_5_9 = njm(J1_3_5, 4, c1_3_5_9, A1_3_5_9)

c1_3_5_10 = w - 2
A1_3_5_10 = [-w + 1, -w - 1, w + 2, w]
J1_3_5_10 = njm(J1_3_5, 4, c1_3_5_10, A1_3_5_10)

c1_3_6_3 = -w + 2
A1_3_6_3 = [w + 1, w - 3]
J1_3_6_3 = njm(J1_3_6, 4, c1_3_6_3, A1_3_6_3)

c1_3_6_10 = w + 1
A1_3_6_10 = [-w + 2, w - 3]
J1_3_6_10 = njm(J1_3_6, 4, c1_3_6_10, A1_3_6_10)

c1_3_6_11 = w - 3
A1_3_6_11 = [-w + 2, w + 1]
J1_3_6_11 = njm(J1_3_6, 4, c1_3_6_11, A1_3_6_11)

for x in idemp:
    x[0] = x[0].replace("_", ",")
    x[0] = x[0].replace("J", "J_{(")
    x[0] = x[0] + ")}"

with open("njm.txt", "w") as f:
    f.write("\\begin{dmath*}" + idemp[0][0] + "=" + tupsumtolatex(idemp[0][1]) + "\\end{dmath*}")
with open("njm.txt", "a") as f:
    for x in idemp[1: len(idemp)]:
        f.write("\\begin{dmath*}" + x[0] + "=" + tupsumtolatex(x[1]) + "\\end{dmath*}\n")

