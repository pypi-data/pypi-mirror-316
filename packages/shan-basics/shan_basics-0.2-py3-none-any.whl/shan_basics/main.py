def print_python_basics():
    a = r"""
    
    print("Hello my crazy people!")
print("Ive done it, Yesssss!!!!")
print("Hello World")
print("............................................................................")
#Calculator
print(2*3)
print(2/3)#division gives float_conversion
print(2+3)
print(2-3)
print(2%3)
print(2**3)
#or
a = pow(2,3)
print(a)
print("............................................................................")
#data_types
a= "stringA" + "+" + "stringB"
b= 2
print(a)
print(type(a))
print(b)
print(type(b))
#c=a+b is not possible
print("............................................................................")
#type_conversion
#float_conversion
i=100
print(i)
print(type(i))
j = float(i)
print(j)
print(type(j))
print("adding")
print(float(i) + 100 + 100.3)
print(int(83.9))
#string_conversion
a="222"
b= int(a)
print(a)
print(type(a))
print(b)
print(type(b))
#same is not valid when string has alphabets i.e a="alphabets "
print("............................................................................")
#input
ques = input("Hello my friend, whats your name?")
print("You've got a beautiful name",ques + ".", "Nice to meet you. My name is CARE")
#input type conversion for addition, subtraction,...
ques2 = input("I am a newly born AI. How old are you?")
ques2a = int(ques2) - 1
print("Woah! You are", ques2, "years old", "So you are one year older than SAM who is", ques2a, "years old")
print("............................................................................")
#Assignmnet
c = input("What is the total no of days, you worked?")
print("Given you worked", c , "no of days")
d = input("What is the rate you earn per day?")
print("Given you earn at a rate of", d , "per day")
print("So you earn a total of",int(c)*float(d),"currency as per given data")
print("............................................................................")
#Comparisions
# e == f, e != f or  e <> f, e > f, e < f, e >= f, e <= f....if or elif or else should be followed by ':'
x = float(input("Input the value of x"))
if x>=4:
    if x>4:
        print("x is greater than 4")
    else:
        print("x is equal to 4")
else:
    print("x is less than 4")

z = input("Enter the value of y")
y = float(z)
if y>4:
    print("Greater than four")
elif y==4:
    print("Equal to four")
else:
    print("Less than 4")
#if else for string
name = input("Enter your login id")
if name=="shan4smiles":
    print("Welcome Shanmukha Dhanush")
else:
    print("Incorrect ID entered.")
print("............................................................................")
#if else for input() --> try except ---------> input by user can be number or alphabet
####for input only as numbers
x = input("Enter your age number")
try:
    x=int(x)
except:
    x = -1

if x>0:
    print("You have entered a positive number", x, "as your age number")
elif x==0:
    print("You have entered zero-a neutral number as your age number")
else:
    print("please enter numbers only. Alphabets are not supported by our system")
####try except for non-input functions --> xtra
a = "Hello"
try:
    b = int(a) + 1
except:
    b = -1
print("Helo",b)
####application --> where things are not defined, to avvoid syntax error
#simple for non input functions
try:
    s = 4/0
    print("Your division is successful")
except:
    s = -1

if s==0:
    print("0 divided by anything is zero", s)
elif s>0:
    print("the quotient is a positive number", s)
else:
    print("Anything divided by o is undefined")
#simple - for input may be given as numbers only (negative ans not supported)
m = float(input("Enter a positive divident"))
n = float(input("Enter a positive divisor"))

try:
    o = m/n
except:
    o = -1

if o>=0:
    if o==0:
        print("0 divided by anything is zero")
    else:
        print("The quotient is", o)
else:
    print("0 as divisor is not supported")
#simple2 - for input may be given as numbers or alphabets (negative ans not supported)
print("............................................................................")
#doubt1
a = "abc"
b = 0

try:
    b = int(a)
except:
    b = -1

print(b)
print("............................................................................")
#unknown errors case
import sys
while True:
    a = input("Enter")
    try:
        b = float(1)/float(a)
        break
    except:
        print(sys.exc_info, "error")
print("Done", b)

print("............................................................................")
#functions
def example():
    print("example statement")
def example2():
    print("example statement 2")

example()
print("Hello Krazies")
example2()
#functions with input
def intro1():
    ques = input("Hello my friend, whats your name?")
    print("You've got a beautiful name",ques + ".", "Nice to meet you. My name is CARE")
def intro2():
    ques2 = input("I am a newly born AI. How old are you?")
    ques2a = int(ques2) - 1
    print("Woah! You are", ques2, "years old", "So you are one year older than SAM who is", ques2a, "years old")

print("printing intro 1")
intro1()
print("printing intro 2")
intro2()
intro1()
intro2()
#functions with PARAMETERS
def Hello(language):
    if language == "english":
        print("Hello")
    elif language == "french":
        print("Hola")
    elif language == "turkish":
        print("Merabha")
    elif language == "hindi":
        print("Salem")
    elif language == "telugu":
        print("Namaste")
    else:
        print("Language un-identified")
print("Examples")
Hello("eng")
Hello("telugu")
#application of even EvenOdd
def EvenOdd(num):
    a = num%2
#or directly:--> if num%2 == 0:
    if a == 0:
        print(num, "is a even number")
    else:
        print(num, "is a odd number")

EvenOdd(5)
EvenOdd(4)
print(".......................................................................")
#return
def example():
    print("example statement")
def example2():
    return "example statement 2"

example()
print("Hello Krazies", example2())
###Here if we replace example2() with example(), then the result would be different & also we cannot use example2() like how we can use example()
# return is for calling the function so that we can add something more to the function, whereas def-with-print is just for simply printing (returning) exactly what is written
#return always needs print i.e print(example2())
#.
#that is for below code it appers result as Hello Krazies string_conversion
def example():
    print("example statement")
def example2():
    print("example statement 2")

example()
print("Hello Krazies", example2())
print(".......................................................................")
#more tha 1 PARAMETERS
#addition of parameters is possible for both strings and numbers, but not multiplication. And also input parameters should be same as mentioned parameters.
def addition(a,b,c):
    d = a+b+c
    return d

print(addition(2,3,5))
print(addition("hi", "fellow", "mate"))
print(".......................................................................")
#assignment tricks #repetition
def ass(m,n):
    a = m*n
    return a
ass("helo",5)
#or
def ass(m,n):
    print(m*n)
ass("helo",5)
#prints helo 5 times
print(".......................................................................")
#loops and iterations
#while
a = 0
while a<3: #or--> while (a<3):
    a = a+1
    print("helo")
#example2
a = 0
while a<10:
    a = a+1
    if a%2==0:
        print(a,"even")
    else:
        print(a,"odd")
#while true:
#breaking out of while loop  --> break
while True:
    line = input("Enter the work progress")
    if line == "done":
        break#breaks loop here
    print("only", line, "percentage is done. Keep working")
print("congo, your work is done")
#entering to start of loop --> continue
while True:
    line = input("Login")#input should be inside while true only
    if line[0] == "#":
        continue
    if line == "done":
        break
    print("your progress is", line)
print("Your work is done")
#for loops
for s in [1,2,3,4,5]:
    print (s)
#example2
a = [1,2,3,4,5]
for i in a:
    if i%2==0:
        print(i, "is even")
    else:
        print(i, "is odd")
#question
#find greatest
a = [9,41,12,3,74,15]
b = -1
for i in  a:
    if i>b:
        b = i
print(b)
#least number
a = [9,41,3,12,74,15]
b = None
for i in  a:
    if b is None:
        b = i
    elif i<b:
        b=i
        print(b) #or directly print(i), after elif statement{b will not be changed}
        #or by finding greatest
a = [9,41,12,3,74,15]
b = -1
for i in  a:
    if i>b:
        b = i
print(b)

for j in a:
    if j<b:
        b = j
print(b)
#find number of digits
a = [9,41,12,3,74,15]
print(len(a))
    #or
a = [9,41,12,3,74,15]
count = 0
for i in a:
    count = count + 1
print(count)
#addition
a = [9,41,12,3,74,15]
b = 0
for i in a:
    b = b + i
print(b)
#multiplication
a = [9,41,12,3,74,15]
count = 1
for i in a:
    count = count * i
print(count)
#average
a = [9,41,12,3,74,15]
b = 0
c = 0
for i in a:
    b = b + i
    c = c + 1
print(b/c)
#or
a = [9,41,12,3,74,15]
b = 0
for i in a:
    b = b + i
print(b/len(a))
print("........................................................................")
#filtering in python
#greater than x
a = [9,41,12,3,74,15]
for i in a:
    if i>20:
        print(i)
#less than x
a = [9,41,12,3,74,15]
for i in a:
    if i<20:
        print(i)
print("........................................................................")
#search
a = [9,41,12,3,74,15]
b = a.index(15) + 1
for i in a:
    if i==15:
        print(b, "th element is the number 15")
    else:
        print(i, "is not 15")
        #or
a = [9,41,12,3,74,15]
for i in a:
    if i==12:
        print(i, "is present")
    else:
        print(i,"nope")
#xtra
a = [9,41,12,3,74,15]
b = a.index(15)
c = b+1
print(c,"th element is the number 15")
print("........................................................................")
#miscellaneous
b = 0
c = 1
d = 0
while True:
    a = input("Enter")
    if a =="exit":
        break
    try:
        a = int(a)
    except:
        print("invalid")
        continue
    b = a+b
    c=c*a
    d=d+1
print("sum is", b)
print("product is", c)
print("count is", d)
print("average is", b/d)
print("........................................................................")
#Strings
#index_inside
s = input("enter any three unit word/number")
b = s[0]
c = s[1]
d = s[2]
print("the letter one is", b)
print("the letter two is", c)
print("the letter three is", d)
#len_of_string
print("The length of string", len(s))
print("........................................................................")
#printing_all_index
s = input("enter any three unit word/number")
q = len(s)
for i in range(0,q):
    print(s[i])
#or
s = input("enter any three unit word/number")
for i in s:
    print(i)
print("........................................................................")
#using count to find number of letters
a = input("enter")
b = 0
for i in range(0,len(a)):
    if a[i]=="a":
        b = b+1
print(b)
#or
a = input("enter")
b=0
for i in a:
    if i =="a":
        b=b+1
print(b)
#using count to find number of letters --> method 2 --> using loops XXXXXXXXXXXXXXXXXXXXXXXXXXtra
while True:
    a = input("enter")
    b = 0
    if a == "done":
        break
    else:
        for i in range(0,len(a)):
            if a[i]=="a":
                b = b+1
        print(b)
print("........................................................................")
#to print only in needed index range
a = input("enter")
b = a[2:5] #index 5 is not-included
print(b)
#or
a = input("enter")
for i in range(2,len(a)):
    if i>5:  #index 5 is included
        break
    else:
        print(a[i])

#to find letters only in needed index range
a = input("enter")
b = 0
for i in range(0,len(a)):
    if i>2:
        if a[i] == "l":
            b = b + 1
print(b)
print("........................................................................")
#print every 5th letters
a = input("enter")
print(a[::5])
#from one index to another every 5th letters
a = input("enter")
b = a[2:27:5]
print(b)
print("........................................................................")
#print all string reverse
a = input("enter")
print(a[::-1])
#print string in reverse upto needed only
a = input("enter")
b = a[2::-1]
print(b)
#print string in reverse in a range
a = input("enter")
b = a[4:2:-1]
print(b)
print("........................................................................")
#finding if present or not
a = input("enter")
print("n" in a)
#or
a = input("enter")
if "a" in a:
     print("has a")
else:
     print("no a")
print("........................................................................")
#making and checking upper or lower
a = input("enter")
b = a.isupper()
c = a.islower()
d = a.upper()
e = a.lower()
print(a,b,c,d,e)
print("........................................................................")
#remove strips
a = input("enter content with strips left and right")
b = a.lstrip()
c = a.rstrip()
d = a.strip()
print(b,c,d)
print("........................................................................")
#data mining or data sorting
#finding a specific name
a = "shanmukhadhanush27@gmail.com"
b = a.find("d")
print(b)
c = a.find("2",b)
print(c)
d = a[b:c]
print(d)
##.find()
b = "helolkmokl"
a = b.find("o")
print(a)
print(b.find("l",a))
print(b.find("l",6))
print(b.find("p"))

#defining above data sorting
def mining(a,m,n):
    a
    b = a.find(m)
    print(b)
    c = a.find(n,b)
    print(c)
    d = a[b:c+1]
    print(d)
print(mining("abcdef","b","d"))
print("........................................................................")
#Assignment
a = "Perfect-PLAN-B:0.7541"
b = a.find(":")
c = a[b+1:len(a)+1]
print(c)
d = float(c)
print(d)
e = int(d) #string to int is via float only
print(e)
    
    
    
    """

    return a


