
import re


class Parser:
    def __init__(self, input):
        self.input = input
        self.entries = {}
        self.pos = 0
        self.unique_key = True
        self.currentEntry = ""
        self.strings = {
            'JAN': "January",
            'FEB': "February",
            'MAR': "March",
            'APR': "April",
            'MAY': "May",
            'JUN': "June",
            'JUL': "July",
            'AUG': "August",
            'SEP': "September",
            'OCT': "October",
            'NOV': "November",
            'DEC': "December"}
        self.bibtex()

    def getEntries(self):
        return self.entries

    def isWhitespace(self,s):
        return s == ' ' or s == '\r' or s == '\t' or s == '\n'


    def skipWhitespace(self):
        while self.pos < len(self.input) and self.isWhitespace(self.input[self.pos]):
            self.pos += 1

    def match(self,s):
        self.skipWhitespace()
        if self.input[self.pos: self.pos+len(s)] == s:
            self.pos += len(s)
        self.skipWhitespace()

    def tryMatch(self,s):
        self.skipWhitespace()
        if self.input[self.pos:self.pos+len(s)] == s:
            self.skipWhitespace()
            return True
        self.skipWhitespace()
        return False

    def value_braces(self):
        braces = ["{"]
        self.match("{")
        start = self.pos
        while True:
            if self.input[self.pos] == "}" and self.input[self.pos-1] != '\\':
                if len(braces) > 1:
                    braces.pop()
                elif len(braces) < 1:
                    raise Exception("File format error: Extra '}'")
                else:
                    end = self.pos
                    self.pos+=1
                    return self.input[start:end]
            elif self.input[self.pos] == '{':
                braces.append('{')
            elif self.pos >= len(self.input):
                raise Exception("File Format error: Extra '{'")
            self.pos += 1


    def value_quotes(self):
        self.pos += 1
        start = self.pos
        while True:
            if self.input[self.pos] == '"' and self.input[self.pos-1] != '\\':
                end = self.pos
                self.pos += 1
                return self.input[start:end]
            elif self.pos >= len(self.input) -1:
                raise Exception("File format error: Extra quote")
            self.pos += 1

    

    def single_value(self):
        start = self.pos
        if self.tryMatch('{'):
            return self.value_braces()
        elif self.tryMatch('"'):
            return self.value_quotes()
        else:
            k = self.key()
            if k in self.strings:
                return self.strings[k]
            elif re.match("^[0-9]+$", k) is not None:
                return k
            else:
                raise Exception("Value expected:"+self.input[start:])

    def value(self):
        values = self.single_value()
        while self.tryMatch('#'):
            self.match('#')
            values+=self.single_value()
        return values
        
    def key(self):
        self.skipWhitespace()
        start = self.pos
        while True:
            if self.pos == len(self.input):
                raise Exception("Runaway key")
            if re.match("[a-zA-z0-9_:\\./-]", self.input[self.pos]) is not None:
                self.pos += 1
            else:
                if self.unique_key:
                    return self.input[start:self.pos]
                else:
                    return self.input[start: self.pos].upper()

    def key_value(self):
        k = self.key()
        if self.tryMatch('='):
            self.match('=')
            v = self.value()
            return [k,v]
        else:
            raise Exception("... = value expected, equals sign missing:"+self.input[self.pos])

    def key_value_list(self):
        kv = self.key_value()
        self.entries[self.currentEntry][kv[0]] = kv[1]
        while self.tryMatch(","):
            self.match(",")
            if self.tryMatch("}"):
                break
            kv = self.key_value()
            self.entries[self.currentEntry][kv[0]] = kv[1]

    def entry_body(self):
        self.unique_key = True
        self.currentEntry = self.key()
        self.unique_key = False
        self.entries[self.currentEntry] = {}
        self.match(",")
        self.key_value_list()

    def directive(self):
        self.match('@')
        return '@'+self.key()

    def string(self):
        kv = self.key_equals_value()
        self.strings[kv[0].upper()] = kv[1]

    def preamble(self):
        self.value()

    def comment(self):
        self.entry_body()

    def entry(self):
        self.entry_body()

    def bibtex(self):
        while self.tryMatch('@'):
            d = self.directive().upper()
            self.match("{")
            if d == "@STRING":
                self.string()
            elif d == "@PREAMBLE":
                self.preamble()
            elif d == "@COMMENT":
                self.comment()
            else:
                self.entry()
            self.match("}")

    
        
        
                        
                            
                            
        
        
    
                            
        

                
        
        

        
    
        
