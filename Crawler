# Import

import re
import requests
import pandas as pd
import seaborn as sns

#

def searchKe(communityName,web="https://gz.ke.com/ershoufang/rs"):
    txt=str(communityName.encode('utf-8', 'strict'))
    txt1=txt[2:-1]
    txt2=txt1.replace("\\x", "%")
    txt3=txt2+"/"
    txtRs=web+txt3
    return(txtRs)
    
def getNum(x,str):
    y = re.sub(str, '', x)
    z = float(y)
    return(z)
    
def getBasicInfo(url):
    req = requests.get(url)
    reqStr = req.content.decode("utf-8")
    # totalPrice
    reTotalPrice = re.compile(r'''<div class="totalPrice"><span>.*?</span>万</div>\n''', re.S)
    strTotalPrice = re.findall(reTotalPrice, reqStr)
    # unitPrice
    reUnitPrice = re.compile(r'''<span>单价.*?元/平米</span>\n''', re.S)
    strUnitPrice = re.findall(reUnitPrice, reqStr)
    # generate dataframe and clean
    df=pd.DataFrame({"totalPrice":strTotalPrice,
                     "unitPrice":strUnitPrice})
    df.totalPrice=df.totalPrice.apply(lambda totalPrice:getNum(totalPrice,r'[<div class="totalPrice"><span>/万/\n]'))
    df.unitPrice=df.unitPrice.apply(lambda unitPrice:getNum(unitPrice,r'[<span>单价元/平米</span>\n]'))
    df["square"]=df["totalPrice"]*10000/df["unitPrice"]
    return(df)

def getResult(communityName):
    url=searchKe(communityName)
    df=getBasicInfo(url)
    print(df)
    sns.scatterplot(x="square",y="unitPrice",data=df)
    sns.scatterplot(x="square",y="totalPrice",data=df)

getResult("珠江帝景")