def print_python_files():
    a = r"""
    
        
    #Files
#file_opening
a = open(r'C:\Users\DELL\Python\Notes.txt')
count = 0
for i in a:
    count = count +1
    print(i)
#a = open(r'C:\Users\DELL\Python\Notes.txt', 'r')
#a = open(r'C:\Users\DELL\Python\Notes.txt', 'a')
#a = open(r'C:\Users\DELL\Python\Notes.txt', 'w')
#a = open(r'C:\Users\DELL\Python\Notes.txt', 'x')
#Lines in a file
print(count)
#file_casing
a = open(r'C:\Users\DELL\Python\Notes.txt')
for i in a:
    print(i.upper())
    print(i.lower())
    print(i.isupper())
    print(i.islower())
#file.read()
a = open(r'C:\Users\DELL\Python\Notes.txt')
b = a.read()
##as a string
print(b)
##len of characters in string
print(len(b))
##Slice
print(b[:10])
print(len(b[:10]))
##search
if "is" in b:
    print("Yes")
else:
    print("No")
#file line search
a = open(r"C:\Users\DELL\Python\Notes.txt")
for i in a:
    print(i)
    print(i.rstrip())
    print(i.lstrip())
#file line search
##startswith() and endswith()
a = open(r"C:\Users\DELL\Python\Notes.txt")
for i in a:
    i = i.lstrip()
    i = i.rstrip()
    if i.startswith("1"):
        print(i)
    if not i.startswith("1"):
        print("nah")
    if i.endswith("slicing"):
        print('Here', "\n")
    if not i.endswith("slicing"):
        print("Not here","\n")
a = open(r"C:\Users\DELL\Python\Notes.txt")
for i in a:
    if not i.startswith("2"):
        continue
    print(i)
a = open(r"C:\Users\DELL\Python\Notes.txt")
for i in a:
    if not i.startswith("2"):
        print(i)
#Searching_files/Naming files
input = input("Name?")
try:
    a = open(input)
except:
    print("File not found")
    quit()
count = 0
for i in a:
    i = i.strip()
    if i.startswith("1"):
        count = count + 1
print(count)
#Assignment_files
a = open(r"C:\Users\DELL\Python\files.txt")
for i in a:
    print(i.upper())
print("........................................................................")
    
    """

    return a

def print_python_lists():
    a = r"""
#lists
a = ["Balarama", "Sree", "Shan", "Asthra"]
print(a)
a[2] = "Shan"
print(a)
#len and range of a
a = [1,2,3,4,5]
for i in range(len(a)):
    print("the number are", a[i])
alpha = ["a","b","c","d","e"]
for i in alpha:
    print("The alphabets are", i)
#lists and use cases
#list slicing
a = [0,1,2,3,4,5,6]
b = a[:]
print(b)
b = a[2:6]
print(b)
b = a[2:]
print(b)
b = a[:6]
print(b)
b = a[::2]
print(b)
b = a[::-2]
print(b)
b = a[2:6:2]
print(b)
b = a[6:2:-2]
print(b)

s = [0,1,2,3,4]
print(s)
#appending
s.append(5)
s.append(6)
print(s)
#slicing
print(s[5:1:-1])
#searching
print(6 in s)
print(6 not in s)
#sorting
s = ["1","2"]
s.append("-1")
s.append("ba")
s.append("ab")
print(s)
s.sort()
print(s)
#sum_and_average_miscelleaneous
s = list()
while True:
    num = input("Enter")
    if num == "done":
        break
    else:
        num = int(num)
        s.append(num)
print(sum(s)/len(s))
#sum_and_average_miscelleaneous_2
s = list()
while True:
    num = input("Enter")
    if num == "done":
        break
    else:
        num = int(num)
        s.append(num)
try:
    a= sum(s)/len(s)
except:
    a = print("Empty list")
print(sum(s))
print(a)
#sum_and_average_miscelleaneous_3
s = list()
while True:
    num = input("Enter")
    if num == "done":
        break
    else:
        try:
            num = int(num)
        except:
            num=0
        s.append(num)
try:
    a= sum(s)/len(s)
except:
    a = print("Empty list")
print("Sum is",sum(s),"alphabets are not considered for sum")
print("Average is",a,"alphabets are considered for average")
#splitting
str = input("Enter a sequence of strings")
list = str.split()
print(list)
for i in list:
    print(i)
str2 = input("Enter a sequence of strings with semi-colons")
list2 = str2.split("/")
print(list2)
for i in list2:
    print(i)
#double_split
a = input("Enter your email ID in form od-'From-email-To-email'")
b = a.split("-")
print(b,"\n")
print("The reciever mail is",b[1],"\nThe sender mail is ",b[3])
#searching_in_lists
a = input("Enter your email ID in form od-'From-email-To-email'")
b = a.split("-")
count = 0
for i in b:
    count = count +1
    if i=="From":
        print("The",count,"time string satisifies condition")
    else:
        print("The",count,"time string does not satisify the condition")
#remove_#index_#append_#replace
a = input("Enter your email ID in form od-'From-email-To-email'")
b = a.split("-")
b.append("falthooz")
b.append("flix")
print(b)
print(b.index("flix")+1)
b.remove("falthooz")
b[2]="given"
print(b)
#Assignment_lists
#method1
a = open(r"C:\Users\DELL\Python\files.txt")
for i in a:
    b = i.find("net ")
    print(i[b+4:b+7])
#method2
a = open(r"C:\Users\DELL\Python\files.txt")
for i in a:
    i = i.split()
    print(len(i))
    if len(i)<3 or i[0]!="From":
        continue
    print(i[2])

print("..........................................................................")
    
    """

    return a

def print_python_dicts():
    a = r"""
    
    #dictionaries
a = list()
a.append("n")
print(a)
a = dict()
a["python"]=1
a["javascript"]=2
a["c++"]=3
a["c"]=4
a["ruby"]=5
print(a["python"])
a["ruby"]=a["c++"]
print(a)
#addition_in_dictionaries
a = dict()
a["C"]=1972
a["SQL"]=1979
a["C++"]=1985
a["Python"]=1990
a["R"]=1993
a["Java"]=1995
a["JavaScript"]=1995
a["PHP"]=1995
a["Ruby"]=1995
print(a)
a["C"]=a["C"]+a["C++"]
print(a)
a["C"]=a["C"]-a["C++"]
print(a)
#dictionary_literal or constant
dict = {"a":1, "b":2, "c":3, "d":4, "e":5}
print(dict)
dict["f"]=6
print(dict)
dict["f"]=dict["f"]+1
print(dict)
dict["e"]=dict["e"]+1
print(dict)
#dict_by_input
list = dict()
while True:
    a = input("Input Keyword")
    if a=="done":
        break
    else:
        b = int(input("Keyword's value"))
        list[a]=b
print(list)
#use_case_of_dictionaries--> get()
a = dict()
b = input("Enter the items in purse")
c = b.split()
#""""c.sort()"""" can also be used here
print("words:",c)
print("Counting no of each items")
for i in  c:
    a[i] = a.get(i,0)+1
print("words:",a)
#or
a = dict()
c = ["a", "a", "b", "b", "ab", "ab", "ba"]
print("words:",c)
print("Counting no of each items")
for i in c:
    a[i]=a.get(i,0)+1
print(a)
#get_using
dict = {"C":1972, "SQL":1979, "C++":1985, "Python":1990, "R":1990, "JavaScript":1995, "Java":1995, "Ruby":1995, "PHP":1995}
print(dict.get("g",1))
print(dict.get("C",1))

#Printing_different_items_in_a_dict
#method_1
dict = {"C":1972, "SQL":1979, "C++":1985, "Python": 1990, "JavaScript":1995}
print("Printing dict\n",dict)
print("Printing list\n",list(dict))
print("Printing keys\n",dict.keys())
print("Printing values\n",dict.values())
print("Printing items\n",dict.items())
#method_2
#for_loop_1
dict = {"C":1972, "SQL":1979, "C++":1985, "Python":1990, "R":1990, "JavaScript":1995, "Java":1995, "Ruby":1995, "PHP":1995}
for i in dict:
    print(i,dict[i])
#method_3
#for_loop_2
dict = {"C":1972, "SQL":1979, "C++":1985, "Python":1990, "R":1990, "JavaScript":1995, "Java":1995, "Ruby":1995, "PHP":1995}
for a,b in dict.items():
    print("\n the keys is\n",a,"\n and the values is\n",b)
#Assignment_dictionaries
##method_1
f = open(r"path")
d = {}
for i in f:
    l = i.split()
for i in l:
    d[i] = d.get(i,0)+1
print(d)

num = None
for m,n in d.items():
    if num == None:
        num = n
    elif n>num:
        num = n
D = {}
for i,j in d.items():
    if j==num:
        D[j]=i
print("Maximum occurence",D)
#method_2
#Assignment_dictionaries
f = open(r"path")
d = {}
for i in f:
    l = i.split()
for i in l:
    d[i] = d.get(i,0)+1
print("dictionary\n",d)
l = []
for m,n in d.items():
    set = (n,m)
    l.append(set)
print("Original list \n",l)
l = sorted(l, reverse = True)
print("Sorted list \n",l)
print(l)
print("Max\n",l[0])

print(".............................................................................................")
    
    """

    return a

def print_python_tuples():
    a = r"""
    
    #tuples --> dict.items()
#tuples_are_not_mutable
a = (2,3,1,5,4)
print(a)
#max_of_tuples
print(max(a))
#min_of_tuples
print(min(a))
#Comparisions_of_tuples
(x,y)=("a","b")
print(x)
#or
x,y = "a", "b"
print(x)
#True_or_False_of_tuples
print((4,5,6)>(1,10,11))
print("..........................................................................")
#sorted_of_tuples
print(sorted(a))
#reverse_sorting_of_tuples
print(sorted(a, reverse=True))
#sorting_by_keys
t = {"C":1972, "C++":1985, "Python":1990, "Java": 1995}
t1 = t.items()
print(sorted(t1))
#reverse_sorting_by_keys
t = {"C":1972, "C++":1985, "Python":1990, "Java": 1995}
t1 = t.items()
print(sorted(t1, reverse=True))
#sorting_by_values
t = {"C":1972, "C++":1985, "Python":1990, "Java": 1995}
t1 = t.items()
print(sorted([(b,a) for a,b in t1]))
#reverse_sorting_by_values
#using_dynamically
t = {"C":1972, "C++":1985, "Python":1990, "Java": 1995}
t1 = t.items()
print(sorted([(b,a) for a,b in t1], reverse=True))
#or
#using_loops
t = {"C":1972, "Java": 1995, "C++":1985, "Python":1990}
l = dict()
for a,b in t.items():
    l[b]=a
print(l)
#using_loops_2
t = {"C":1972, "Java": 1995, "C++":1985, "Python":1990}
l = list()
for a,b in t.items():
    l.append((b,a)) #-------------> double paranthesis are compulsory
print(l)

print("..........................................................................")
#Problem
##sorting_with_keys
t = {"C":1972, "C++":1985, "Python":1990, "Java": 1995}
t1 = t.items()
t2 = sorted(t1)
t3 = sorted(t1, reverse=True)

print("Printing tuples\n",t1)
print("Printing sorted tuples\n",t2)
print("Printing reverse sorted tuples\n",t3)

print("\nPrinting tuples in a loop\n")
for a,b in t1:
    print(a,b)
print("\nPrinting tuples in a loop - sorted\n")
for a,b in t2:
    print(a,b)
print("\nPrinting tuples in a loop - reverse sorted\n")
for a,b in t3:
    print(a,b)
##sorting_with_values
t = {"C":1972, "Java": 1995, "C++":1985, "Python":1990}
l = dict()
for a,b in t.items():
    l[b]=a
print(l)
#or
#t = {"C":1972, "Java": 1995, "C++":1985, "Python":1990}
#l = list()
#for a,b in t.items():
#    l.append((b,a)) -------------> double paranthesis are compulsory
#print(l)


l1 = l.items()
l2= sorted(l1)
l3= sorted(l1,reverse=True)

print("Printing tuples\n",l1)
print("Printing sorted tuples\n",l2)
print("Printing reverse sorted tuples\n",l3)

print("\nPrinting tuples in a loop\n")
for a,b in l1:
    print(a,b)
print("\nPrinting tuples in a loop - sorted\n")
for a,b in l2:
    print(a,b)
print("\nPrinting tuples in a loop - reverse sorted\n")
for a,b in l3:
    print(a,b)
print(".........................................................................")
## NOTE:
t = {"C":1972, "Java": 1995, "C++":1985, "Python":1990}
# t = t.keys()
#print(t[0]) --------->not applicable to dictionaries
t = (1,2,3,4,5)
print(t[0])
t = [1,2,3,4,5]
print(t[0])
#Assignment_tuples
f = open(r"C:\Users\DELL\Python\files.txt")
d = {}
for i in f:
    l = i.split()
for i in l:
    d[i] = d.get(i,0)+1
print(d)
#partB
#method_1
D = {}
for a,b in d.items():
    D[b] = a
print(D)
Dd ={}
for i in sorted(D, reverse =True):
    Dd[i] = D[i]
print(Dd)
#method_2
l = []
for a,b in d.items():
    set = (b,a)
    l.append(set)
print(sorted(l,reverse = True))
print(".........................................................................")
    
    """

    return a

