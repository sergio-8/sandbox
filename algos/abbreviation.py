
def valid_word_abbreviation(word, abbr):

    # Replace the following return statement with your code
    
  
    w_ind = 0
    a_ind = 0
    ins = ""
    
    while w_ind < len (word) and a_ind < len(abbr):
        
        if word[w_ind] == abbr[a_ind]:
            w_ind= w_ind+1
            a_ind = a_ind +1
        
        else:                           # the strings diverge 
            if abbr[a_ind].isdigit():   # the abbr item is a digit 
                if abbr[a_ind] == '0':  # int start with zero case
                    return False
                
                ins = ""
                while a_ind < len(abbr) and abbr[a_ind].isdigit():
                    ins = ins + abbr[a_ind]
                    a_ind = a_ind + 1
                    
                w_ind = w_ind + int(ins)
            else:
                return False
            
    return w_ind == len(word) and a_ind == len(abbr)



print(valid_word_abbreviation("word", "456"))
print(valid_word_abbreviation("word", "w2d"))
print(valid_word_abbreviation("internationalization", "i18n"))
