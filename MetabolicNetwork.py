# -*- coding: utf-8 -*-

from MyGraph import MyGraph
from bioservices import KEGG

#networktype:
#reaction-compound networks R-C
#compound-compound networks C-C
#reaction-reaction networks R-R

class MetabolicNetwork(MyGraph):
    def __init__(self, networktype, modules):    
        MyGraph.__init__(self,graph={})
        self.net_type=networktype
        self.modules=modules
    

    def __kegg_dic(self):
        s = KEGG()
        s.organism = "hsa" # Homo Sapiens
        if type(self.modules)!=list:
            self.modules=s.moduleIds
        dic_reac={}
        for mod in self.modules:
            try:
                dic=s.parse(s.get(mod))
                reactions=dic['REACTION']
                for reac in reactions:
                    teste=reactions[reac]
                    string=teste.split(" ")
                    dic_reac[reac]=string
            except KeyError:
                pass        
        return dic_reac #it gives a dictionary with reactionsID as keys and a list of compoundsID 
                        # 'R01015': ['C00111', '->', 'C00118']
                        # 'R01070': ['C05378', '->', 'C00111', '+', 'C00118']         
    
    def c_c_graph(self):### comp-comp
        dic_reac=self.__kegg_dic()
        gr=MyGraph()
        for reac in dic_reac:
            comp=dic_reac[reac]
            c=0
            if comp[c+1]=="+": 
                try:
                    comp[c+5]=="+"
                    s2=str(comp[c+4])+"+"+str(comp[c+6])
                    s3=str(comp[c])+"+"+str(comp[c+2])
                    gr.addEdge(s3,s2)
                except IndexError:
                    s=str(comp[c])+"+"+str(comp[c+2])
                    gr.addEdge(s,comp[c+4])     
            elif comp[c+1]=="->":
                try:
                    comp[c+3]=="+"
                    s=str(comp[c+2])+"+"+str(comp[c+4])
                    gr.addEdge(comp[c],s)
                except IndexError:
                    gr.addEdge(comp[c],comp[c+2])              
        return gr.printGraph()
        
        
    def r_r_graph(self):### reac-reac
        dic_reac=self.__kegg_dic()
        gr=MyGraph()
        for k, v in dic_reac.items():
            for r, m in dic_reac.items():
                if v[len(v)-2] == "->":
                    if v[len(v)-1]==m[0]:
                        gr.addEdge(k, r)
                else:
                    s=str(v[len(v)-3])+"+"+str(v[len(v)-1])
                    try:
                        s2=str(m[0])+"+"+str(m[2])
                        if s == s2:
                            gr.addEdge(k, r)
                    except IndexError:
                        pass
        return gr.printGraph()      
        

    def r_c_graph(self):### reac-comp
        dic_reac=self.__kegg_dic()
        gr=MyGraph()
        for k, v in dic_reac.items():
            for r, m in dic_reac.items():
                if v[len(v)-2] == "->":
                    if v[len(v)-1]==m[0]:
                        sv="".join(v)
                        sm="".join(m)
                        gr.addEdge(k, sv)
                        gr.addEdge(sv, r)
                        gr.addEdge(r, sm)
                else:
                    s=str(v[len(v)-3])+"+"+str(v[len(v)-1])
                    try:
                        s2=str(m[0])+"+"+str(m[2])
                        if s == s2:
                            sv="".join(v)
                            sm="".join(m)
                            gr.addEdge(k, sv)
                            gr.addEdge(sv, r)
                            gr.addEdge(r, sm)
                    except IndexError:
                        pass
        return gr.printGraph()           
        



if __name__ == "__main__":
    #mod=input("Which module(s) pathway you want to use to create a network?")
    ans=True
    modules=[]
    while ans:
        print("""
        1.Add module ID (ex:M00627)
        2.Add All Modules
        3.All picked
        
        """)
        ans=input("Choose an option? ")
        if ans=="1":
            md=str(input("Which module? "))
            modules.append(md)
        elif ans=="2":
            modules=str("all")
        elif ans=="3":
            ans=False
        else:
            print("\nInvalid") 





















    
        