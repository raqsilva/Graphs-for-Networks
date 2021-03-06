# -*- coding: utf-8 -*-
from bioservices import KEGG
from MyGraph import MyGraph
from MetabolicNetwork import MetabolicNetwork

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
    s.organism = "hsa" #Homo sapiens (human)
    path=s.pathwayIds
    p=s.get(path[2])
#    modules=s.moduleIds #pathway modules
#    dic=s.parse(s.get(modules[0]))
#    compounds=dic["COMPOUND"]#dictionary with the names of the compounds {'C00074': 'Phosphoenolpyruvate',.....
#    pathway=dic["PATHWAY"] # {'map00010': 'Glycolysis / Gluconeogenesis',......
#    module_name=dic["NAME"] #['Glycolysis (Embden-Meyerhof pathway), glucose => pyruvate']
    return p #compounds, pathway, dic, module_name


def teste2():
    s = KEGG()
    s.organism = "hsa"
    modules=s.moduleIds
    print(modules[3])
    dic=s.parse(s.get(modules[3]))
    reactions=dic["REACTION"]
    dic_reac={}
    for reac in reactions:
        teste=reactions[reac]
        string=teste.split(" ")
        dic_reac[reac]=string
    return dic_reac #it gives a dictionary with reactionsID as keys and a list of compounds 
                    # as the reactions occurs,'R01015': ['C00111', '->', 'C00118']
                    # 'R01070': ['C05378', '->', 'C00111', '+', 'C00118'] 
 
#resultado teste2 
#{'R01528,R10221': ['C00345', '->', 'C00199'], 'R02739': ['C00668', '->', 'C01172'], 'R01056': ['C00199', '->', 'C00117'], 'R02736,R10520': ['C01172', '->', 'C01236'], 'R01641': ['C00117', '+', 'C00231', '->', 'C05382', '+', 'C00118'], 'R01830': ['C00279', '+', 'C00231', '->', 'C05345', '+', 'C00118'], 'R01827': ['C05382', '+', 'C00118', '->', 'C00279', '+', 'C05345'], 'R02740': ['C05345', '->', 'C00668'], 'R02035': ['C01236', '->', 'C00345'], 'R01529': ['C00199', '->', 'C00231']}

 
def teste3():
    dic_reac=teste2()
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

### RESULTADO do teste 3 ####

#C00197->['C00631']
#C00668->['C05345']
#C00111->['C00118']
#C00236->['C00197']
#C00074->['C00022']
#C00118->['C00197', 'C00236']
#C00267->['C00668']
#C00111+C00118->[]
#C00022->[]
#C05378->['C00111+C00118']
#C00631->['C00074']
#C05345->['C05378']

#print(teste2())
#teste3()
#print(teste())


def teste4():
    s = KEGG()
    s.organism = "hsa" #Homo sapiens (human)
    modules=s.moduleIds #pathway modules
    dic=s.parse(s.get(modules[0]))
    compounds=dic["COMPOUND"]#dictionary with the names of the compounds {'C00074': 'Phosphoenolpyruvate',.....
    pathway=dic["PATHWAY"] # {'map00010': 'Glycolysis / Gluconeogenesis',......
    module_name=dic["NAME"] #['Glycolysis (Embden-Meyerhof pathway), glucose => pyruvate']
    return pathway


def teste5():
    s = KEGG()
    s.organism = "hsa" #Homo sapiens (human)
    modules=s.moduleIds #pathway modules
    dic=s.parse(s.get("M00627"))
    module_name=dic["NAME"][0]
    reactions=dic["REACTION"]
    if "Pentose phosphate cycle" in module_name:
        print(module_name)
    else:
        print("haha")


def teste6():
    s = KEGG()
    s.organism = "hsa"
    modules=["M00001", "M00002", "M00013", "M00034"]
    dic_reac={}
    for mod in modules:
        dic=s.parse(s.get(mod))
        reactions=dic["REACTION"]
        for reac in reactions:
            teste=reactions[reac]
            string=teste.split(" ")
            dic_reac[reac]=string
    return dic_reac 


#print(teste6())

##### search by module name or pathway modules IDs 

### as funcoes foram optimizadas usando join em vez de "+"

def teste7():### reac-reac
    dic_reac=teste6()
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

#print(teste6())  
#teste7()


def teste8():### reac-comp
    dic_reac=teste6()
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
  

#print(teste6())  
#teste8()

print(teste4())


