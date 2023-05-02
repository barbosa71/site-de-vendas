# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 12:42:14 2022

@author: Alcebíades
"""
import requests
import xml.etree.ElementTree as ETree
import pandas as pd

def descreve_elemento(e, nivel=0):
    espaco = ""
    for i in range(nivel*3): espaco = espaco + " "

    #Leio a tag
    print(espaco, "Tag: ", e.tag, end=" ")
    
    #Leio os atributos
    if(len(e.attrib) != 0):
        print("- Atributos:", end=" ")
        for i,valor in enumerate(e.attrib):
            print(valor, " = ", e.attrib[valor], "; ", end=" ")
    
    #Leio o espaco interno
    if (not e.text is None):
        print()
        print(espaco,"   ", e.text)
    
    #Leio os subelementos (onde tudo se repete, por isso a função é recursiva)
    if(len(e) !=0 ):
        for se in e:
            descreve_elemento(se, nivel = nivel+1)
            
    #fim da tag
    print(espaco, "Fim tag: ", e.tag)
    print()


def grava_elemento(e, nome_arquivo = None, arquivo = None, nivel=0):
    
    if(nivel==0):
        arquivo = open(nome_arquivo,'w')
    
    espaco = ""
    for i in range(nivel*3): espaco = espaco + " "

    #Leio a tag
    arquivo.write(espaco + "Tag: " + e.tag)
    
    #Leio os atributos
    if(len(e.attrib) != 0):
        arquivo.write("- Atributos:")
        for i,valor in enumerate(e.attrib):
            arquivo.write(valor + " = " + e.attrib[valor] + "; ")
    
    #Leio o espaco interno
    if (not e.text is None):
        arquivo.write("\n")
        arquivo.write(espaco + "   " + e.text + "\n")
    
    #Leio os subelementos (onde tudo se repete, por isso a função é recursiva)
    if(len(e) !=0 ):
        for se in e:
            grava_elemento(se,  nome_arquivo = None, arquivo = arquivo, nivel = nivel+1)
            
    #fim da tag
    arquivo.write(espaco + "Fim tag: " + e.tag + "\n")
    arquivo.write("\n")
    
    if(nivel==0):
        arquivo.close()
        
    

def parse_pandas(myroot, nome_arquivo = None):

    colunas=[]
    nomes_colunas=[]
    itens=[]

    if(len(myroot)==0):
        return None

    for elemento in myroot[0]:
        pos = elemento.tag.find("}")   
        colunas.append(elemento.tag)
        nomes_colunas.append(elemento.tag[pos+1:])   #nome da coluna sem o trecho do {http://...}

    for registro in myroot:
        item = []
        for i in range(len(colunas)):
                item.append(None)

        for coluna in colunas:
            posicao = colunas.index(coluna)
            if(not registro.find(coluna) is None):
                item[posicao] = registro.find(coluna).text
            else:
                item[posicao] = ""

        itens.append(item)

    xmlToDf = pd.DataFrame(itens, columns = nomes_colunas)

    if(not nome_arquivo is None):
        xmlToDf.to_csv(nome_arquivo, sep = ";", encoding='utf-8-sig')

    return xmlToDf        


def grava_arquivo(url, arquivo):
    
    print("processando grava_arquivo")
       
    response = requests.get(url)
    
    print("processando parse")
    
    xmldata = response.content
    
    root = ETree.fromstring(xmldata)
    
    parse_pandas(root, arquivo)
        
    print("Finalizado arquivo ", arquivo)
                


'''  
store_items = []
all_items = []
  
for storeno in root.iter():
    
    print(storeno)
    
    #tipo = storeno.attrib.get('type').text
    #language = storeno.find('language').text
  
    #store_items = [tipo, language]
    #all_items.append(store_items)
  
xmlToDf = pd.DataFrame(all_items, columns=[  'tipo', 'language'])
  
print(xmlToDf.to_string(index=False))
'''