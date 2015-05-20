# -*- coding: utf-8 -*-

from bioservices import KEGG
s = KEGG()
s.organism = "hsa"

#x=s.pathwayIds
#res = s.get(x[0])

modules=s.moduleIds
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
        
print(s.parse(s.get(modules[0])))