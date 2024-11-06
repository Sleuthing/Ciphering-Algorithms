import numpy as np
import sys
import string
import ast
plainText = ""
operation_code= ""
jmode = False
al = list(string.ascii_lowercase)
one = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
#Utility functions


def split(word):
    return [char for char in word]


def jmodeAssign(se, y):
    if jmode:
        try:
            al.remove('i')
        except:
            pass
        if 'i' in se:
            se.remove('i')
            se.add('j')
        if 'i' in y:
            print(y)
            z = y.index('i')
            y[z] = 'j'
            print(y)
    else:
        try:
            al.remove('j')
        except:
            pass
        if 'j' in se:
            se.remove('j')
            se.add('i')
        if 'j' in y:
            z = y.index('j')
            y[z] = 'i'
    return se, y


def getOpMatChr(s, line, c):
    r = np.where(s == line[0])
    r1 = np.where(s == line[1])
    if operation_code== "enc":
        a = -1
    else:
        a = +1
    rr011 = r[1]-r1[1]
    rr110 = r1[1]-r[1]
    #equal rows
    if r[0] == r1[0]:
        t = r[1]-a
        t1 = r1[1]-a
        if t < 5 and t >= 0:
            col = t
            row = r[0]
        else:
            col = t % 5
            row = r[0]
        if t1 < 5 and t1 >= 0:
            col1 = t1
            row1 = r1[0]
        else:
            col1 = t1 % 5
            row1 = r1[0]
        print("rows are equal")
    #equal cols
    elif r[1] == r1[1]:
        t = r[0]-a
        t1 = r1[0]-a
        if t < 5 and t >= 0:
            row = t
            col = r[1]
        else:
            row = t % 5
            col = r[1]
        if t1 < 5 and t1 >= 0:
            row1 = t1
            col1 = r1[1]
        else:
            row1 = t1 % 5
            col1 = r1[1]
        print("columns are equal")
    #col1 is bigger
    elif r[1] > r1[1]:
        col = r[1]-rr011
        row = r[0]
        col1 = r1[1]+rr011
        row1 = r1[0]
        print("column1 is bigger")
    #col2 is bigger
    elif r[1] < r1[1]:
        col = r[1]+rr110
        row = r[0]
        col1 = r1[1]-rr110
        row1 = r1[0]
        print("column2 is bigger")
    return row, col, row1, col1, r, r1


def getProcessedString(plainText, lp):
    o = 0
    l = 1
    pp = []
    while o <= lp and l < lp:
        f1 = p[o]
        f2 = p[l]
        if f1 == f2:
            pp.append(f1)
            pp.append('x')
            o = l
            l = o+1
        else:
            pp.append(f1)
            pp.append(f2)
            o += 2
            l += 2
        if o == lp-1 and l >= lp:
            pp.append(plainText[lp-1])
            pp.append('x')
            break
        #print(o,l)
    #print(pp)
    return pp


def getMultiplicativeInverse(r2):
    r1 = 26
    t1 = 0
    t2 = 1
    while (r2 != 0):
        q = r1//r2
        r = r1 % r2
        t = t1-q*t2
        r1 = r2
        r2 = r
        t1 = t2
        t2 = t
    if r1 == 1:
        k11 = t1 % 26
        return k11
    else:
        return "This value can't be used as a key, use one that satisfies: gcd(k,26)=1."


def getInverseMatrix(a):
    e, r = np.shape(a)
    if e == r == 2:
        t = a[0][0]
        a[0][0] = a[1][1]
        a[1][1] = t
        a[1][0] = -1*a[1][0]
        a[0][1] = -1*a[0][1]
        d = a[0][0]*a[1][1]-a[1][0]*a[0][1] % 26
        d = getMultiplicativeInverse(d)
        a = a*d
    else:
        return "Non 2x2 matrices aren't supported yet."
    return a
#Ciphering Algos


