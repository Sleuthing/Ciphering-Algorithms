import numpy as np
import sys
import string
import ast
plain_text = ""
operation_code = ""
jmode = False
alphabet = list(string.ascii_lowercase)
digits = [str(digit) for digit in range(0,10)]
ALPHABET_OFFSET = 97
ALPHABET_LENGTH = 26


#Utility functions
def split(word):
    return [char for char in word]


def jmodeAssign(se, y):
    if jmode:
        try:
            alphabet.remove('i')
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
            alphabet.remove('j')
        except:
            pass
        if 'j' in se:
            se.remove('j')
            se.add('i')
        if 'j' in y:
            z = y.index('j')
            y[z] = 'i'
    return se, y


def getOpMatChr(s, line, operation_code):
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
        #print("rows are equal")
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
        #print("columns are equal")
    #col1 is bigger
    elif r[1] > r1[1]:
        col = r[1]-rr011
        row = r[0]
        col1 = r1[1]+rr011
        row1 = r1[0]
        #print("column1 is bigger")
    #col2 is bigger
    elif r[1] < r1[1]:
        col = r[1]+rr110
        row = r[0]
        col1 = r1[1]-rr110
        row1 = r1[0]
        #print("column2 is bigger")
    return row, col, row1, col1, r, r1


def getProcessedPlainText(plain_text):
    plain_text_length = len(plain_text)
    index_1 = 0
    index_2 = 1
    processed_text = []
    while index_1 <= plain_text_length and index_2 < plain_text_length:
        char_1 = plain_text[index_1]
        char_2 = plain_text[index_2]
        if char_1 == char_2:
            processed_text.append(char_1)
            processed_text.append('x')
            index_1 = index_2
            index_2 = index_1+1
        else:
            processed_text.append(char_1)
            processed_text.append(char_2)
            index_1 += 2
            index_2 += 2
        if index_1 == plain_text_length-1 and index_2 >= plain_text_length:
            processed_text.append(plain_text[plain_text_length-1])
            processed_text.append('x')
            break
    return processed_text


def getMultiplicativeInverse(r2):
    #AKA Euclidean Algorithm
    r1 = ALPHABET_LENGTH
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
        k11 = t1 % ALPHABET_LENGTH
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
        d = a[0][0]*a[1][1]-a[1][0]*a[0][1] % ALPHABET_LENGTH
        d = getMultiplicativeInverse(d)
        a = a*d
    else:
        return "Non 2x2 matrices aren't supported yet."
    return a


#Ciphering Algos
def AdditiveCipher():
    output = []
    plain_text_length = len(plain_text)
    for character_index in range(plain_text_length):
        if operation_code == 'enc':
            character_code = ((ord(plain_text[character_index])-ALPHABET_OFFSET)+int(key)) % ALPHABET_LENGTH
        elif operation_code == 'dec':
            character_code = ((ord(plain_text[character_index])-ALPHABET_OFFSET)-int(key)) % ALPHABET_LENGTH
        else:
            return "Wrong operation code (only 'enc' or 'dec')."
        output.append(chr(character_code+ALPHABET_OFFSET))

    return f"Original Text: {plain_text}\n{operation_code.title()}oded  Text: {''.join(output)}"
   


def MultiplicativeCipher():
    output = []
    plain_text_length = len(plain_text)
    k1 = getMultiplicativeInverse(int(key))
    if type(k1) != str:
        for character_index in range(plain_text_length):
            if operation_code == 'enc':
                character_code = ((ord(plain_text[character_index])-ALPHABET_OFFSET)*int(key)) % ALPHABET_LENGTH
            elif operation_code == 'dec':
                character_code = ((ord(plain_text[character_index])-ALPHABET_OFFSET)*k1) % ALPHABET_LENGTH
            else:
                return "Wrong operation code (only 'enc' or 'dec')."
            output.append(chr(character_code+ALPHABET_OFFSET))
    else:
        return k1
    
    return f"Original Text: {plain_text}\n{operation_code.title()}oded  Text: {''.join(output)}"



