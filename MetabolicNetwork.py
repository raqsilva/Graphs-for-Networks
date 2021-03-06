# -*- coding: utf-8 -*-

from MyGraph import MyGraph
from bioservices import KEGG

#Metabolic Pathways

#networktype:
#reaction-compound network R-C
#compound-compound network C-C
#reaction-reaction network R-R

class MetabolicNetwork(MyGraph):
    def __init__(self, modules, organism="hsa"):    
        MyGraph.__init__(self,{})
        self.gr=MyGraph()
        self.modules=modules
        self.s = KEGG()
        self.s.organism = organism # Homo sapiens as default
    

    def __kegg_dic(self):
        if type(self.modules)!=list:
            self.modules=self.s.moduleIds
        dic_reac={}
        for mod in self.modules:
            try:
                dic=self.s.parse(self.s.get(mod))
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
        gr=self.gr
        for reac in dic_reac:
            comp=dic_reac[reac]
            c=0
            if comp[c+1]=="+": 
                try:
                    comp[c+5]=="+"
                    s2="+".join([str(comp[c+4]), str(comp[c+6])])
                    s3="+".join([str(comp[c]), str(comp[c+2])])
                    gr.addEdge(s3,s2)
                except IndexError:
                    s="+".join([str(comp[c]), str(comp[c+2])])
                    gr.addEdge(s,comp[c+4])     
            elif comp[c+1]=="->":
                try:
                    comp[c+3]=="+"
                    s="+".join([str(comp[c+2]), str(comp[c+4])])
                    gr.addEdge(comp[c],s)
                except IndexError:
                    gr.addEdge(comp[c],comp[c+2])              
        return gr.printGraph()
        
        
    def r_r_graph(self):### reac-reac
        dic_reac=self.__kegg_dic()
        gr=self.gr
        for k, v in dic_reac.items():
            for r, m in dic_reac.items():
                if v[len(v)-2] == "->":
                    if v[len(v)-1]==m[0]:
                        gr.addEdge(k, r)
                else:
                    s="+".join([str(v[len(v)-3]), str(v[len(v)-1])])
                    try:
                        s2="+".join([str(m[0]), str(m[2])])
                        if s == s2:
                            gr.addEdge(k, r)
                    except IndexError:
                        pass
        return gr.printGraph()      
        

    def r_c_graph(self):### reac-comp
        dic_reac=self.__kegg_dic()
        gr=self.gr
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
                    s="+".join([str(v[len(v)-3]), str(v[len(v)-1])])
                    try:
                        s2="+".join([str(m[0]), str(m[2])])
                        if s == s2:
                            sv="".join(v)
                            sm="".join(m)
                            gr.addEdge(k, sv)
                            gr.addEdge(sv, r)
                            gr.addEdge(r, sm)
                    except IndexError:
                        pass
        return gr.printGraph()           
        

    def modules_name(self):
        if type(self.modules)!=list:
            self.modules=self.s.moduleIds
        for i in self.modules:
            dic=self.s.parse(self.s.get(i))
            name=dic["NAME"][0]#['Glycolysis (Embden-Meyerhof pathway), glucose => pyruvate']
            s="-".join([i,name])
            print("\n".join([s]))


    def compounds_name(self):        
        if type(self.modules)!=list:
            self.modules=self.s.moduleIds
        for i in self.modules:
            print(i)
            dic=self.s.parse(self.s.get(i))
            comps=dic["COMPOUND"]#dictionary with the names of the compounds {'C00074': 'Phosphoenolpyruvate',.....
            for key in comps.keys():
                s="-".join([key,comps[key]])
                print("\n".join([s]))        
        
    
    def pathway_name(self):
        if type(self.modules)!=list:
            self.modules=self.s.moduleIds
        for i in self.modules:
            dic=self.s.parse(self.s.get(i))
            pathway=dic["PATHWAY"]#{'map00010': 'Glycolysis / Gluconeogenesis',......
            for key in pathway.keys():
                s="-".join([key, pathway[key]])
                print(s)
        
    
    def nodes_degree(self):
        gr=self.gr
        return gr.allDegrees()
        
    
    def clustering(self):
        gr=self.gr
        return gr.allClusteringCoefs()
        
        
    def connections(self, n1, n2):
        gr=self.gr
        return gr.distance(n1, n2)

        

if __name__ == "__main__":
    ans=True
    modules=[]
    while ans:
        print("""
        1.Add Module ID (ex:M00627)
        2.Add All Modules IDs (Homo sapiens)
        3.All picked
        
        """)
        ans=input("Choose an option? ")
        if ans=="1":
            md=str(input("Which Module ID? "))
            modules.append(md)
        elif ans=="2":
            modules=str("all")
            ans=False
        elif ans=="3":
            ans=False
        else:
            print("\nInvalid")     
    
    mt=MetabolicNetwork(modules)
    
    ans=True
    while ans:
        print("""
        1.Compound-Compound Network
        2.Reaction-Compound Network
        3.Reaction-Reaction Network
        4.Exit

        """)
        ans=input("Choose an option? ")
        if ans=="1":
            print(mt.c_c_graph())
        elif ans=="2":
            print(mt.r_c_graph())
        elif ans=="3":
            print(mt.r_r_graph())
        elif ans=="4":
            ans=False
        else:
            print("\nInvalid")

    
    ans=True
    while ans:
        print("""
        1.Modules name
        2.Compounds name
        3.Nodes Degree
        4.Clustering Coeficients
        5.Connections between two specific nodes
        6.Pathway Names
        10.Exit
        
        """)
        ans=input("Choose an option? ")
        if ans=="1":
            mt.modules_name()
        elif ans=="2":
            mt.compounds_name()
        elif ans=="3":
            print(mt.nodes_degree())
        elif ans=="4":
            print(mt.clustering())
        elif ans=="5":
            n1=str(input("First node: "))
            n2=str(input("Second node: "))
            print(mt.connections(n1, n2))
        elif ans=="6":
            mt.pathway_name()
        elif ans=="10":
            ans=False
        else:
            print("\nInvalid")  














    
        