def AdditiveCipher():
    output = []
    plainText_length = len(plainText)
    for character_index in range(plainText_length):
        if operation_code == 'enc':
            character_code = ((ord(plainText[character_index])-97)+int(k)) % 26
        elif operation_code == 'dec':
            character_code = ((ord(plainText[character_index])-97)-int(k)) % 26
        else:
            return "Wrong operation code (only 'enc' or 'dec')."
        output.append(chr(character_code+97))

    return f"Original Text: {plainText}\n{operation_code.title()}oded  Text: {''.join(output)}"
   


def MultiplicativeCipher():
    y = []
    lp = len(plainText)
    k1 = getMultiplicativeInverse(int(k))
    if type(k1) != str:
        for i in range(lp):
            if operation_code == 'enc':
                m = ((ord(plainText[i])-97)*int(k)) % 26
            elif operation_code == 'dec':
                m = ((ord(plainText[i])-97)*k1) % 26
            else:
                return "Wrong operation code (only 'enc' or 'dec')."
            y.append(chr(m+97))
    else:
        return k1
    m = ''.join(y)
    if operation_code == 'enc':
        return "Original Text: "+plainText+"\nEncoded  Text: "+m
    else:
        return "Original Text: "+plainText+"\nDecoded  Text: "+m


def AffineCipher():
    y = []
    lp = len(plainText)
    k11 = getMultiplicativeInverse(int(k))
    if type(k11) != str:
        for i in range(lp):
            if operation_code == 'enc':
                m = ((ord(plainText[i])-97)*int(k)+int(k1)) % 26
            elif operation_code == 'dec':
                m = (((ord(plainText[i])-97)-int(k1))*k11) % 26
            else:
                return "Wrong operation code (only 'enc' or 'dec')."
            y.append(chr(m+97))
    else:
        return k11
    m = ''.join(y)
    if operation_code == 'enc':
        return "Original Text: "+plainText+"\nEncoded  Text: "+m
    else:
        return "Original Text: "+plainText+"\nDecoded  Text: "+m


def VigenereCipher():
    s = []
    lk = len(k)
    lp = len(plainText)
    '''if lk<lp:
        while len(s)<len(plainText): 
            for i in range(lk):
                s.append(k[i])
        y=''.join(s)
    else:
        y=k   
    s.clear()'''
    for i in range(lp):
        '''if c=="enc":
            t=((ord(p[i])-97)+(ord(y[i])-97)) % 26
            elif c=="dec":
            t=((ord(p[i])-97)-(ord(y[i])-97)) % 26'''
        if operation_code == "enc":
            t = ((ord(plainText[i])-97)+(ord(k[i % lk])-97)) % 26
        elif operation_code == "dec":
            t = ((ord(plainText[i])-97)-(ord(k[i % lk])-97)) % 26
        else:
            return "Wrong operation code (only 'enc' or 'dec')."
        s.append(chr(t+97))
    r = ''.join(s)
    if operation_code == "dec":
        return "Original Text: "+plainText+"\nDecoded  Text: "+r
    else:
        return "Original Text: "+plainText+"\nEncoded  Text: "+r


def AutoKeyCipher():
    s = []
    lk = len(k)
    lp = len(plainText)
    ll = lp-lk
    if operation_code == "enc":
        if lk < lp:
            for i in range(lk):
                s.append(k[i])
            for i in range(ll):
                s.append(plainText[i])
            y = ''.join(s)
        else:
            y = k
        s.clear()
        for i in range(lp):
            t = ((ord(plainText[i])-97)+(ord(y[i])-97)) % 26
            s.append(chr(t+97))
        r = ''.join(s)
        return "Original Text: "+plainText+"\nEncoded  Text: "+r
    elif operation_code == "dec":
        if lk < lp:
            y = k
            for i in range(lk):
                t = ((ord(plainText[i])-97)-(ord(y[i])-97)) % 26
                s.append(chr(t+97))
            for i in range(lk, lp):
                t = ((ord(plainText[i])-97)-(ord(s[i-lk])-97)) % 26
                s.append(chr(t+97))
        else:
            y = k
            for i in range(lp):
                t = ((ord(plainText[i])-97)-(ord(y[i])-97)) % 26
                s.append(chr(t+97))
        r = ''.join(s)
        return "Original Text: "+plainText+"\nDecoded  Text: "+r
    else:
        return "Wrong operation code (only 'enc' or 'dec')."