def AffineCipher():
    output = []
    plain_text_length = len(plain_text)
    k11 = getMultiplicativeInverse(int(key))
    if type(k11) != str:
        for character_index in range(plain_text_length):
            if operation_code == 'enc':
                character_code = ((ord(plain_text[character_index])-ALPHABET_OFFSET)*int(key)+int(second_key)) % ALPHABET_LENGTH
            elif operation_code == 'dec':
                character_code = (((ord(plain_text[character_index])-ALPHABET_OFFSET)-int(second_key))*k11) % ALPHABET_LENGTH
            else:
                return "Wrong operation code (only 'enc' or 'dec')."
            output.append(chr(character_code+ALPHABET_OFFSET))
    else:
        return k11
    
    return f"Original Text: {plain_text}\n{operation_code.title()}oded  Text: {''.join(output)}"


def VigenereCipher():
    output = []
    plain_text_length = len(plain_text)
    key_length = len(key)

    for character_index in range(plain_text_length):
        if operation_code == "enc":
            character_code = ((ord(plain_text[character_index])-ALPHABET_OFFSET)+
                              (ord(key[character_index % key_length])-ALPHABET_OFFSET)) % ALPHABET_LENGTH
        elif operation_code == "dec":
            character_code = ((ord(plain_text[character_index])-ALPHABET_OFFSET)-
                              (ord(key[character_index % key_length])-ALPHABET_OFFSET)) % ALPHABET_LENGTH
        else:
            return "Wrong operation code (only 'enc' or 'dec')."
        output.append(chr(character_code+ALPHABET_OFFSET))

    return f"Original Text: {plain_text}\n{operation_code.title()}oded  Text: {''.join(output)}"


def AutoKeyCipher():
    output = []
    plain_text_length = len(plain_text)
    key_length = len(key)
    plain_textKey_length_difference = plain_text_length-key_length

    if operation_code == "enc":
        if key_length < plain_text_length:
            for i in range(key_length):
                output.append(key[i])
            for i in range(plain_textKey_length_difference):
                output.append(plain_text[i])
            y = ''.join(output)
        else:
            y = key
        output.clear()
        for i in range(plain_text_length):
            t = ((ord(plain_text[i])-ALPHABET_OFFSET)+(ord(y[i])-ALPHABET_OFFSET)) % ALPHABET_LENGTH
            output.append(chr(t+ALPHABET_OFFSET))
    

    elif operation_code == "dec":
        if key_length < plain_text_length:
            y = key
            for i in range(key_length):
                t = ((ord(plain_text[i])-ALPHABET_OFFSET)-(ord(y[i])-ALPHABET_OFFSET)) % ALPHABET_LENGTH
                output.append(chr(t+ALPHABET_OFFSET))
            for i in range(key_length, plain_text_length):
                t = ((ord(plain_text[i])-ALPHABET_OFFSET)-(ord(output[i-key_length])-ALPHABET_OFFSET)) % ALPHABET_LENGTH
                output.append(chr(t+ALPHABET_OFFSET))
        else:
            y = key
            for i in range(plain_text_length):
                t = ((ord(plain_text[i])-ALPHABET_OFFSET)-(ord(y[i])-ALPHABET_OFFSET)) % ALPHABET_LENGTH
                output.append(chr(t+ALPHABET_OFFSET))
                
    else:
        return "Wrong operation code (only 'enc' or 'dec')."
    
    return f"Original Text: {plain_text}\n{operation_code.title()}oded  Text: {''.join(output)}"


'''def HillCipher():
    o=0 
    lp=len(plain_text)
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
                n[i][j]=ord(plain_text[o])-97
                #print(plain_text[o])
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
                r.append(chr(t[i][j]%alphabet_length+97))
        m=''.join(r)
        return "Original Text: "+plain_text+"\nEncoded  Text: "+'''


