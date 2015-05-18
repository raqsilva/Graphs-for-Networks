# -*- coding: utf-8 -*-

from bioservices import KEGG
s = KEGG()
s.organism = "hsa"

x=s.pathwayIds
res = s.get(x[0])

modules=s.moduleIds

mod=s.get(modules[0])
dic=s.parse(mod)
reactions=dic['REACTION']
for reac in reactions:
    print(reactions[reac])