'''def HillCipher():
    o=0 
    lp=len(plainText)
    lj=lp//2
    s=([0,0],[0,0])
    n=([0,0],[0,0],[0,0],[0,0])
    if c=="enc":
        for i in range(2):
            for j in range(2):
                s[i][j]=ord(k[o])-97
                if o!=3:
                    o+=1
        #for i in range(2):
            for j in range(2):
                print(m[i][j])
            print()
        o=0
        #print(str(lp)+" "+str(lj))
        for i in range(lj):
            for j in range(2):
                n[i][j]=ord(plainText[o])-97
                #print(plainText[o])
                if  o!=lp-1:
                    o+=1
        #for i in range(lj):
            for j in range(2):
                print(n[i][j])
            #print()
        t=np.dot(n,s) 
        r=[]
        for i in range(lj):
            for j in range(2):
                r.append(chr(t[i][j]%26+97))
        m=''.join(r)
        return "Original Text: "+plainText+"\nEncoded  Text: "+'''


def HC():
    o = 0
    lp = len(plainText)
    if lp % 2 == 0:
        lp2 = len(plainText)//2
    else:
        lp2 = len(plainText)//2+1
    lk = len(k)
    s = np.zeros((2, 2), dtype=np.int32)
    n = np.zeros((lp2, 2), dtype=np.int32)
    for i in range(2):
        for j in range(2):
            s[i][j] = ord(k[o])-97
            if o != lk-1:
                o += 1
    o = 0
    for i in range(lp2):
        for j in range(2):
            if o <= lp-1:
                n[i][j] = ord(plainText[o])-97
                o += 1
            elif lp % 2 != 0:
                n[i][j] = ord('z')-97
            else:
                pass
    if operation_code == "enc":
        t = np.dot(n, s)
    elif operation_code == "dec":
        s = getInverseMatrix(s)
        t = np.dot(n, s)
    else:
        return "Wrong operation code (only 'enc' or 'dec')."
    r = []
    for i in range(lp2):
        for j in range(2):
            r.append(chr(t[i][j] % 26+97))
    m = ''.join(r)
    if operation_code == "enc":
        return "Original Text: "+plainText+"\nEncoded  Text: "+m
    elif operation_code == "dec":
        return "Original Text: "+plainText+"\nDecoded  Text: "+m


def PlayfairCipher():
    #set up the variables and lists
    lp = len(plainText)
    l = []
    o = 0
    oo = 0
    #process string to add 'x' between each two repeated characters
    #and add 'x' at the end -if needed- to satisfy (length of prcoessed string)%2==0
    #initialize the matrices with the proper shape
    pp = getProcessedString(plainText, lp)
    lpp = len(pp)
    lppl = lpp//2
    s = np.zeros((5, 5), dtype=np.int32)
    n = np.zeros((lppl, 2), dtype=np.int32)
    se = set()
    y = split(k)
    lk = len(y)
    # determines if j or i is used
    se, y = jmodeAssign(se, y)
    #get a unique character key string and
    #remove its characters from the alphabet
    for i in range(lk):
        se.add(y[i])
    for i in range(lk):
        if y[i] in se:
            l.append(y[i])
            se.remove(y[i])
            al.remove(y[i])
    #filling up the matrix s with the result of the previous operations
    #unique key chracters first then the rest of the non used alphabet characters
    #row-wise
    ll = len(l)
    for i in range(5):
        for j in range(5):
            if o < ll:
                s[i][j] = ord(l[o])-97
                o += 1
            else:
                s[i][j] = ord(al[oo])-97
                oo += 1
    print(s)
    o = 0
    if operation_code == "enc":
        #filling up the matrix n with the characters from the processed string
        #a couple at a time, row wise
        for i in range(lppl):
            for j in range(2):
                n[i][j] = ord(pp[o])-97
                o += 1
        print(n)
        #after doing that we calculate the encoded character for each of the characters
        #from the couples we made and then make new couples that are the encoded string
        cc = []
        for line in n:
            row, col, row1, col1, r, r1 = getOpMatChr(s, line, c)
            '''print(str(line[0])+" row: "+str(r[0])+" new row: "+str(row)+" col: "+str(r[1])+" new col: "+str(col))
            print(str(line[1])+" row1: "+str(r1[0])+" new row1: "+str(row1)+" col1: "+str(r1[1])+" new col1: "+str(col1))
            print(line[1],r1[0],r1[1],col1)'''
            cc.append(chr(s[int(row)][int(col)]+97))
            cc.append(chr(s[int(row1)][int(col1)]+97))
            #print(cc[0],cc[1])
        jj = ''.join(cc)
        return "Original Text: "+plainText+"\nEncoded  Text: "+jj
    elif operation_code == "dec":
        #filling up the matrix n with the encoded string, row wise
        for i in range(lppl):
            for j in range(2):
                n[i][j] = ord(pp[o])-97
                o += 1
        print(n)
        #getting the decoded characters for each of the characters in the encoded string
        #resulting a new string made of decoded couples, that we will most likely
        #have to remove excess 'x's from
        cc = []
        for line in n:
            row, col, row1, col1, r, r1 = getOpMatChr(s, line, c)
            '''print(str(line[0])+" row: "+str(r[0])+" new row: "+str(row)+" col: "+str(r[1])+" new col: "+str(col))
            print(str(line[1])+" row1: "+str(r1[0])+" new row1: "+str(row1)+" col1: "+str(r1[1])+" new col1: "+str(col1))
            print()
            print(line[1],r1[0],r1[1],col1)'''
            cc.append(chr(s[int(row)][int(col)]+97))
            cc.append(chr(s[int(row1)][int(col1)]+97))
            #print(cc[0],cc[1])
        jj = ''.join(cc)
        return "Original Text: "+plainText+"\nDecoded  Text: "+jj
    else:
        return "Wrong operation code (only 'enc' or 'dec')."


