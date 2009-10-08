from yappy.parser import *

class ParseReg(Yappy):
     def __init__(self, no_table=0, table='tablereg'):
        grammar ="""
        program -> statement {{ self.OrSemRule }} ;
        statement -> expression {{ self.OrSemRule }} ;
        expression -> NUMBER {{ self.OrSemRule }} ;
        statement -> name_reference EQUALS expression {{ self.OrSemRule }} ;
        expression -> expression PLUS expression {{ self.OrSemRule }} ;
        name_reference -> NAME {{ self.OrSemRule }} ;
        """
        tokenize = [
        ("\s+",""),
        ("@epsilon", lambda x: ("id", x)),
        ("@empty_set", lambda x: ("id", x)),
        ("[A-Za-z0-9]", lambda x: ("id", x)),
        ("[+]", lambda x: ("+", x), ("+", 100, 'left')),
        ("[*]", lambda x: (x, x), ("*", 300, 'left')),
        ("\(|\)", lambda x: (x, x)) ]


        Yappy.__init__(self, tokenize, grammar, table, no_table, tabletype=LR1table)

     # semantic rules build a parse tree...
     def OrSemRule(self,list,context):
         return "(%s+%s)" %(list[0],list[2])

     def ConcatSemRule(self,list,context):
         return "(%s%s)" %(list[0],list[1])

     def ParSemRule(self,list,context):
         return "(%s)" %list[1]

     def BaseSemRule(self,list,context):
         return list[0]

     def StarSemRule(self,list,context):
         return "(%s*)" %list[0]

d = ParseReg()

print d