def print_python_sets():
    a = r"""
    
    #set
s = {1,2,3,4,5}
print("Simple Sets\t",s)
#set_dont_promote_duplicate
s = {1,2,3,4,3,5,5,4,6}
print("With duplicates filtered\t",s)
#sets_do_not_promote_mutable_items_like_lists_or_dictionaries
#sets_do_promote_non_mutable_items----(mixed_elements_too)----like all of strings, integers, floats, tuples
s = {"hello", 1, 1.0, (1,2,"3")}
print("With mixed elements\t",s)
#appending_sets_from_list
t = [1,2,3,4,5]
s = set(t)
print("As lists\t",s)
#appending_sets_from_dict
d = {"C":1975, "C++":1985, "Python": 1990}
D = [(b,a) for a,b in d.items()]
s = set(d)
S = set(D)
print("With keys\t",s)
print("With values\t",S)
#data_type_of_list
a = {}
b = []
c = ()
d = dict()
e = list()
f = set()
print(type(a),type(b),type(c), type(d), type(e), type(f))
#modifying_sets
s = set()
#add()
s.add("C")
s.add("Python")
s.add(100)
print(s)
#update()
#----> can include strings, list, dict, string+list+dict,
#----> eliminates duplicates
#----> cannot include integers at all
#----> using update without list/dicts --> i.e for strings results in printing the strings as letter wise.
s.update("C++", "javascript")
print(s)
s.update(["C++", "javascript"])
print(s)
s.update({"PHP":1995, "Rubu":1990})
print(s)
#update([])----> is also used for including mutable items in a list {provided only them}
s.update('amanda', [1,2,3], {"amandaaaaaaa": 1})
print(s)
print(".........................................................................")
s = {"C", "C++", "Python"}
print(s)
#remove----> shows syntax error if set doesnt contain the element
s.remove("C")
print(s)
s.add("C")
#s.remove("React")-----> shows syntax error
print(".........................................................................")
#discard ----> shows no syntax error if set doesnt contain the element
s.discard("C++")
print(s)
s.update("C")
#s.discard("React")-----> shows no syntax error
print(s)
print("..........................................................................")
#pop() -------------> removes the last element in the set ----> {The last element can be anything, cause elements are unordered in sets, thus we can us eit to find the last element in the set too}
#pop() is similar to add, as it can remove 1 element only from the set {the last element}
s = {"C", "C++", "Python","JavaScript"}
print(s)
a = s.pop()
print("Removing 1st element\t",a)
print(s)

b = s.pop()
print("Removing 2nd element\t",b)
print(s)

c = s.pop()
print("Removing 3rd element\t",c)
print(s)

s.add(a)
print("Adding 1st element back")
print(s)

s.update([b,c])
print("Adding 2nd and 3rd elements back")
print(s)
print(".................................................................")
#clear() ----> used to clear the whole set
#clear() is similar to update as it removes more than 1 element from the set {all the elements}
#del ---> deletes the whole sets
#A] clear()
s = {"C", "C++", "Python"}
print(s)
s.clear()
print(s)
#B] del
del s
try:
    print(s)
except:
    print("set is deleted")
print(".................................................................")
#Use_case_of_sets
#union---> "|"
setA = {1,2,3}
setB = {"a", "b", "c", 1,2,3}
print("Printing union 1",setA.union(setB))
print("Printing union 2",setA|setB)
#intersection---> "&"
setA = {1,2,3}
setB = {"a", "b", "c", 1,2,3}
print("\nPrinting intersection 1",setA.intersection(setB))
print("Printing intersection 2",setA&setB)
#difference---> "-"
setA = {1,2,3}
setB = {"a", "b", "c", 1,2,3}
print("\nPrinting A-B")
print("Printing difference 1",setA.difference(setB))
print("Printing difference 2",setA-setB)
print("\nPrinting B-A")
print("Printing difference 1",setB.difference(setA))
print("Printing difference 2",setB-setA)
#symmetric_difference---> "^"
#{remaining elements of setA and setB intersection}
setA = {1,2,3,4,5,6}
setB = {"a", "b", "c", 1,2,3}
print("\nPrinting symmetric_difference 1",setA.symmetric_difference(setB))
print("Printing symmetric_difference 2",setA^setB)
#finding_element_in_a_set_yes_or_no
set = {1,2,3, "a", "d"}
print(3 in set)
print(3 not in set)
print("d" in set)
print("d" not in set)
#or
for i in set:
    if i=="a":
        print(i)
    else:
        print("not a")
#len()_in_a_set
set = {1,2,3,4,5}
print("len of set is ",len(set))
#frozen_set ----> Immutable
#frozen_set_do_not_take_add/update/remove/discard/clear
set = {1,2,3}
print(set)
Set = frozenset(set)
print(Set)
#or
Set = frozenset([1,2,3])
print(Set)
try:
    m = set.add("aaaaaaaaaaaaaaa")
except:
    print("noooooooooooooooo")
print(set)

try:
    m = Set.add("bbbbbbbbbbbbbbbbb")
except:
    print("niiiiiiiiiiiiiiiii")
del Set
try:
    print(Set)
except:
    print("Set is deleted")
#representation_of_set
s = set((1,2,3))
s = set([1,2,3])
s = set({1,2,3})
s = {4,5,6}
#sets can have only 1 argument in them when set() func is used---> below is invalid
#s = set([1,2], [2,1])
#s*3
    
    """

    return a

def print_python_new():
    a = r"""
    
    #Python_math_from_instagram
print("Printing max",max(1,2,3))
print("Printing min",min(1,2,3))
print("Printing abs",abs(-123))
print("Printing power",pow(2,3))
import math
print("Printing sqrt",math.sqrt(4))
print("Printing ceil",math.ceil(5.5))
print("Printing floor",math.floor(5.5))
print("Printing pi",math.pi)
#emojis
print("\U0001F917")
print("\U0001F62A")
print("\U0001F637")
print("\U0001F618")
print("\U0001F600")


#comparision of sets

# Args and Kwargs
# args = '*'
# to allocate a variable list of values in def
def sum(*a):
    sum = 0
    for i in a:
        sum+=i
    return sum
a = sum(5,1,5)
print(a)
# kwargs = '**'
# to allocate variable dictionary of values in def
def dicto(**a):
    sum = 0
    for key,value in a.items():
        print(key)
        sum+=value
    print(sum)
dicto(a=1,b=2)

# Operations:
print(np.random.random(10).cumsum())

# NEW
# printing in a matrix form
l = [[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1]]
for i in l:
    print(*i)
# making a alist of n similar elements
l = [1]*5

    
    """

    return a

