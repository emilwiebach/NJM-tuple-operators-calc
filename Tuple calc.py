import sympy
from sympy import factor

N=sympy.Symbol('N')

#This calculator serves to add and multiply tuples of polariser powers
#A sum of tuples of polariser power has to be introduced as a list
#The first entry of the list specifies the lengths of the tuples
#The second a global factor with which the sum shall be multiplied
#Every other entry has to consist of a list with two entries. Its first entry (the tuple) a list with integer entries) and its second entry a coefficient
#Exmp: tupsum=[3, 1/(N**2), ([0,0,0], 1), ([1,0,0],N), ([0,1,2], -2*(N-2))]

def extend(tupsum, k): #extends each tuple in a sum of tuples by k zeroes
    tupsum[0]=tupsum[0]+k
    for i in range(2,len(tupsum)):
        tupsum[i][0].extend(k*[0])
    return tupsum

def tupsumsimplify(tupsum):
    i=2
    while i<len(tupsum):
        j=i+1
        while j<len(tupsum):
            if tupsum[i][0]==tupsum[j][0]:
                tupsum[i][1]=tupsum[i][1]+tupsum[j][1]
                tupsum.pop(j)
            j=j+1
        i=i+1
    return tupsum

def scale(tupsum): #takes the global factor and multiplies each tuple with it, eliminating the global factor
    x=tupsum[1]
    for i in range(2,len(tupsum)):
        tupsum[i][1]=tupsum[i][1]*x
    tupsum[1]=1
    return tupsum

def add(tupsum1, tupsum2):
    if tupsum1[0]<tupsum2[0]:
        tupsum1=extend(tupsum1, tupsum2[0]-tupsum1[0])
    elif tupsum1[0]>tupsum2[0]:
        tupsum2=extend(tupsum2, tupsum1[0]-tupsum2[0])
    tupsum1=scale(tupsum1)
    tupsum2=scale(tupsum2)
    res=tupsum1+tupsum2[2:len(tupsum2)]
    res=tupsumsimplify(res)
    return res

def addtup(tup1, tup2): #adds single tuples of same length
    res=[]
    for i in range(len(tup1)):
        res.append(tup1[i]+tup2[i])
    return res

def multiply(tupsum1, tupsum2):
    if tupsum1[0]<tupsum2[0]:
        tupsum1=extend(tupsum1, tupsum2[0]-tupsum1[0])
    elif tupsum1[0]>tupsum2[0]:
        tupsum2=extend(tupsum2, tupsum1[0]-tupsum2[0])
    res=[tupsum1[0], factor(tupsum1[1]*tupsum2[1])]
    for i in range(2,len(tupsum1)):
        for j in range(2,len(tupsum2)):
            res.append([addtup(tupsum1[i][0], tupsum2[j][0]), tupsum1[i][1]*tupsum2[j][1]])
    return res

def multiplyandsimplify(tupsum1, tupsum2):
    res=tupsumsimplify(multiply(tupsum1, tupsum2))
    return res

def tuptostr(tup):
    res="("
    for i in range(len(tup)):
        res=res+str(tup[i])+","
    res=res[:-1]+")"
    return res

def tupsumtostr(tupsum):
    c=1/tupsum[1]
    res="("+str(tupsum[1])+")"+"*("
    for i in range(2,len(tupsum)):
        res=res+"("+str(tupsum[i][1])+")"+"*"+tuptostr(tupsum[i][0])+"+"
    res=res[:-1]+")"
    return res

def tupsumtolatex(tupsum):
    c = 1 / tupsum[1]
    res = ""
    if c!=1.0:
        res = "\\frac{"
    for i in range(2, len(tupsum)):
        res = res + "(" + str(tupsum[i][1]) + ")" + "*" + tuptostr(tupsum[i][0]) + "+"
    if c != 1.0:
        res = res[:-1] +"}{"+str(c)+"}"
    else:
        res=res[:-1]
    res=res.replace("**", "^")
    res=res.replace("*", "\\cdot ")
    return res


