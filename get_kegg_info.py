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
    for reac in dic_reac:
        comp=dic_reac[reac]
        for c in comp:
            if c=="+"




#{'R01512': 'C00236 -> C00197', 'R00658': 'C00631 -> C00074', 
# 'R07159': 'C00118 -> C00197', 'R01786,R02189,R09085': 'C00267 -> C00668', 
#'R01518': 'C00197 -> C00631', 'R01070': 'C05378 -> C00111 + C00118', 
#'R01015': 'C00111 -> C00118', 'R04779,R09084': 'C05345 -> C05378', 
#'R00200': 'C00074 -> C00022', 'R02740': 'C00668 -> C05345', 'R01061,R01063': 'C00118 -> C00236'},


print(teste2())