# ----------------------------------------------------------------------------------------------------------------------
def print_python_libraries():
    a = r"""
    Pandas:

  pd.Timestamp.now() ===> current date via pandas
  pd.Categorical(df['label']).codes ===> label encoding via pandas
  from sklearn.preprocessing import LabelEncoder
  df['label'] = LabelEncoder.fit_transform(df['label'])

  Pandas_codes():
    import pandas as pd
    df1 = pd.DataFrame({'marks':[80,90,100], 'rank': [3,2,1]}, index = ['StudentA', 'StudentB', 'StudentC'])
    print(df1)
    df2 = pd.DataFrame({'grade':['C','B','A'], 'rank': [3,2,1]}, index=[1,2,3])
    print(df2)
    df = pd.merge(df1,df2,on='rank')
    print(df)
    df3 = pd.DataFrame({'CGPA':[8,9,10]})
    df_ = pd.concat([df,df3]) # df.append(df3) works the same
    print(df_)
    df_= pd.concat([df,df3], axis=1)
    print(df_)
    print(df_.corr())
    import seaborn as sns
    import matplotlib.pyplot as plt
    map = sns.heatmap(df_.corr(), annot = True, cmap = 'coolwarm', linewidths = 10) #linewidths = space b/w each box, annot is used to show names on boxes
    #plt.show()
    change = {'A':1.0,'B':2.0,'C':3.0}
    df_['grade'] = df_['grade'].map(change)
    print(df_)
    print(df_.dtypes)
    df_ = df_.rename(columns = {'CGPA':'Point'})
    print(df_)
    df4 = pd.DataFrame({'Status':['follower', 'follower', 'leader']})
    df_ = pd.concat([df_,df4], axis = 1)
    print(df_)
    df5 = pd.get_dummies(df_['Status'])
    print(df5)
    df_ = pd.concat([df_,df5], axis = 1)
    print(df_)
    print(df_.shape)
    a = [1,2,3,4]
    _df = pd.Series(['a','b','c'], index = [1,2,3], name = 'Series')
    print(_df)

    fruit = ['Apple', 'Orange', 'Grapes']
    rate = [80, 45, 40]
    health = ['A', 'B', 'C']
    shop = pd.Series(rate, fruit) # right
    # shop = pd.Series(rate, fruit, health) # wrong
    shopee = pd.DataFrame(rate, fruit)
    print(shop)
    print(shopee)
    print(".................")
    df_=pd.read_csv(r"C:\Users\DELL\Desktop\Mini_project2\water_potability.csv")
    print(df_.columns, df_.describe, df_.info)

    import pandas as pd
    import numpy as np
    df = pd.read_csv(r'C:\Users\DELL\Downloads\wine.csv')
    # changing all values of a data frame by a specific formuls
    df['quality_Q'] = df['quality'].apply(lambda x:x*100)
    # or
    df['quality_QQ'] = df['quality'].map(lambda x:x*1000)
    #or
    df['quality_QQQ'] = df['quality'] * 10000
    print(df[['quality', 'quality_Q', 'quality_QQ' ,'quality_QQQ']])
    print(df)
    print(df.quality_QQ.unique())
    df.apply(lambda x: x*100)
    print(df)

    import pandas as pd
    import numpy as np
    df = pd.DataFrame(np.random.rand(5,3), index=[5,3,2,4,1], columns = list('ABC'))
    # for a specific row
    print(df)
    print(df.loc[1]) #for a specific index calling wrt no
    print(df.iloc[1]) # for a specific index calling wrt location {location starts from 0}
    #Sorting
    print(df.sort_index())
    print(df.sort_index(ascending = False))
    #Slicing
    df = df.sort_index()
    print(df.head(3))
    print(df.tail(3))
    print(df[1:4])

    import pandas as pd
    import numpy as np
    df = pd.DataFrame([[10,15,12], [np.NaN, 13, 10], [14, np.NaN, 13], [np.NaN, np.NaN, 14], [13,12,11]], index = [1,2,3,4,5], columns = ['A', 'B', 'C'])
    print(df)
    df1 = df.dropna(subset = ['col name'], axis = 0 , inplace - True) # list wise deletion
    print(df1)
    df2 = df.dropna(subset = ['col name'], axis = 1 , inplace - True) # pair wise deletion
    print(df2)

    df = df['col name']
    df4 = df.fillna(method = 'ffill')
    print(df4)
    df5 = df.fillna(method = 'bfill')
    print(df5)
    df3 = df.fillna(0)
    print(df3)
    df6 = df.fillna(df.mean()) #or df.median / df.mode() / df.max() / df.min()
    print(df6)
    df10 = df.replace(np.nan, df.mean())

    print(df.isnull().sum())
    #df7 = df.fillna(subset = ['B']) ???????????????????????????????????????
    #print(df7) ??

    import pandas as pd
    import numpy as np
    df = pd.read_csv(r'C:\Users\DELL\Downloads\wine.csv')
    print(df.describe(include = 'all')) # include = 'all' implies all the columns must be considered for describing
    print(df.info())
    print(df[['pH', 'type']].groupby(['type'], as_index=False).mean())
    print(df[['pH', 'type']].groupby(['type'], as_index=True).mean())
    print(df[['type', 'quality', 'density']].groupby(['type', 'quality'], as_index = False).mean())
    print(df.groupby(['type'], as_index = False).mean())

    print(df[df['quality']>5][['pH', 'quality', 'density']].groupby(['quality'], as_index=False).mean())
    print(df[df['quality']>5][['pH', 'quality', 'density','type']].groupby(['quality', 'type'], as_index=False).mean())

    print(df[['density', 'pH', 'quality']].groupby(['quality'], as_index=True).agg([np.sum, np.mean, np.std]))

    print(df.groupby('quality').filter(lambda x: len(x)>=50)) # ??????????????????

  link: https://towardsdatascience.com/an-introduction-to-pandas-in-python-b06d2dd51aba
  link_from_PPB: https://colab.research.google.com/drive/13iWNFfaJAU0BtPhIDvHHZUzGXO7YLlUC?usp=sharing
  for data manipulation
  types of data structures in pandas: DataFrame{for 2D arrays} + Series{ for 1D arrays}

  PLOTTING
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    df = pd.DataFrame(np.random.rand(10,4), columns = list('ABCD'))
    print(df)

    plt.figure(figsize =(20,20))
    sns.heatmap(df.corr(), annot = True, cmap = 'coolwarm', linewidths = 2)

    df.plot.scatter(x = 'A', y  = 'B')
    for each trial:
    df.plot()
    df.plot.bar()
    df.plot.bar(stacked = True) ??
    df.plot.barh()
    for each column:
    df.hist(bins=10) - - gives column wise frequency
    df.plot.hist(bins = 10)
    df.plot.area() ??
    df.plot.box() - column wise values mean,...
    df.plot.pie(subplots = True)

  MAKING A DATAFRAME
    2D
    df = pd.DataFrame({'marks':[25,35], 'rank':[1,2]}, index = ["StudentA", "StudentB"], name='dataframe name')
    or
    df = pd.DataFrame({[25,35], [1,2]}, index =  ["StudentA", "StudentB"], column = ['marks', 'rank'])
    #when index is not mentioned 0,1,2... are taken as default
    # similar to dictionaries
    1D
    df = pd.Series([1,2,3], index = ['a','b','c'], name = 'Series name')
    1D + 2D
    fruit = ['Apple', 'Orange', 'Grapes']
    rate = [80, 45, 40]
    health = ['A', 'B', 'C']
    shop = pd.Series(rate, fruit) # right
    shopee = pd.DataFrame(rate, fruit) # right
    # shop = pd.Series/DataFrame(rate, fruit, health) # wrong

  MERGING DATAFRAME
    pd.merge(df1, df2, on='common_column name', how='left/right/inner/outer')
    # consider sets df1 and df2
    inner = common of both
    left = common of both + left xtra
    right = common of both + right xtra
    outer = all

  OPENING A DATAFRAME
    pd.read_csv / pd.read_excel / pd.read_{file_type}

  OTHER PROPS
    df.drop(['a','b',...]) - takes all other columns than the dropped ones
    df.drop("region", axis = 1, inplace = True)
      #inplace = True ensures that data frame operation is not performed and nothing is returned
      #{axis = 1} == {axis = 'columns'} & {axis = 0} == {axis = "rows"}
    df.rename(columns = {'a':'A',...}) - renames the columns
    df['A'] = df['A'].astype("int")

  DESCRIPTIVE
    df['Portability'].value_counts - unique value counts
    df['Portability'].value_counts.index.tolist() - unique value key names
    df['Portability'].unique() - gives all the unique values, same as above
    df['Portability'].nunique() - gives total no of unique values
    df['Portability'].isnull().sum() - gives total no of null cells in 'Portability' column
    df.dtypes - gives the type of data stored in each column
    df.shape - column * row
    df.shape[0] - size of rows
    df.shape[1] - size of columns
    df.columns - column names
    df.describe - describes data, like its mean, 75% values, etc.
    df.describe(include='all')
    df.info

  APPLY AND MAP
    df['quality'] = df['quality'].apply(lambda x:x*100)
    df['quality'] = df['quality'].map(lambda x:x*100)
    df.apply(lambda x:x*100)

  INDEXING SORTING SLICING {INDEX PROPS}
    import pandas as pd
    import numpy as np
    df = pd.DataFrame(np.random.rand(5,3), index=[5,3,2,4,1], columns = list('ABC'))

    # for a specific row
    print(df)
    print(df.loc[1]) #for a specific index calling wrt no
    print(df.iloc[1]) # for a specific index calling wrt location {location starts from 0}

    #Sorting
    print(df.sort_index())
    print(df.sort_index(ascending = False))




    #Slicing
    df = df.sort_index()
    print(df.head(3))
    print(df.tail(3))
    print(df[1:4])

  MISSING VALUES
    import pandas as pd
    import numpy as np
    df = pd.DataFrame([[10,15,12], [np.NaN, 13, 10], [14, np.NaN, 13], [np.NaN, np.NaN, 14], [13,12,11]], index = [1,2,3,4,5], columns = ['A', 'B', 'C'])
    print(df)



    df = df['col name']
    df4 = df.fillna(method = 'ffill')
    print(df4)
    df5 = df.fillna(method = 'bfill')
    print(df5)
    df3 = df.fillna(0)
    print(df3)
    df6 = df.fillna(df.mean()) #or df.median / df.mode() / df.max() / df.min()
    print(df6)
    df10 = df.replace(np.nan, df.mean())

    print(df.isnull().sum())
    #df7 = df.fillna(subset = ['B']) ???????????????????????????????????????
    #print(df7) ??

    df1 = df.dropna(subset = ['col name'], axis = 0 , inplace - True) # list wise deletion
    print(df1)
    df2 = df.dropna(subset = ['col name'], axis = 1 , inplace - True) # pair wise deletion
    print(df2)

    df = df['col name']
    df4 = df.fillna(method = 'ffill')
    print(df4)
    df5 = df.fillna(method = 'bfill')
    print(df5)
    df3 = df.fillna(0)
    print(df3)
    df6 = df.fillna(df.mean()) / df.median / df.mode() / df.max() / df.min()
    print(df6)
    df10 = df.replace(np.nan, df.mean())
    print(df10)
    df8 = df.fillna(df.mode().iloc[0])
    print(df8)

    print(df.isnull().sum())
    print(df.info())
    print(df.isna())
    df9 = df.dropna(subset = ['col name'], axis = 0/1)
    #df7 = df.fillna(subset = ['Col name'], df.mean()) ??
    #print(df7) ??

  GROUPING, FILTERING AND VALUE_COUNTS- {FOR COLUMN RELATION SHIPS}
    import pandas as pd
    import numpy as np
    df = pd.read_csv(r'C:\Users\DELL\Downloads\wine.csv')
    print(df.describe(include = 'all')) # include = 'all' implies all the columns must be considered for describing
    print(df.info())
    print(df[['pH', 'type']].groupby(['type'], as_index=False).mean())
    print(df[['pH', 'type']].groupby(['type'], as_index=True).mean())
    print(df[['type', 'quality', 'density']].groupby(['type', 'quality'], as_index = False).mean())
    print(df.groupby(['type'], as_index = False).mean())

    print(df[df['quality']>5][['pH', 'quality', 'density']].groupby(['quality'], as_index=False).mean())
    print(df[df['quality']>5][['pH', 'quality', 'density','type']].groupby(['quality', 'type'], as_index=False).mean())

    print(df[['density', 'pH', 'quality']].groupby(['quality'], as_index=True).agg([np.sum, np.mean, np.std]))

    print(df.groupby('quality').filter(lambda x: len(x)>=50)) # ??????????????????

  RELATION BETWEEN COLUMNS - USED FOR PLOTTING
    Refer to SEC - GROUPING + FILTERING TOO
    #df.corr() - gives us the correlation of each column with each other columns
    #plt.figure(figsize =(20,20))
     sns.heatmap(df.corr(), annot = True, cmap = 'coolwarm', linewidths = 2)
    # On basis on heatmap correlation b/w two columns we decide to draw a graph between them

  FOR ALPHABETICAL DATA
    FOR MAKING COLUMS FOR EACH DISTINCT ALPHABETICAL DATA = 4
      a = pd.get_dummies(df['a']) - #try and see
      df = pd.concat([df, a], axis = 1) - then df dataframe adds 'a' dataframe into it
      #pd.concat([df,a]) without axis parameter may concat in row
      # pd.append() works similar to pd.concat()
    FOR YES / NO = 2
      map1 = {'male':1, 'female': 0}
      df['gender'] = df['gender'].map(map1)
    LABEL ENCODER = MAKING ARBITARY NUMBERS FOR EACH COLUMN
      from sklearn.preprocessing import LabelEncoder
      outlook_at = LabelEncoder()
      df['Summary_a'] = outlook_at.fit_transform(a)
      df['D_Sum_b'] = outlook_at.fit_transform(b)
      df['Precip_c'] = outlook_at.fit_transform(c)

Numpy:
  to work with arrays.
  to operate on numerical python {sin, cos, pi}
  np.sin
  np.cos
  np.linspace(0,10,20) - 20 equally apced no's b/w 0 and 10
  np.radnom.randn(500).cumsum()
  Numpy_codes
      # array vs np.array
      import numpy as np
      l = range(1000)
      print(type(l))
      n = np.arange(1000)
      print(type(n))
      print('??????????????')
      S = np.random.rand(1000)
      L = [S]
      N = np.array(S)
      import sys
      print("{0} \n{1}".format(type(L), type(N)))
      print(sys.getsizeof(1)*len(L))
      print(N.size * N.itemsize)
      print('??????????????')

      # Storage:
        import sys
        l_storage = sys.getsizeof(1)*len(l)
        print('list: ',l_storage,  )
        n_storage = n.size * n.itemsize
        print('numpy: ',n_storage)

      # Time
        import time
        l1 = range(1000000)
        l2 = range(1000000)
        l3 = []
        start = time.time()
        for i in range(len(l1)):
            l3.append(l1[i] + l2[i])
        end = time.time()
        print("list: ", (end - start) * 1000)
        n1 = np.arange(1000000)
        n2 = np.arange(1000000)
        start2 = time.time()
        n3 = n1 + n2
        end2 = time.time()
        print('array: ', (end2 - start2) * 1000)

      # Creating specific lists {random}
        print(np.empty(5)) #it is used to fit elements in empty np array using range  # returns previously allocated elements in similar dimentional arrays
        print(np.empty((5,3)))

        print(np.ones(5))
        print(np.ones((5,3)))

        print(np.arange(1,10,2)) #(start, stop, step)  #similar to range func

        print(np.linspace(1,10,10))

        print(np.random,randn(500).cumsum())

        #using random {# Here the code is not in python format}
          # rand = random
          np.random.seed(10)
          random(B) = 1 set with B number of elements { only + }
            random((a,b,c,d,e))  = a sets are formed {only +}
                             each of a set with b sets
                             each of b set with c sets
                             each of c set with d sets
                             each of d set has e elements in it
          rand(B) = 1 set with B number of elements { only +}
            rand(a,b,c,d,e) = a sets are formed {only +} ----- ERROR
                             each of a set with b sets
                             each of b set with c sets
                             each of c set with d sets
                             each of d set has e elements in it
          randn(B) = 1 set with B number of elements { + and - }
            randn(a,b,c,d,e) = a sets are formed ----- ERROR
                             each of a set with b sets
                             each of b set with c sets
                             each of c set with d sets
                             each of d set has e elements in it
          randint(B) = 1 element in range(B)
            randint(a,b) = 1 element between a and b
            randint(a,b,c) = c elements between a and b
            randint(A,B,(a,b,c,d,e)) = numbers between A and B form
                             a sets are formed {only +}
                             each of a set with b sets
                             each of b set with c sets
                             each of c set with d sets
                             each of d set has e elements in it
          x = [1,2,3,4,5,6,7,8,9]

          print(np.random.choice(x))

          print('Permutation: ', np.random.permutation(5))

          print('Before shuffle',x)
          np.random.shuffle(x)
          print('After shuffle',x)

      # Manipulations {nd_to_1d + slicing + concat + split}
        # 1D to nD
          n1 = np.arange(1,13,2)
          n2 = n1.reshape(2,3)
          print(n2) # reshaped (2,3) i.e 2x3 = 6 must be the number of elements in the 1D (1,13,2) array
          # nD to 1D
          print(n2.ravel())
          print(n2.flatten())
          # columns to rows and rows to columns
          print(n2.transpose())

        #Array slicing
          n = np.array([[1,2,3],[4,5,6],[7,8,9]])
          print(n)
          # for rows:
          print(n[0])
          print(n[0:2]) # first two
          # for columns
          print(n[:,0])
          print(n[:,0:2])

        # concatinating
          n1 = np.array([[1,2,3],[4,5,6],[7,8,9]])
          n2 = np.array([[1,2,3],[4,5,6],[7,8,9]])
          n = np.concatenate((n1,n2))
          print(n)
          n_v = np.vstack((n1,n2))
          print(n_v)
          n_h = np.hstack((n1,n2))
          print(n_h)

        # Splitting
          v_n = np.split(n_v,2)
          print(v_n)
          V_N = np.split(n_v,3, axis = 1)
          print(V_N)
          h_n = np.split(n_h,3)
          print(h_n)
          H_N = np.split(n_h,3, axis = 1)
          print(H_N)

      # Props
        n = np.array(np.random.random(10))
        N = np.array(np.random.rand(3,5))

        print(n.ndim)
        print(N.ndim)

        print(n.shape)
        print(N.shape)

      # Operations
        n = np.array([[1,2],[3,4]])
        N = np.array([[1,2],[3,4]])

        # print(n  +-*/  N)
        print(np.add(n,N))
        print(np.subtract(n,N))
        print(n.dot(N))

        print(n)
        print(n.max())
        print(n.min())
        print(n.max(axis = 1))
        print(n.min(axis = 1))
        print(n.max(axis = 0))
        print(n.min(axis = 0))
        print(n.argmax())
        print(n.argmin())

        # Many more
        nN = np.array(np.random.rand(3,5,5))
        print("sum:{0}, mean:{1}, sqrt:{2}, log:{3}, exp:{4}, std: {5}, log10{6}".format(np.sum(nN), np.mean(nN), np.sqrt(nN), np.log(nN), np.exp(nN), np.std(n), np.log10(n)))
        np.sum(n, axis = 0/1)

      # String Manipulation
        a = 'Pilla'
        b = 'Bunny'
        print(np.char.add(a,b))
        print(np.char.equal(a,b))
        print(np.char.upper(a))
        print(np.char.lower(b))
        print(np.char.replace(a,'l','L'))
        print(np.char.center(a,12,fillchar="*"))
        print(np.char.join([':', "/"], [a,b]))
        print(np.char.count(a,'l'))
        print(np.char.split(a, 'l'))
        #split line from string
        str3 = "abc \n 123"
        print (np.char.splitlines(str3))

      # Trig
        import matplotlib.pyplot as plt
        x = np.arange(0,2*np.pi,0.1)
        plt.plot(x, np.sin(x))
        plt.plot(x, np.cos(x))
        #plt.plot(x, np.tan(x))
        plt.show()
        plt.plot(x, np.tan(x))
        plt.show()

Matplotlib:
  for data visualization
  similar to MATLAB

  X AND Y
    plt.figure(figsize=(10,10)) --- size
    fig = plt.figure()
      ax1 = fig.add_axes([0,0,1,1])           #[0-x(leftmost_co-ord), 0-y(bottom_co-ord), 1-x(rightmost_co-ord), 1-y(top_co-ord)]
      ax2 = fif.add_axes([0.5,0.5,0.4,0.4])   #graph_of_{0.5 to 0.5+0.4 on x and y} inside graph_of_{0 to 1 on x and y}
    plt.xlim([0,1]) / plt.ylim([0,1])
    plt.ylim()
    plt.title('')
    plt.xlabel('') / plt.ylable('')
    plt.legend(loc='upper right')
    plt.show()

  PLOTS
    Here : x = range(len(y))
    plt.plot(x,y, color='') ---line
    plt.scatter(x,y, color='') --- points
    plt.bar(x,y) ---bar
    plt.barh(x,y) --- horizontal bar
    plt.pie(x, labels = leabels) --- pie
                                    E.x. :
                                    plt.figure(figsize=(7,7))
                                    x10 = [35, 25, 20, 20]
                                    labels = ['Computer', 'Electronics', 'Mechanical', 'Chemical']
                                    plt.pie(x10, labels=labels);
                                    plt.show()
    plt.boxplot(x) --- boxplot:
                      used to get visualization on distribution of values in a field or to compare the value trends in two / more fields
                      Q1 = lower quartile represent 25% of data's value
                      Q2 = median represent 50% of data's value
                      Q3 = upper quartile represent 75% of data's value
                      Maximum represent the maximum value
                      Minimum represent the min value
                      outliers represent the values beyond minimum and maximum {far from graph}
                      whiskers represent the remaining values
    plt.bar(range(len(y)), y, 'r')
    plt.bar(range(len(z)), z, 'b', bottom = y )

  plt properties:

    marker='*'/ color='red' / emap='viridis' or 'binary' or 'plt.cm.binary' /

  3D:
    ax = plt.axes(projection='3d')
    ax.plot3D(X,Y,Z,emap='')
    Images:
    plt.imshow(images[i], cmap = plt.cm.binary) --- to show Images
    plt.grid(True) --- to show grids
    plt.subplot(5,5,i+1) # 5,5=size , i+1 = index_no --- subplots size and no
    plt.xticks([]) / plt.yticks([]) --- ticks representation

Seaborn:
  link: https://towardsdatascience.com/seaborn-python-8563c3d0ad41
  on top of matplotlib - advanced version of matplotlib
  supports high level abstractions for multi plot grids

  Codes:
    import seaborn as sns
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd

    loaded = pd.read_csv('https://raw.githubusercontent.com/btkhimsar/DataSets/master/tips.csv')
    print(loaded.nunique())

    # Scatter plot
    sns.relplot(x="total_bill", y="tip",color = 'b', data=loaded);
    plt.show()
    sns.relplot(x="total_bill", y="tip", palette='viridis', hue='sex', style='time', size='size', sizes=(10,200), data=loaded)
    plt.show()

    # Lineplot
    # using loaded data
    sns.relplot(x="size", y="total_bill", hue ='day', kind='line', data=loaded);
    plt.title("loaded data")
    plt.show()
    # using random.cumsum()
    # A
    np.random.seed(42)
    sns.relplot(x=np.arange(500), y=np.random.randn(500).cumsum(), color='r', kind='line')
    plt.title("random A - cumsum")
    plt.show()
    # B - y manipulated wrt x
    np.random.seed(0)
    a = np.random.random((5,2))
    print(a)
    data = pd.DataFrame(a.cumsum(axis=0), columns=['x', 'y'])
    print(data)
    sns.relplot(x='x', y='y', data=data, kind='line')
    plt.title("random B - cumsum \n y manipulated wrt x")
    plt.show()

    # using dict = y manipulated wrt x
    diction = dict(key = np.arange(500), value=np.random.randn(500).cumsum())
    data = pd.DataFrame(diction)
    print(data)
    sns.relplot(x='key', y='value', data=data, kind='line')
    plt.title("dict")
    plt.show()

    # Getting dependancy of columns
    plt.figure(figsize=([10,10]))
    sns.heatmap(loaded.corr(), annot = True, cmap = 'coolwarm', linewidths = 2)
    plt.title('Heat Plot')
    plt.show()
    # point distribution w.r.t columns
    sns.pairplot(loaded[['pH', 'sulphates', 'alcohol', 'quality']])
    plt.title('Pair Plot')
    plt.show()

Scipy:
    on top of numpy - advanced version of numpy
    scientific operations with more features, but slow in speed than numpy

Sklearn:
  link: https://scikit-learn.org/stable/
  on top of scipy, numpy, matplotlib

northeast...


Excel:
  import numpy as np
  import pandas as pd

  # Creating a DataFrame
  data = {
      'Name': ['Alice', 'In', 'Charlie'],
      'Age': [25, 30, 28],
      'City': ['New York', 'San Francisco', 'Los Angeles']
  }
  df = pd.DataFrame(data)
  excel_file_path = r'C:\Users\DELL\Desktop\B tech 1\Excel\from_python.xlsx'
  df.to_excel(excel_file_path, index=False, sheet_name='Sheet1')

  data = {
      'Name': ['John', 'Cena', 'WWW'],
      'Age': [25, 30, 28],
      'City': ['New York', 'San Francisco', 'Los Angeles']
  }
  excel_file_path = r'C:\Users\DELL\Desktop\B tech 1\Excel\from_python.xlsx'
  with pd.ExcelWriter(excel_file_path, engine='openpyxl') as writer:
      df.to_excel(writer, index=False, sheet_name='Sheet2')
      # You can add more sheets and customize the Excel file here

    """

    return a