w=(N-1)/2

idemp=[]
#in this list will consist of all Jucys Murphy idempotents and a string with their name in it

#The Jucys Murphy idempotents for n=0:
E011=[1,1, [[0],1]]
idemp.append(["E011",E011])

#The Jucys Murphy idempotents for n=1:
E111=[1,1, [[0],1]]
idemp.append(["E111",E111])

#The Jucys Murphy idempotents for n=2:
E211=[1, 1/(N*(N-2)), [[0], -1], [[2],1]]
idemp.append(["E211", E211])
E221=[1, 1/(N*2), [[0], N-1], [[1], N], [[2],1]]
idemp.append(["E221", E221])
E231=[1, 1/(2*(N-2)), [[0], N-1], [[1], -N+2], [[2],-1]]
idemp.append(["E231", E231])

def jm (F, c, A, n):
    x=[0]*(n-1)
    y=[0]*(n-1)
    y[n-2]=1
    if A!=[]:
        E=[n-2, 1/(c-A[0]), [x, w-A[0]], [y,1] ]
        for i in range(1,len(A)):
            E=multiplyandsimplify(E, [2, 1/(c-A[i]),[x, w-A[i]], [y,1]])
        E=multiply(F, E)
        return E
    else:
        return extend(F,1)

#The Jucys Murphy idempotents for n=3
A311=[]
c311=w
E311=jm(E211,c311,A311,3)
idemp.append(["E311", E311])
A312=[w+2, w-1]
c312=-w+1
E312=jm(E231,c312,A312,3)
idemp.append(["E312", E312])
A313=[w-2,w+1]
c313=-w+1
E313=jm(E231,c313,A313,3)
idemp.append(["E313", E313])
A321=[-w-1, w-1]
c321=w+2
E321=jm(E221,c321,A321,3)
idemp.append(["E321", E321])
A331=[-w-1, w+2]
c331=w-1
E331=jm(E221,c331,A331,3)
idemp.append(["E331", E331])
A332=[w-2,-w+1]
c332=w+1
E332=jm(E231,c332,A332,3)
idemp.append(["E332", E332])
A341=[w+1, -w+1]
c341=w-2
E341=jm(E231,c341,A341,3)
idemp.append(["E341", E341])

#The Jucys Murphy idempotents for n=4:
A411=[w+1,w-1]
c411=-w
E411=jm(E311,c411,A411,4)
idemp.append(["E411", E411])
A412=[w+1,w-1]
c412=-w
E412=jm(E312,c412,A412,4)
idemp.append(["E412", E412])
A413=[w+1,w-1]
c413=-w
E413=jm(E313,c413,A413,4)
idemp.append(["E413", E413])
A421=[-w,w-1]
c421=w+1
E421=jm(E312,c421,A421,4)
idemp.append(["E421", E421])
A422=[-w,w-1]
c422=w+1
E422=jm(E313,c422,A422,4)
idemp.append(["E422", E422])
A423=[-w,w-1]
c423=w+1
E423=jm(E311,c423,A423,4)
idemp.append(["E423", E423])
A424=[-w-1,w+2,w, w-2]
c424=-w+1
E424=jm(E331,c424,A424,4)
idemp.append(["E424", E424])
A425=[-w-1,w+2,w, w-2]
c425=-w+1
E425=jm(E332,c425,A425,4)
A426=[w+3, w-1]
c426=-w-2
E426=jm(E321,c426,A426,4)
idemp.append(["E426", E426])

with open("JM Latex.txt", "w") as f:
    f.write(idemp[0][0]+":"+tupsumtolatex(idemp[0][1]))
with open("JM Latex.txt", "a") as f:
    for x in idemp[1:len(idemp)]:
        f.write("\\newline " + x[0] + ":" + tupsumtolatex(x[1]))
