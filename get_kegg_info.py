# -*- coding: utf-8 -*-

from bioservices import KEGG

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
    print(s.parse(s.get(modules[0])))


teste()