def print_python_pandas():
    a = r"""
    
    Pandas:

  pd.Timestamp.now() ===> current date via pandas
  pd.Categorical(df['label']).codes ===> label encoding via pandas
  from sklearn.preprocessing import LabelEncoder
  df['label'] = LabelEncoder.fit_transform(df['label'])

  Pandas_codes():
    import pandas as pd
    df1 = pd.DataFrame({'marks':[80,90,100], 'rank': [3,2,1]}, index = ['StudentA', 'StudentB', 'StudentC'])
    print(df1)
    df2 = pd.DataFrame({'grade':['C','B','A'], 'rank': [3,2,1]}, index=[1,2,3])
    print(df2)
    df = pd.merge(df1,df2,on='rank')
    print(df)
    df3 = pd.DataFrame({'CGPA':[8,9,10]})
    df_ = pd.concat([df,df3]) # df.append(df3) works the same
    print(df_)
    df_= pd.concat([df,df3], axis=1)
    print(df_)
    print(df_.corr())
    import seaborn as sns
    import matplotlib.pyplot as plt
    map = sns.heatmap(df_.corr(), annot = True, cmap = 'coolwarm', linewidths = 10) #linewidths = space b/w each box, annot is used to show names on boxes
    #plt.show()
    change = {'A':1.0,'B':2.0,'C':3.0}
    df_['grade'] = df_['grade'].map(change)
    print(df_)
    print(df_.dtypes)
    df_ = df_.rename(columns = {'CGPA':'Point'})
    print(df_)
    df4 = pd.DataFrame({'Status':['follower', 'follower', 'leader']})
    df_ = pd.concat([df_,df4], axis = 1)
    print(df_)
    df5 = pd.get_dummies(df_['Status'])
    print(df5)
    df_ = pd.concat([df_,df5], axis = 1)
    print(df_)
    print(df_.shape)
    a = [1,2,3,4]
    _df = pd.Series(['a','b','c'], index = [1,2,3], name = 'Series')
    print(_df)

    fruit = ['Apple', 'Orange', 'Grapes']
    rate = [80, 45, 40]
    health = ['A', 'B', 'C']
    shop = pd.Series(rate, fruit) # right
    # shop = pd.Series(rate, fruit, health) # wrong
    shopee = pd.DataFrame(rate, fruit)
    print(shop)
    print(shopee)
    print(".................")
    df_=pd.read_csv(r"C:\Users\DELL\Desktop\Mini_project2\water_potability.csv")
    print(df_.columns, df_.describe, df_.info)

    import pandas as pd
    import numpy as np
    df = pd.read_csv(r'C:\Users\DELL\Downloads\wine.csv')
    # changing all values of a data frame by a specific formuls
    df['quality_Q'] = df['quality'].apply(lambda x:x*100)
    # or
    df['quality_QQ'] = df['quality'].map(lambda x:x*1000)
    #or
    df['quality_QQQ'] = df['quality'] * 10000
    print(df[['quality', 'quality_Q', 'quality_QQ' ,'quality_QQQ']])
    print(df)
    print(df.quality_QQ.unique())
    df.apply(lambda x: x*100)
    print(df)

    import pandas as pd
    import numpy as np
    df = pd.DataFrame(np.random.rand(5,3), index=[5,3,2,4,1], columns = list('ABC'))
    # for a specific row
    print(df)
    print(df.loc[1]) #for a specific index calling wrt no
    print(df.iloc[1]) # for a specific index calling wrt location {location starts from 0}
    #Sorting
    print(df.sort_index())
    print(df.sort_index(ascending = False))
    #Slicing
    df = df.sort_index()
    print(df.head(3))
    print(df.tail(3))
    print(df[1:4])

    import pandas as pd
    import numpy as np
    df = pd.DataFrame([[10,15,12], [np.NaN, 13, 10], [14, np.NaN, 13], [np.NaN, np.NaN, 14], [13,12,11]], index = [1,2,3,4,5], columns = ['A', 'B', 'C'])
    print(df)
    df1 = df.dropna(subset = ['col name'], axis = 0 , inplace - True) # list wise deletion
    print(df1)
    df2 = df.dropna(subset = ['col name'], axis = 1 , inplace - True) # pair wise deletion
    print(df2)

    df = df['col name']
    df4 = df.fillna(method = 'ffill')
    print(df4)
    df5 = df.fillna(method = 'bfill')
    print(df5)
    df3 = df.fillna(0)
    print(df3)
    df6 = df.fillna(df.mean()) #or df.median / df.mode() / df.max() / df.min()
    print(df6)
    df10 = df.replace(np.nan, df.mean())

    print(df.isnull().sum())
    #df7 = df.fillna(subset = ['B']) ???????????????????????????????????????
    #print(df7) ??

    import pandas as pd
    import numpy as np
    df = pd.read_csv(r'C:\Users\DELL\Downloads\wine.csv')
    print(df.describe(include = 'all')) # include = 'all' implies all the columns must be considered for describing
    print(df.info())
    print(df[['pH', 'type']].groupby(['type'], as_index=False).mean())
    print(df[['pH', 'type']].groupby(['type'], as_index=True).mean())
    print(df[['type', 'quality', 'density']].groupby(['type', 'quality'], as_index = False).mean())
    print(df.groupby(['type'], as_index = False).mean())

    print(df[df['quality']>5][['pH', 'quality', 'density']].groupby(['quality'], as_index=False).mean())
    print(df[df['quality']>5][['pH', 'quality', 'density','type']].groupby(['quality', 'type'], as_index=False).mean())

    print(df[['density', 'pH', 'quality']].groupby(['quality'], as_index=True).agg([np.sum, np.mean, np.std]))

    print(df.groupby('quality').filter(lambda x: len(x)>=50)) # ??????????????????

  link: https://towardsdatascience.com/an-introduction-to-pandas-in-python-b06d2dd51aba
  link_from_PPB: https://colab.research.google.com/drive/13iWNFfaJAU0BtPhIDvHHZUzGXO7YLlUC?usp=sharing
  for data manipulation
  types of data structures in pandas: DataFrame{for 2D arrays} + Series{ for 1D arrays}

  PLOTTING
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    df = pd.DataFrame(np.random.rand(10,4), columns = list('ABCD'))
    print(df)

    plt.figure(figsize =(20,20))
    sns.heatmap(df.corr(), annot = True, cmap = 'coolwarm', linewidths = 2)

    df.plot.scatter(x = 'A', y  = 'B')
    for each trial:
    df.plot()
    df.plot.bar()
    df.plot.bar(stacked = True) ??
    df.plot.barh()
    for each column:
    df.hist(bins=10) - - gives column wise frequency
    df.plot.hist(bins = 10)
    df.plot.area() ??
    df.plot.box() - column wise values mean,...
    df.plot.pie(subplots = True)

  MAKING A DATAFRAME
    2D
    df = pd.DataFrame({'marks':[25,35], 'rank':[1,2]}, index = ["StudentA", "StudentB"], name='dataframe name')
    or
    df = pd.DataFrame({[25,35], [1,2]}, index =  ["StudentA", "StudentB"], column = ['marks', 'rank'])
    #when index is not mentioned 0,1,2... are taken as default
    # similar to dictionaries
    1D
    df = pd.Series([1,2,3], index = ['a','b','c'], name = 'Series name')
    1D + 2D
    fruit = ['Apple', 'Orange', 'Grapes']
    rate = [80, 45, 40]
    health = ['A', 'B', 'C']
    shop = pd.Series(rate, fruit) # right
    shopee = pd.DataFrame(rate, fruit) # right
    # shop = pd.Series/DataFrame(rate, fruit, health) # wrong

  MERGING DATAFRAME
    pd.merge(df1, df2, on='common_column name', how='left/right/inner/outer')
    # consider sets df1 and df2
    inner = common of both
    left = common of both + left xtra
    right = common of both + right xtra
    outer = all

  OPENING A DATAFRAME
    pd.read_csv / pd.read_excel / pd.read_{file_type}

  OTHER PROPS
    df.drop(['a','b',...]) - takes all other columns than the dropped ones
    df.drop("region", axis = 1, inplace = True)
      #inplace = True ensures that data frame operation is not performed and nothing is returned
      #{axis = 1} == {axis = 'columns'} & {axis = 0} == {axis = "rows"}
    df.rename(columns = {'a':'A',...}) - renames the columns
    df['A'] = df['A'].astype("int")

  DESCRIPTIVE
    df['Portability'].value_counts - unique value counts
    df['Portability'].value_counts.index.tolist() - unique value key names
    df['Portability'].unique() - gives all the unique values, same as above
    df['Portability'].nunique() - gives total no of unique values
    df['Portability'].isnull().sum() - gives total no of null cells in 'Portability' column
    df.dtypes - gives the type of data stored in each column
    df.shape - column * row
    df.shape[0] - size of rows
    df.shape[1] - size of columns
    df.columns - column names
    df.describe - describes data, like its mean, 75% values, etc.
    df.describe(include='all')
    df.info

  APPLY AND MAP
    df['quality'] = df['quality'].apply(lambda x:x*100)
    df['quality'] = df['quality'].map(lambda x:x*100)
    df.apply(lambda x:x*100)

  INDEXING SORTING SLICING {INDEX PROPS}
    import pandas as pd
    import numpy as np
    df = pd.DataFrame(np.random.rand(5,3), index=[5,3,2,4,1], columns = list('ABC'))

    # for a specific row
    print(df)
    print(df.loc[1]) #for a specific index calling wrt no
    print(df.iloc[1]) # for a specific index calling wrt location {location starts from 0}

    #Sorting
    print(df.sort_index())
    print(df.sort_index(ascending = False))




    #Slicing
    df = df.sort_index()
    print(df.head(3))
    print(df.tail(3))
    print(df[1:4])

  MISSING VALUES
    import pandas as pd
    import numpy as np
    df = pd.DataFrame([[10,15,12], [np.NaN, 13, 10], [14, np.NaN, 13], [np.NaN, np.NaN, 14], [13,12,11]], index = [1,2,3,4,5], columns = ['A', 'B', 'C'])
    print(df)



    df = df['col name']
    df4 = df.fillna(method = 'ffill')
    print(df4)
    df5 = df.fillna(method = 'bfill')
    print(df5)
    df3 = df.fillna(0)
    print(df3)
    df6 = df.fillna(df.mean()) #or df.median / df.mode() / df.max() / df.min()
    print(df6)
    df10 = df.replace(np.nan, df.mean())

    print(df.isnull().sum())
    #df7 = df.fillna(subset = ['B']) ???????????????????????????????????????
    #print(df7) ??

    df1 = df.dropna(subset = ['col name'], axis = 0 , inplace - True) # list wise deletion
    print(df1)
    df2 = df.dropna(subset = ['col name'], axis = 1 , inplace - True) # pair wise deletion
    print(df2)

    df = df['col name']
    df4 = df.fillna(method = 'ffill')
    print(df4)
    df5 = df.fillna(method = 'bfill')
    print(df5)
    df3 = df.fillna(0)
    print(df3)
    df6 = df.fillna(df.mean()) / df.median / df.mode() / df.max() / df.min()
    print(df6)
    df10 = df.replace(np.nan, df.mean())
    print(df10)
    df8 = df.fillna(df.mode().iloc[0])
    print(df8)

    print(df.isnull().sum())
    print(df.info())
    print(df.isna())
    df9 = df.dropna(subset = ['col name'], axis = 0/1)
    #df7 = df.fillna(subset = ['Col name'], df.mean()) ??
    #print(df7) ??

  GROUPING, FILTERING AND VALUE_COUNTS- {FOR COLUMN RELATION SHIPS}
    import pandas as pd
    import numpy as np
    df = pd.read_csv(r'C:\Users\DELL\Downloads\wine.csv')
    print(df.describe(include = 'all')) # include = 'all' implies all the columns must be considered for describing
    print(df.info())
    print(df[['pH', 'type']].groupby(['type'], as_index=False).mean())
    print(df[['pH', 'type']].groupby(['type'], as_index=True).mean())
    print(df[['type', 'quality', 'density']].groupby(['type', 'quality'], as_index = False).mean())
    print(df.groupby(['type'], as_index = False).mean())

    print(df[df['quality']>5][['pH', 'quality', 'density']].groupby(['quality'], as_index=False).mean())
    print(df[df['quality']>5][['pH', 'quality', 'density','type']].groupby(['quality', 'type'], as_index=False).mean())

    print(df[['density', 'pH', 'quality']].groupby(['quality'], as_index=True).agg([np.sum, np.mean, np.std]))

    print(df.groupby('quality').filter(lambda x: len(x)>=50)) # ??????????????????

  RELATION BETWEEN COLUMNS - USED FOR PLOTTING
    Refer to SEC - GROUPING + FILTERING TOO
    #df.corr() - gives us the correlation of each column with each other columns
    #plt.figure(figsize =(20,20))
     sns.heatmap(df.corr(), annot = True, cmap = 'coolwarm', linewidths = 2)
    # On basis on heatmap correlation b/w two columns we decide to draw a graph between them

  FOR ALPHABETICAL DATA
    FOR MAKING COLUMS FOR EACH DISTINCT ALPHABETICAL DATA = 4
      a = pd.get_dummies(df['a']) - #try and see
      df = pd.concat([df, a], axis = 1) - then df dataframe adds 'a' dataframe into it
      #pd.concat([df,a]) without axis parameter may concat in row
      # pd.append() works similar to pd.concat()
    FOR YES / NO = 2
      map1 = {'male':1, 'female': 0}
      df['gender'] = df['gender'].map(map1)
    LABEL ENCODER = MAKING ARBITARY NUMBERS FOR EACH COLUMN
      from sklearn.preprocessing import LabelEncoder
      outlook_at = LabelEncoder()
      df['Summary_a'] = outlook_at.fit_transform(a)
      df['D_Sum_b'] = outlook_at.fit_transform(b)
      df['Precip_c'] = outlook_at.fit_transform(c)
    
    """

    return a

