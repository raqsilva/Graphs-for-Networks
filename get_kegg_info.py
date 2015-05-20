# -*- coding: utf-8 -*-
from bioservices import KEGG
from MyGraph import MyGraph

#x=s.pathwayIds
#res = s.get(x[0])

#dic_reac={}
# pick one organism or just the module (cycle) you want to create the network from
# each module corresponds a cycle, a pathway
#for ids in modules:
#    mod=s.get(ids)
#    dic=s.parse(mod)
#    try:
#        reactions=dic['REACTION']
#        for reac in reactions:
#            teste=reactions[reac]
#            string=teste.split(" ")
#            dic_reac[reac]=string
#    except KeyError:
#        pass
          
def teste():
    s = KEGG()
    s.organism = "hsa"
    modules=s.moduleIds
    dic=s.parse(s.get(modules[0]))
    return dic


def teste2():
    s = KEGG()
    s.organism = "hsa"
    modules=s.moduleIds
    dic=s.parse(s.get(modules[0]))
    reactions=dic['REACTION']
    dic_reac={}
    for reac in reactions:
        teste=reactions[reac]
        string=teste.split(" ")
        dic_reac[reac]=string
    return dic_reac #it gives a dictionary with reactionsID as keys and a list of compounds 
                    # as the reactions occurs,'R01015': ['C00111', '->', 'C00118']
                    # 'R01070': ['C05378', '->', 'C00111', '+', 'C00118'] 
 

dic_reac=teste2()

def teste3():
    gr=MyGraph()
    for reac in dic_reac:
        comp=dic_reac[reac]
        for c in comp:
            if c not in gr.getNodes():
            else:
                gr.addEdge()



print(teste2())



