def HC():
    o = 0
    lp = len(plain_text)
    if lp % 2 == 0:
        lp2 = len(plain_text)//2
    else:
        lp2 = len(plain_text)//2+1
    lk = len(key)
    s = np.zeros((2, 2), dtype=np.int32)
    n = np.zeros((lp2, 2), dtype=np.int32)
    for i in range(2):
        for j in range(2):
            s[i][j] = ord(key[o])-ALPHABET_OFFSET
            if o != lk-1:
                o += 1
    o = 0
    for i in range(lp2):
        for j in range(2):
            if o <= lp-1:
                n[i][j] = ord(plain_text[o])-ALPHABET_OFFSET
                o += 1
            elif lp % 2 != 0:
                n[i][j] = ord('z')-ALPHABET_OFFSET
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
            r.append(chr(t[i][j] % ALPHABET_LENGTH+ALPHABET_OFFSET))
    m = ''.join(r)
    if operation_code == "enc":
        return "Original Text: "+plain_text+"\nEncoded  Text: "+m
    elif operation_code == "dec":
        return "Original Text: "+plain_text+"\nDecoded  Text: "+m


def PlayfairCipher():
    #set up the variables and lists
    l = []
    o = 0
    oo = 0
    #process string to add 'x' between each two repeated characters
    #and add 'x' at the end -if needed- to satisfy (length of prcoessed string)%2==0
    #initialize the matrices with the proper shape
    processed_plain_text = getProcessedPlainText(plain_text)
    processed_plain_text_length = len(processed_plain_text)
    
    s = np.zeros((5, 5), dtype=np.int32)
    n = np.zeros((processed_plain_text_length//2, 2), dtype=np.int32)
    se = set()
    split_key = split(key)
    split_key_length = len(split_key)
    # determines if j or i is used
    se, split_key = jmodeAssign(se, split_key)
    #get a unique character key string and
    #remove its characters from the alphabet
    for i in range(split_key_length):
        se.add(split_key[i])
    for i in range(split_key_length):
        if split_key[i] in se:
            #print(y[i],se,l,se,alphabet)
            #print()
            l.append(split_key[i])
            se.remove(split_key[i])
            alphabet.remove(split_key[i])
    #filling up the matrix s with the result of the previous operations
    #unique key chracters first then the rest of the non used alphabet characters
    #row-wise
    ll = len(l)
    for i in range(5):
        for j in range(5):
            if o < ll:
                s[i][j] = ord(l[o])-ALPHABET_OFFSET
                o += 1
            else:
                s[i][j] = ord(alphabet[oo])-ALPHABET_OFFSET
                oo += 1
    #print(s)
    o = 0
    output = []
    if operation_code == "enc":
        #filling up the matrix n with the characters from the processed string
        #a couple at a time, row wise
        for i in range(processed_plain_text_length//2):
            for j in range(2):
                n[i][j] = ord(processed_plain_text[o])-ALPHABET_OFFSET
                o += 1
        #print(n)
        #after doing that we calculate the encoded character for each of the characters
        #from the couples we made and then make new couples that are the encoded string
       
        for line in n:
            row, col, row1, col1, r, r1 = getOpMatChr(s, line, operation_code)
            output.append(chr(s[int(row)][int(col)]+ALPHABET_OFFSET))
            output.append(chr(s[int(row1)][int(col1)]+ALPHABET_OFFSET))

    elif operation_code == "dec":
        #filling up the matrix n with the encoded string, row wise
        for i in range(processed_plain_text_length//2):
            for j in range(2):
                n[i][j] = ord(processed_plain_text[o])-ALPHABET_OFFSET
                o += 1
        #getting the decoded characters for each of the characters in the encoded string
        #resulting a new string made of decoded couples, that we will most likely
        #have to remove excess 'x's from
                
        for line in n:
            row, col, row1, col1, r, r1 = getOpMatChr(s, line, operation_code)
            output.append(chr(s[int(row)][int(col)]+ALPHABET_OFFSET))
            output.append(chr(s[int(row1)][int(col1)]+ALPHABET_OFFSET))
        
    else:
        return "Wrong operation code (only 'enc' or 'dec')."
    
    return f"Original Text: {plain_text}\n{operation_code.title()}oded  Text: {''.join(output)}"


def ADFGVXCipher():
    #setting up variables, sets, lists and matrices
    AX = ['A', 'D', 'F', 'G', 'V', 'X']
    plain_text_length = len(plain_text)
    l = []
    o = 0
    oo = 0
    #k1=getProcessedString(k1,len(k1))
    s = np.zeros((6, 6), dtype=str)
    se = set()
    #check if key is of the right type
    if type(key) == str:
        y = split(key)
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
                alphabet.remove(y[i])
            except:
                digits.remove(y[i])
    ll = len(l)
    olo = 0
    #filling up the matrix with the key characters first then the rest of the unused alphabet characters
    for i in range(6):
        for j in range(6):
            if o < ll:
                s[i][j] = l[o]
                o += 1
            elif oo < len(alphabet):
                s[i][j] = alphabet[oo]
                oo += 1
            elif olo < len(digits):
                s[i][j] = digits[olo]
                olo += 1
    #print(s)
    if operation_code == "enc":
        cc = []
        #getting the tw v c"o character code for each character in the original text
        for i in range(plain_text_length):
            q = np.where(s == plain_text[i])
            #print(q[0],q[1])
            cc.append(AX[int(q[0])])
            cc.append(AX[int(q[1])])
        #print(cc)
        lk1 = len(second_key)
        sk1 = []
        #sorting the characters of the second key out in a list
        for i in range(lk1):
            sk1.append(second_key[i])
        sk1.sort()
        #print(sk1)
        #figuring out the shape of the second key matrix to initialize it correctly
        if len(cc) % lk1 == 0:
            lkc = len(cc)//lk1+1
        else:
            lkc = len(cc)//lk1+2
        n = np.zeros((lk1, lkc), dtype=str)
        o = 0
        oo = 0
        # fill that matrix with the second key characters in the first column and the two-character-codes
        # in the rest of the columns, in a column-wise filling pattern, and filling what's left with 'A's
        for j in range(lkc):
            for i in range(lk1):
                if oo < lk1:
                    n[i][j] = second_key[oo]
                    oo += 1
                elif oo > lk1-1 and o < len(cc):
                    n[i][j] = cc[o]
                    o += 1
                else:
                    n[i][j] = 'X'
        #print(n)
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
        return "Original Text: "+plain_text+"\nEncoded  Text: "+jj
    elif operation_code == "dec":
        cc = []
        #inserting all of the encdod text characters into a list
        for i in range(plain_text_length):
            #q=np.where(s==p[i])
            #print(q[0],q[1])
            cc.append(plain_text[i])
        #sort the second key characters alphabetically
        lk1 = len(second_key)
        sk1 = []
        for i in range(lk1):
            sk1.append(second_key[i])
        sk1.sort()
        #determine the shape of the matrix n to intialize it
        if len(cc) % lk1 == 0:
            lkc = len(cc)//lk1+1
        else:
            lkc = len(cc)//lk1+2
        n = np.zeros((lk1, lkc), dtype=str)
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
        #print(n)
        #finding out the original order of the two-character codes by comparing each letter
        #to its position in the second key string
        scc = []
        for i in range(lk1):
            q = np.where(n == second_key[i])
            for j in range(1, lkc):
                #print(q[0],q[1])
                scc.append(n[int(q[0])][int(q[1])+j])
        #print(scc)
        #re-filling n with the non-sorted key characters in the first column
        o = 0
        for j in range(lkc):
            for i in range(lk1):
                if o < lk1:
                    n[i][j] = second_key[o]
                    o += 1
        #re-filling the rest of n's columns row-wise with the two-character codes extracted
        o = 0
        for i in range(lk1):
            for j in range(1, lkc):
                if o < len(cc):
                    n[i][j] = scc[o]
                    o += 1
        #print(n)
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
        return "Original Text: "+plain_text+"\nDecoded  Text: "+jj
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
    return algos[algorithm_index]()


if __name__ == "__main__":
    plain_text = sys.argv[1]
    algorithm_index = sys.argv[2]
    operation_code = sys.argv[3]
    if int(algorithm_index) != 6:
        key = sys.argv[4]
    else:
        try:
            key = sys.argv[4]
        except:
            key = ''
    if int(algorithm_index) == 2 or int(algorithm_index) == 7:
        second_key = sys.argv[5]
    elif int(algorithm_index) == 6:
        try:
            jmode = ast.literal_eval(sys.argv[5])
        except:
            jmode = False
    else:
        pass
    print(navigator())