def print_python_numpy():
    a = r"""
    
    Numpy:
  to work with arrays.
  to operate on numerical python {sin, cos, pi}
  np.sin
  np.cos
  np.linspace(0,10,20) - 20 equally apced no's b/w 0 and 10
  np.radnom.randn(500).cumsum()
  Numpy_codes
      # array vs np.array
      import numpy as np
      l = range(1000)
      print(type(l))
      n = np.arange(1000)
      print(type(n))
      print('??????????????')
      S = np.random.rand(1000)
      L = [S]
      N = np.array(S)
      import sys
      print("{0} \n{1}".format(type(L), type(N)))
      print(sys.getsizeof(1)*len(L))
      print(N.size * N.itemsize)
      print('??????????????')

      # Storage:
        import sys
        l_storage = sys.getsizeof(1)*len(l)
        print('list: ',l_storage,  )
        n_storage = n.size * n.itemsize
        print('numpy: ',n_storage)

      # Time
        import time
        l1 = range(1000000)
        l2 = range(1000000)
        l3 = []
        start = time.time()
        for i in range(len(l1)):
            l3.append(l1[i] + l2[i])
        end = time.time()
        print("list: ", (end - start) * 1000)
        n1 = np.arange(1000000)
        n2 = np.arange(1000000)
        start2 = time.time()
        n3 = n1 + n2
        end2 = time.time()
        print('array: ', (end2 - start2) * 1000)

      # Creating specific lists {random}
        print(np.empty(5)) #it is used to fit elements in empty np array using range  # returns previously allocated elements in similar dimentional arrays
        print(np.empty((5,3)))

        print(np.ones(5))
        print(np.ones((5,3)))

        print(np.arange(1,10,2)) #(start, stop, step)  #similar to range func

        print(np.linspace(1,10,10))

        print(np.random,randn(500).cumsum())

        #using random {# Here the code is not in python format}
          # rand = random
          np.random.seed(10)
          random(B) = 1 set with B number of elements { only + }
            random((a,b,c,d,e))  = a sets are formed {only +}
                             each of a set with b sets
                             each of b set with c sets
                             each of c set with d sets
                             each of d set has e elements in it
          rand(B) = 1 set with B number of elements { only +}
            rand(a,b,c,d,e) = a sets are formed {only +} ----- ERROR
                             each of a set with b sets
                             each of b set with c sets
                             each of c set with d sets
                             each of d set has e elements in it
          randn(B) = 1 set with B number of elements { + and - }
            randn(a,b,c,d,e) = a sets are formed ----- ERROR
                             each of a set with b sets
                             each of b set with c sets
                             each of c set with d sets
                             each of d set has e elements in it
          randint(B) = 1 element in range(B)
            randint(a,b) = 1 element between a and b
            randint(a,b,c) = c elements between a and b
            randint(A,B,(a,b,c,d,e)) = numbers between A and B form
                             a sets are formed {only +}
                             each of a set with b sets
                             each of b set with c sets
                             each of c set with d sets
                             each of d set has e elements in it
          x = [1,2,3,4,5,6,7,8,9]

          print(np.random.choice(x))

          print('Permutation: ', np.random.permutation(5))

          print('Before shuffle',x)
          np.random.shuffle(x)
          print('After shuffle',x)

      # Manipulations {nd_to_1d + slicing + concat + split}
        # 1D to nD
          n1 = np.arange(1,13,2)
          n2 = n1.reshape(2,3)
          print(n2) # reshaped (2,3) i.e 2x3 = 6 must be the number of elements in the 1D (1,13,2) array
          # nD to 1D
          print(n2.ravel())
          print(n2.flatten())
          # columns to rows and rows to columns
          print(n2.transpose())

        #Array slicing
          n = np.array([[1,2,3],[4,5,6],[7,8,9]])
          print(n)
          # for rows:
          print(n[0])
          print(n[0:2]) # first two
          # for columns
          print(n[:,0])
          print(n[:,0:2])

        # concatinating
          n1 = np.array([[1,2,3],[4,5,6],[7,8,9]])
          n2 = np.array([[1,2,3],[4,5,6],[7,8,9]])
          n = np.concatenate((n1,n2))
          print(n)
          n_v = np.vstack((n1,n2))
          print(n_v)
          n_h = np.hstack((n1,n2))
          print(n_h)

        # Splitting
          v_n = np.split(n_v,2)
          print(v_n)
          V_N = np.split(n_v,3, axis = 1)
          print(V_N)
          h_n = np.split(n_h,3)
          print(h_n)
          H_N = np.split(n_h,3, axis = 1)
          print(H_N)

      # Props
        n = np.array(np.random.random(10))
        N = np.array(np.random.rand(3,5))

        print(n.ndim)
        print(N.ndim)

        print(n.shape)
        print(N.shape)

      # Operations
        n = np.array([[1,2],[3,4]])
        N = np.array([[1,2],[3,4]])

        # print(n  +-*/  N)
        print(np.add(n,N))
        print(np.subtract(n,N))
        print(n.dot(N))

        print(n)
        print(n.max())
        print(n.min())
        print(n.max(axis = 1))
        print(n.min(axis = 1))
        print(n.max(axis = 0))
        print(n.min(axis = 0))
        print(n.argmax())
        print(n.argmin())

        # Many more
        nN = np.array(np.random.rand(3,5,5))
        print("sum:{0}, mean:{1}, sqrt:{2}, log:{3}, exp:{4}, std: {5}, log10{6}".format(np.sum(nN), np.mean(nN), np.sqrt(nN), np.log(nN), np.exp(nN), np.std(n), np.log10(n)))
        np.sum(n, axis = 0/1)

      # String Manipulation
        a = 'Pilla'
        b = 'Bunny'
        print(np.char.add(a,b))
        print(np.char.equal(a,b))
        print(np.char.upper(a))
        print(np.char.lower(b))
        print(np.char.replace(a,'l','L'))
        print(np.char.center(a,12,fillchar="*"))
        print(np.char.join([':', "/"], [a,b]))
        print(np.char.count(a,'l'))
        print(np.char.split(a, 'l'))
        #split line from string
        str3 = "abc \n 123"
        print (np.char.splitlines(str3))

      # Trig
        import matplotlib.pyplot as plt
        x = np.arange(0,2*np.pi,0.1)
        plt.plot(x, np.sin(x))
        plt.plot(x, np.cos(x))
        #plt.plot(x, np.tan(x))
        plt.show()
        plt.plot(x, np.tan(x))
        plt.show()
    
    """

    return a


