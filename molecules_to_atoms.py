from collections import Counter
import re

def parse_molecule (formula):

    brackets = True
    chemical_dictionary = {}
    formula_list = [formula]
    while brackets : 
        for f in formula_list :
            if istherebracket(f) :
                outer_parts, inside_formula, x = blow_outer_bracket(f)
                index = formula_list.index(f)
                formula_list.remove(f)
                formula_list.append(outer_parts)
                for i in range (x) :
                    formula_list.append(inside_formula)
                break
        if istherebracket(f) == False :
            brackets = False
        #merging dictionaries elegantly
    for f in formula_list :
        A = Counter(chemical_dictionary)
        B = Counter(rip(f))
        chemical_dictionary = dict(A + B)
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
    for i in range (0,len(chemlist)) :
        chemdict[chemlist[i]] = multi(formula, formula.find(chemlist[i])+len(chemlist[i])-1)
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
        return int(re.search('(\d+)', f[x:x+3]).group(0)) #int(f[x+1])
    except :
        return 1