def ADFGVXCipher():
    #setting up variables, sets, lists and matrices
    AX = ['A', 'D', 'F', 'G', 'V', 'X']
    lp = len(plainText)
    l = []
    o = 0
    oo = 0
    #k1=getProcessedString(k1,len(k1))
    s = np.zeros((6, 6), dtype=np.str)
    se = set()
    #check if key is of the right type
    if type(k) == str:
        y = split(k)
    else:
        return "Wrong key type."
    lk = len(y)
    se = set()
    #y=k
    #setting up the key character list and removing duplicate characters
    for i in range(lk):
        se.add(y[i])
    for i in range(lk):
        if y[i] in se:
            l.append(y[i])
            se.remove(y[i])
            try:
                al.remove(y[i])
            except:
                one.remove(y[i])
    ll = len(l)
    olo = 0
    #filling up the matrix with the key characters first then the rest of the unused alphabet characters
    for i in range(6):
        for j in range(6):
            if o < ll:
                s[i][j] = l[o]
                o += 1
            elif oo < len(al):
                s[i][j] = al[oo]
                oo += 1
            elif olo < len(one):
                s[i][j] = one[olo]
                olo += 1
    print(s)
    if operation_code == "enc":
        cc = []
        #getting the tw v c"o character code for each character in the original text
        for i in range(lp):
            q = np.where(s == p[i])
            #print(q[0],q[1])
            cc.append(AX[int(q[0])])
            cc.append(AX[int(q[1])])
        print(cc)
        lk1 = len(k1)
        sk1 = []
        #sorting the characters of the second key out in a list
        for i in range(lk1):
            sk1.append(k1[i])
        sk1.sort()
        #print(sk1)
        #figuring out the shape of the second key matrix to initialize it correctly
        if len(cc) % lk1 == 0:
            lkc = len(cc)//lk1+1
        else:
            lkc = len(cc)//lk1+2
        n = np.zeros((lk1, lkc), dtype=np.str)
        o = 0
        oo = 0
        # fill that matrix with the second key characters in the first column and the two-character-codes
        # in the rest of the columns, in a column-wise filling pattern, and filling what's left with 'A's
        for j in range(lkc):
            for i in range(lk1):
                if oo < lk1:
                    n[i][j] = k1[oo]
                    oo += 1
                elif oo > lk1-1 and o < len(cc):
                    n[i][j] = cc[o]
                    o += 1
                else:
                    n[i][j] = 'X'
        print(n)
        scc = []
        # getting the final coded string by extracting the codes row-wise from the matrix n that we just built
        # into a list and according to the character indexes of the second key that we sorted alphabetically
        for i in range(lk1):
            q = np.where(n == sk1[i])
            for j in range(1, lkc):
                #print(q[0],q[1])
                try:
                    scc.append(n[int(q[0])][int(q[1])+j])
                except:
                    return "Second keyword has duplicate characters, choose one with no duplicate characters (e.x: corn)"
        jj = ''.join(scc)
        return "Original Text: "+plainText+"\nEncoded  Text: "+jj
    elif operation_code == "dec":
        cc = []
        #inserting all of the encdod text characters into a list
        for i in range(lp):
            #q=np.where(s==p[i])
            #print(q[0],q[1])
            cc.append(plainText[i])
        #sort the second key characters alphabetically
        lk1 = len(k1)
        sk1 = []
        for i in range(lk1):
            sk1.append(k1[i])
        sk1.sort()
        #determine the shape of the matrix n to intialize it
        if len(cc) % lk1 == 0:
            lkc = len(cc)//lk1+1
        else:
            lkc = len(cc)//lk1+2
        n = np.zeros((lk1, lkc), dtype=np.str)
        #filling the first column of n with the sorted key characters
        o = 0
        for j in range(lkc):
            for i in range(lk1):
                if o < lk1:
                    n[i][j] = sk1[o]
                    o += 1
        o = 0
        #filling the rest of the columns with the the encoded characters row-wise
        for i in range(lk1):
            for j in range(1, lkc):
                if o < len(cc):
                    n[i][j] = cc[o]
                    o += 1
        print(n)
        #finding out the original order of the two-character codes by comparing each letter
        #to its position in the second key string
        scc = []
        for i in range(lk1):
            q = np.where(n == k1[i])
            for j in range(1, lkc):
                #print(q[0],q[1])
                scc.append(n[int(q[0])][int(q[1])+j])
        #print(scc)
        #re-filling n with the non-sorted key characters in the first column
        o = 0
        for j in range(lkc):
            for i in range(lk1):
                if o < lk1:
                    n[i][j] = k1[o]
                    o += 1
        #re-filling the rest of n's columns row-wise with the two-character codes extracted
        o = 0
        for i in range(lk1):
            for j in range(1, lkc):
                if o < len(cc):
                    n[i][j] = scc[o]
                    o += 1
        print(n)
        #getting these two-character codes after into a list
        scc.clear()
        for j in range(1, lkc):
            for i in range(lk1):
                scc.append(n[i][j])
        #finally, finding the character in matrix s
        #that has the coordinates of the two-character code that belongs to it
        cc = []
        for i in range(0, len(scc), 2):
            a = AX.index(scc[i])
            d = AX.index(scc[i+1])
            #print(a,d)
            cc.append(s[a][d])
        jj = ''.join(cc)
        return "Original Text: "+plainText+"\nDecoded  Text: "+jj
    else:
        return "Wrong operation code (only 'enc' or 'dec')."


def PlaceSubstitutionCipher():
    pass


def DESCipher():
    pass


def navigator():
    algos = {
        "0": AdditiveCipher,
        "1": MultiplicativeCipher,
        "2": AffineCipher,
        "3": VigenereCipher,
        "4": AutoKeyCipher,
        "5": HC,
        "6": PlayfairCipher,
        "7": ADFGVXCipher
    }
    return algos[n]()


if __name__ == "__main__":
    al = list(string.ascii_lowercase)
    plainText = sys.argv[1]
    n = sys.argv[2]
    operation_code = sys.argv[3]
    if int(n) != 6:
        k = sys.argv[4]
    else:
        try:
            k = sys.argv[4]
        except:
            k = ''
    if int(n) == 2 or int(n) == 7:
        k1 = sys.argv[5]
    elif int(n) == 6:
        try:
            jmode = ast.literal_eval(sys.argv[5])
        except:
            jmode = False
    else:
        pass
    print(navigator())