def print_python_matplotlib():
    a = r"""
    
    Matplotlib:
  for data visualization
  similar to MATLAB

  X AND Y
    plt.figure(figsize=(10,10)) --- size
    fig = plt.figure()
      ax1 = fig.add_axes([0,0,1,1])           #[0-x(leftmost_co-ord), 0-y(bottom_co-ord), 1-x(rightmost_co-ord), 1-y(top_co-ord)]
      ax2 = fif.add_axes([0.5,0.5,0.4,0.4])   #graph_of_{0.5 to 0.5+0.4 on x and y} inside graph_of_{0 to 1 on x and y}
    plt.xlim([0,1]) / plt.ylim([0,1])
    plt.ylim()
    plt.title('')
    plt.xlabel('') / plt.ylable('')
    plt.legend(loc='upper right')
    plt.show()

  PLOTS
    Here : x = range(len(y))
    plt.plot(x,y, color='') ---line
    plt.scatter(x,y, color='') --- points
    plt.bar(x,y) ---bar
    plt.barh(x,y) --- horizontal bar
    plt.pie(x, labels = leabels) --- pie
                                    E.x. :
                                    plt.figure(figsize=(7,7))
                                    x10 = [35, 25, 20, 20]
                                    labels = ['Computer', 'Electronics', 'Mechanical', 'Chemical']
                                    plt.pie(x10, labels=labels);
                                    plt.show()
    plt.boxplot(x) --- boxplot:
                      used to get visualization on distribution of values in a field or to compare the value trends in two / more fields
                      Q1 = lower quartile represent 25% of data's value
                      Q2 = median represent 50% of data's value
                      Q3 = upper quartile represent 75% of data's value
                      Maximum represent the maximum value
                      Minimum represent the min value
                      outliers represent the values beyond minimum and maximum {far from graph}
                      whiskers represent the remaining values
    plt.bar(range(len(y)), y, 'r')
    plt.bar(range(len(z)), z, 'b', bottom = y )

  plt properties:

    marker='*'/ color='red' / emap='viridis' or 'binary' or 'plt.cm.binary' /

  3D:
    ax = plt.axes(projection='3d')
    ax.plot3D(X,Y,Z,emap='')
    Images:
    plt.imshow(images[i], cmap = plt.cm.binary) --- to show Images
    plt.grid(True) --- to show grids
    plt.subplot(5,5,i+1) # 5,5=size , i+1 = index_no --- subplots size and no
    plt.xticks([]) / plt.yticks([]) --- ticks representation
    
    """

    return a

def print_python_seaborn():
    a = r"""
    
    Seaborn:
  link: https://towardsdatascience.com/seaborn-python-8563c3d0ad41
  on top of matplotlib - advanced version of matplotlib
  supports high level abstractions for multi plot grids

  Codes:
    import seaborn as sns
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd

    loaded = pd.read_csv('https://raw.githubusercontent.com/btkhimsar/DataSets/master/tips.csv')
    print(loaded.nunique())

    # Scatter plot
    sns.relplot(x="total_bill", y="tip",color = 'b', data=loaded);
    plt.show()
    sns.relplot(x="total_bill", y="tip", palette='viridis', hue='sex', style='time', size='size', sizes=(10,200), data=loaded)
    plt.show()

    # Lineplot
    # using loaded data
    sns.relplot(x="size", y="total_bill", hue ='day', kind='line', data=loaded);
    plt.title("loaded data")
    plt.show()
    # using random.cumsum()
    # A
    np.random.seed(42)
    sns.relplot(x=np.arange(500), y=np.random.randn(500).cumsum(), color='r', kind='line')
    plt.title("random A - cumsum")
    plt.show()
    # B - y manipulated wrt x
    np.random.seed(0)
    a = np.random.random((5,2))
    print(a)
    data = pd.DataFrame(a.cumsum(axis=0), columns=['x', 'y'])
    print(data)
    sns.relplot(x='x', y='y', data=data, kind='line')
    plt.title("random B - cumsum \n y manipulated wrt x")
    plt.show()

    # using dict = y manipulated wrt x
    diction = dict(key = np.arange(500), value=np.random.randn(500).cumsum())
    data = pd.DataFrame(diction)
    print(data)
    sns.relplot(x='key', y='value', data=data, kind='line')
    plt.title("dict")
    plt.show()

    # Getting dependancy of columns
    plt.figure(figsize=([10,10]))
    sns.heatmap(loaded.corr(), annot = True, cmap = 'coolwarm', linewidths = 2)
    plt.title('Heat Plot')
    plt.show()
    # point distribution w.r.t columns
    sns.pairplot(loaded[['pH', 'sulphates', 'alcohol', 'quality']])
    plt.title('Pair Plot')
    plt.show()

    
    """

    return a

def print_python_new_lib():
    a = r"""
    
    Scipy:
    on top of numpy - advanced version of numpy
    scientific operations with more features, but slow in speed than numpy

Sklearn:
  link: https://scikit-learn.org/stable/
  on top of scipy, numpy, matplotlib

northeast...


Excel:
  import numpy as np
  import pandas as pd

  # Creating a DataFrame
  data = {
      'Name': ['Alice', 'In', 'Charlie'],
      'Age': [25, 30, 28],
      'City': ['New York', 'San Francisco', 'Los Angeles']
  }
  df = pd.DataFrame(data)
  excel_file_path = r'C:\Users\DELL\Desktop\B tech 1\Excel\from_python.xlsx'
  df.to_excel(excel_file_path, index=False, sheet_name='Sheet1')

  data = {
      'Name': ['John', 'Cena', 'WWW'],
      'Age': [25, 30, 28],
      'City': ['New York', 'San Francisco', 'Los Angeles']
  }
  excel_file_path = r'C:\Users\DELL\Desktop\B tech 1\Excel\from_python.xlsx'
  with pd.ExcelWriter(excel_file_path, engine='openpyxl') as writer:
      df.to_excel(writer, index=False, sheet_name='Sheet2')
      # You can add more sheets and customize the Excel file here
    
    """

    return a

