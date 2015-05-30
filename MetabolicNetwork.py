# -*- coding: utf-8 -*-

from MyGraph import MyGraph
#networktype:
#reaction-compound networks R-C
#compound-compound networks C-C
#reaction-reaction networks R-R

class MetabolicNetwork(MyGraph):
    def __init__(self, networktype):    
        MyGraph.__init__(self,graph={})
        self.net_type=networktype
