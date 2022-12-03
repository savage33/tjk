# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 14:52:42 2022

@author: Savage33
"""

import pandas as pd
from sklearn.preprocessing import OneHotEncoder,LabelEncoder

def get_parantezici(metin):
    bas = metin.find("(")+1
    son=metin.find(")")
    deger=metin[bas:son]
    return deger
def get_Apranti(metin):
    if metin.find("APApranti")!=-1:
        deger=1
    else:
        deger=0
    return deger



veri = pd.read_excel(r"C:\Users\Savage33\OneDrive\Masaüstü\TJK.xlsx")
veri.drop(columns=["Forma","Orijin(Baba - Anne)"],inplace=True)
veri["ilkSira"]=None
veri["Apranti"]=None
veri["AGF_Parantez"]=None
veri["Fark"].astype('category')
veri["ilkSira"]=veri["At İsmi"].apply(lambda x: get_parantezici(x))
veri["At İsmi"]=veri["At İsmi"].apply(lambda x: x[:x.find("(")])
veri["Apranti"]=veri["Jokey"].apply(lambda x: get_Apranti(x) )
veri["Jokey"]=veri["Jokey"].apply(lambda x: x[:x.find("APApranti")])
veri["AGF_Parantez"]=veri["AGF"].apply(lambda x: get_parantezici(x) )
veri["AGF"]=veri["AGF"].apply(lambda x: x[1:x.find("(")])
veri["Yaş"]=veri["Yaş"].apply(lambda x: x[0:x.find("y")])
veri["Fark"]=veri["Fark"].str.replace(" Boy", "")

sutun_S=veri["S"]
sutun_atismi=veri["At İsmi"]
sutun_yas=veri["Yaş"].astype("int32")
sutun_jokey=veri["Jokey"]
sutun_sahip=veri["Sahip"]
sutun_antrenor=veri["Antrenörü"]
sutun_ganyan=veri["Gny"]
sutun_agf=veri["AGF"]
sutun_agfparantez=veri["AGF_Parantez"]
try:
    sutun_S=sutun_S.fillna(0).astype("int32")
except:
    pass

try:
    sutun_ganyan=sutun_ganyan.fillna(0).astype("int32")
except:
    pass

try:
    sutun_agf=sutun_agf.fillna(0).astype("int32")
except:
    pass
try:
    sutun_agfparantez=sutun_agfparantez.fillna(0).astype("int32")
except:
    pass


le_sutun_atismi=LabelEncoder().fit_transform(sutun_atismi)
le_sutun_jokey=LabelEncoder().fit_transform(sutun_jokey)
le_sutun_sahip=LabelEncoder().fit_transform(sutun_sahip)
le_sutun_antrenor=LabelEncoder().fit_transform(sutun_antrenor)

veriler=pd.concat([sutun_yas,sutun_ganyan,sutun_agf,sutun_agfparantez],axis=1)
veriler["Atismi"]=pd.Series(le_sutun_atismi)
veriler["Jokey"]=pd.Series(le_sutun_jokey)
veriler["Sahip"]=pd.Series(le_sutun_sahip)
veriler["Antrenor"]=pd.Series(le_sutun_antrenor)
veriler["Sonuc"]=sutun_S
veri.to_excel(r"C:\Users\Savage33\OneDrive\Masaüstü\TJK_islenmis.xlsx")