def print_python_data_visualization():
    a = r"""
    
    ### Data Generation
    
import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Constants
n_orders = 1000
categories = ['Electronics', 'Clothing', 'Home', 'Books', 'Toys']
regions = ['North', 'South', 'East', 'West']

# Generate data
data = {
    'Order ID': [f'ORD{i+1}' for i in range(n_orders)],
    'Product Category': np.random.choice(categories, n_orders),
    'Product Price': np.round(np.random.uniform(5, 500, n_orders), 2),  # Prices between $5 and $500
    'Quantity Sold': np.random.randint(1, 20, n_orders),  # Quantity between 1 and 20
    'Order Date': pd.date_range(start='2023-01-01', periods=n_orders, freq='H'),
    'Customer ID': [f'CUST{i+1}' for i in range(n_orders)],
    'Region': np.random.choice(regions, n_orders)
}

# Create DataFrame
df = pd.DataFrame(data)

# Show the first few rows of the DataFrame
print(df.head())

print("-------------------------------------------------------------------------------------------------------------------------------------------")

### Descriptive
# Info - to get: shape, columns, nulls
print(df.info())
for col in df.columns:
  if df[col].dtype == 'object':
    df[col] = df[col].astype('string')
print(df.info())

print("-------------------------------------------------------------------------------------------------------------------------------------------")

## Diagnostic
# numerical value statistics
df.describe()

# categorical value statistics - I
categorical_columns = df.select_dtypes(include=['string'])
cat_dict = {}
for col in categorical_columns:
  cat_dict[col] = categorical_columns[col].unique()
for i in cat_dict.items():
  print(i, "\n")

# categorical value statistics - II

primary_cols = categorical_columns[['Customer ID', 'Order ID']]
categorical_cols = categorical_columns.drop(columns=['Customer ID', 'Order ID'])
continuous_cols = df.drop(columns=categorical_columns.columns)
print(primary_cols)
print(categorical_cols)
print(continuous_cols)

print("-------------------------------------------------------------------------------------------------------------------------------------------")

### Visuals
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display
def summary():
  return continuous_cols.describe()

# Histogram: df - single col - continous

# bins = int(round(max(df['Product Price'])/10, 2))
# print(bins)
plt.figure(figsize=(10, 6))
sns.histplot(df['Product Price'], bins=50, kde=True)

plt.xlim(0,500)
plt.xticks(np.arange(0,500,50))

plt.title('Distribution of Product Prices')
plt.xlabel('Price')
plt.ylabel('Frequency')

plt.show()

summary()

# Pie chart - groupby - single col - descrete
data = df.groupby('Product Category')['Quantity Sold'].sum().reset_index()
from IPython.display import display
display(data)
plt.pie(data['Quantity Sold'], labels=data['Product Category'], autopct='%1.3f%%') # automatically converted to percentage
plt.show()

# Pie chart - 2
# Number of regions
regions = df['Region'].unique()
n_regions = len(regions)
# Create a subplot for each region: 1=row, n_regions=column, figsize=(width, height)
fig, axes = plt.subplots(1, n_regions, figsize=(n_regions*5, 5))
for ax, region in zip(axes, regions):
    data_region = df[df['Region'] == region]['Product Category'].value_counts()
    display(data_region)
    ax.pie(data_region, labels=data_region.index, autopct='%1.1f%%')
    ax.set_title(f'Product Categories in {region} Region')
plt.tight_layout()
plt.show()

# Countplot
data = df.groupby('Product Category').count()
display(data)
sns.countplot(x='Product Category', data=df)
plt.show()

# bar chart: groupby - continuous + descrete
# resetting index is important
data = df[['Quantity Sold']].groupby([df['Product Category']]).agg(
    Total_Sold = ('Quantity Sold', 'sum')
).reset_index()
data2 = df[['Quantity Sold']].groupby([df['Product Category'], df['Region']]).agg(
    Total_Sold = ('Quantity Sold', 'sum')
).reset_index()

from IPython.display import display
display(data)
sns.barplot(x='Product Category', y='Total_Sold', data=data, palette='husl')
plt.show()
display(data2)
sns.barplot(x='Product Category', y='Total_Sold', hue='Region', data=data2)
plt.show()

# boxplot: df - continuous + descrete

sns.boxplot(x='Product Category', y='Product Price', data=df)
plt.show()

# Violin plot - continuous + descrete

sns.violinplot(x='Product Category', y='Product Price', data=df)
plt.show()

# Strip plot - continuous + decrete (while not summary statistic, but individual points)
# introduces jitters (noise) in each category to reduce overlap
sns.stripplot(x='Product Category', y='Product Price', data=df)
plt.show()

display(df.head(5))

# scatter plot: df - continuous + continuous

df['Total Sales'] = df['Quantity Sold']*df['Product Price']
fig, axes = plt.subplots(2,2, figsize=(12,10))

sns.scatterplot(x='Quantity Sold', y='Total Sales', data=df, ax=axes[0,0])

sns.scatterplot(x='Quantity Sold', y='Total Sales', data=df, size='Product Price', ax=axes[0,1])

sns.scatterplot(x='Quantity Sold', y='Total Sales', data=df, hue='Region', ax=axes[1,0])

sns.scatterplot(x='Quantity Sold', y='Total Sales', data=df, size='Product Price', hue='Region', ax=axes[1,1])

plt.legend(loc='upper right')
plt.show()

fig, axes = plt.subplots(1, 5, figsize=(20,10))
print(fig)
print(axes)

# line chart: df - continuous + continuous (timeline dates)
# Area Chart: df - continuous + continous (timeline + cummulative frequencies)

df['Order Date Date'] = df['Order Date'].dt.date    # date extraction
df['Order Date Format'] = df['Order Date'].dt.strftime('%d-%m-%Y') # format
df['Order Day'] = df['Order Date'].dt.day           # day number
df['Order Month'] = df['Order Date'].dt.month       # month number
df['Order Year'] = df['Order Date'].dt.year         # year number
df['Order Weekday'] = df['Order Date'].dt.weekday   # week number (0 = Monday, 6 = Sunday)
df['Order Quarter'] = df['Order Date'].dt.quarter   # quarter number (1-4)
df['Order Month End'] = df['Order Date'].dt.is_month_end # (boolean)
df['Order Month Start'] = df['Order Date'].dt.is_month_start # (boolean)
weekday_mapping = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
df['Order Weekday-English'] = df['Order Weekday'].map(weekday_mapping)
df['time'] = df['Order Date'].dt.time # time extraction
df['hour'] = df['Order Date'].dt.hour
df['min'] = df['Order Date'].dt.minute
df['sec'] = df['Order Date'].dt.second

sns.lineplot(x='Order Date', y='Quantity Sold', data=df.head(50))
plt.show()
plt.fill_between(x=df['Order Date'].head(50), y1=df['Quantity Sold'].head(50), color='red', alpha=0.3)
plt.show()
sns.lineplot(x='Order Date', y='Quantity Sold', data=df.head(50))
plt.fill_between(x=df['Order Date'].head(50), y1=df['Quantity Sold'].head(50), color='red', alpha=0.3)
plt.show()

df.head()

# heatmap: pivot/matrix - .corr()/ .pivot_tables()

data = df[['Quantity Sold', 'Product Price', 'Total Sales']]
data_matrix = data.corr()
sns.heatmap(data_matrix, cmap='coolwarm', annot=True)
plt.show()

# heatmap2: Making a pivot table values

data_pivot = df.pivot_table(index=['Region'], columns=['Product Category'], values='Quantity Sold', aggfunc='sum')
sns.heatmap(data_pivot, cmap='coolwarm', annot=True)
plt.show()
data_pivot

# pair plot: making numeric columns

data = df[['Quantity Sold', 'Product Price', 'Total Sales']]
sns.pairplot(data)
plt.show()

    
    """

    return a

# ----------------------------------------------------------------------------------------------------------------------

def print_sort_algs():
    a = r"""
    
    # Bubble Sort: o	https://youtube.com/shorts/L3cAPN-YNEM?si=lapKWRbV1MY8FTg1
# sorts by comparing adj elements. largest element at the bottom last position after each iteration

array = list(np.random.randint(1,13,5))
print("Before BB sort: ",array)
n = len(array)
for i in range(n):
  for j in range(n-1-i):
    if array[j]>array[j+1]:
      array[j], array[j+1] = array[j+1], array[j]
print("After BB sort: ",array)


print("-------------------------------------------------------------------------------------------------------------------------------------------")

# Selection sort: o	https://youtube.com/shorts/gga_Y8ZrJCk?si=EBenPOiSMh7pin5
# selects the 1st element and exchanges it by min element and then 2nd element and so on

array = list(np.random.randint(1,13,5))
print("Before Insertion sort: ",array)
n = len(array)
for i in range(n):
  mini = i
  for j in range(i+1, n):
    if array[mini]>array[j]:
      mini = j
  array[mini], array[i] = array[i], array[mini]
print("After Insertion sort: ",array)

print("-------------------------------------------------------------------------------------------------------------------------------------------")
# Quick sort: https://www.youtube.com/watch?v=WprjBK0p6rw
# takes a pivot element and finds it's final position:
# implement the logic in the image of the video
##################################################################
# THE LOGIC
o = orange: l-1 - the exchanging component
g = green: l - iterator
pv = array[r]

if array[g]>pv -> pass
else:
  o = o+1
  if o<g: swap
  else: pass
  
##################################################################

array = list(np.random.randint(1,13,5))
print("Before Quick sort: ",array)
def quick_Sort(l,r,array):
  if l<r: # sorting can happen if there is more than 1 element - else its already sorted
    new_pivot = find_pivot(l, r, array)
    quick_Sort(l, new_pivot-1, array)
    quick_Sort(new_pivot+1, r, array)

def find_pivot(l, r, array):
  o = l-1
  pv = array[r]
  for g in range(l, r+1):
    if array[g]<=pv:
      o = o+1
      if g>o: # when g==o no need to swap
        array[o], array[g] = array[g], array[o]
  return o
quick_Sort(0, len(array)-1, array)
print("After Quick sort: ",array)
print("-------------------------------------------------------------------------------------------------------------------------------------------")
# Merge Sort: https://www.youtube.com/watch?v=4VqmGXwpLqc
# Simple divide and merge

array = list(np.random.randint(1,13,5))
print("Before Merge sort: ",array)

def merge_sort(array):
  n = len(array)
  if n==1:
    return array

  array_left = array[:n//2]
  array_right = array[n//2:]

  sorted_left = merge_sort(array_left)
  sorted_right = merge_sort(array_right)

  return merge(sorted_left, sorted_right)


def merge(array_left, array_right):
  merged_array = []
  while (array_left and array_right):
    if array_left[0] < array_right[0]:
      merged_array.append(array_left.pop(0))
    else:
      merged_array.append(array_right.pop(0))

  while(array_left):
    merged_array.append(array_left.pop(0))
  # or simply:
  merged_array.extend(array_right)

  return merged_array

sorted_array = merge_sort(array)
print("After Merge sort: ",sorted_array)
print("-------------------------------------------------------------------------------------------------------------------------------------------")
# Insertion sort: https://www.youtube.com/watch?v=8mJ-OhcfpYg
# Using teh temp logic in video:

array = list(np.random.randint(1,13,5))
print("Before Insertion sort: ",array)

for i in range(1, len(array)):
  temp = array[i]
  j = i-1
  while j>=0 and array[j]>temp:
      array[j+1] = array[j]
      j -= 1
  array[j+1] = temp

print("After Insertion sort: ",array)
print("-------------------------------------------------------------------------------------------------------------------------------------------")

Time & Space Complexities:

| Sorting Algorithm  | Best Case                 | Average Case     | Worst Case                     | Space Complexity  |
|--------------------|---------------------------|------------------|--------------------------------|-------------------|
| Merge Sort         | O(n log n)                | O(n log n)       | O(n log n)                     | O(n)              |
| Quick Sort         | O(n log n) (good pivot)   | O(n log n)       | O(n²) (bad pivot choice)       | O(log n)          |
| Selection Sort     | O(n²)                     | O(n²)            | O(n²)                          | O(1)              |
| Bubble Sort        | O(n) (already sorted)     | O(n²)            | O(n²)                          | O(1)              |
| Insertion Sort     | O(n) (already sorted)     | O(n²)            | O(n²)                          | O(1)              |
print("-------------------------------------------------------------------------------------------------------------------------------------------")
    """

    return a

