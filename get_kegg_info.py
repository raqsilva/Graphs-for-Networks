# -*- coding: utf-8 -*-

from bioservices import KEGG
s = KEGG()
s.organism = "hsa"

#x=s.pathwayIds
#res = s.get(x[0])

modules=s.moduleIds
dic_reac={}
for ids in modules:
    mod=s.get(ids)
    dic=s.parse(mod)
    reactions=dic['REACTION']
    for reac in reactions:
        teste=reactions[reac]
        string=teste.split(" ")
        dic_reac[reac]=string

#for reac in reactions:
#    print(reactions[reac])
