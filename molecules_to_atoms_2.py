from collections import Counter
import re

def parse_molecule (formula):

    print ("massaging formula", formula)
    brackets = True
    chemical_dictionary = {}
    formula_list = [formula] # creating a list for formulas to split by brackets
    #print("creating a formula list:", formula_list)
    ###while there is bracket available
    while brackets : 
        for f in formula_list :
            if istherebracket(f) :
                #print ("formula", f, " has bracket, splitting up")
                #here we should remove the original formula from the list,
                #and insert as many parts as we tore this apart
                outer_parts, inside_formula, x = blow_outer_bracket(f)
                #print("outer_parts: ", outer_parts)
                #print("inner formula: ",inside_formula)
                #print("original f: ", f)
                #print("multiplier: ", x)
                index = formula_list.index(f)
                #print("index of f in list: ", index)
                #f.replace(inside_formula, "")
                #print("new, replaced f: " + f)
                formula_list.remove(f)
                formula_list.append(outer_parts)
                for i in range (x) :
                    formula_list.append(inside_formula)
                #print("new splitted formula list: ", formula_list)
                break
        if istherebracket(f) == False :
            brackets = False
        #merging dictionaries elegantly
    for f in formula_list :
        A = Counter(chemical_dictionary)
        B = Counter(rip(f))
        chemical_dictionary = dict(A + B)
    #print(chemical_dictionary)
    return chemical_dictionary
    #and converting back from Counter type to dict

def istherebracket(formula) :
    squary_begin_pos = formula.find("[")
    curly_begin_pos = formula.find("(")
    
    if(formula.find("[") == -1 and formula.find("(") == -1) :
        return False
    else :
        return True     


def rip(formula) :
    chemdict = {}
    chemlist = re.findall('([A-Z][a-z]?)', formula)
    #print(chemlist)
    for i in range (0,len(chemlist)) :
        #we do not deal here with recurrent atoms, hope there are no such guys
        chemdict[chemlist[i]] = multi(formula, formula.find(chemlist[i])+len(chemlist[i])-1)
    #print(chemdict)
    return chemdict

def blow_outer_bracket (formula) :

    bracketz =["{","[","(","}","]",")"]
    
    for i in range (0, 3):
            o = formula.find(bracketz[i])
            if o >= 0 :
                return split(formula, bracketz[i+3],o)

#split up the shit based on the bracket type and open position
def split(f, bracket, open_pos) :
    close_pos = f.find(bracket)
    multiplier = multi(f, close_pos)
    
    if multiplier > 1 :
        outer_parts = f.replace(f[open_pos:close_pos+2], "")
    else :    
        outer_parts = f.replace(f[open_pos:close_pos+1], "")
    return outer_parts, f[open_pos+1:close_pos], multiplier
        
#finding multiplier
def multi(f, x) :
    try :
        if f[x+1].isupper() : 
            return 1
        #print(f, f[x:x+2], x, re.search('(\d+)', f[x:len(f)]).group(0))
        return int(re.search('(\d+)', f[x:x+3]).group(0)) #int(f[x+1])
    except :
        return 1