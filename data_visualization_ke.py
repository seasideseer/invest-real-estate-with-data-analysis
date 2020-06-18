# Import

import re
import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
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
    # community name
    reCm = re.compile(r'''<div class="positionInfo">
                  <span class="positionIcon"></span>
                                      <a href="https://gz.ke.com/xiaoqu/.*?/">.*?</a>
                                                    </div>\n''', re.S)
    strCm = re.findall(reCm, reqStr)
    # generate dataframe and clean
    df=pd.DataFrame({"totalPrice":strTotalPrice,
                     "unitPrice":strUnitPrice,
                     "cmRaw":strCm})
    df.totalPrice=df.totalPrice.apply(lambda totalPrice:getNum(totalPrice,r'[<div class="totalPrice"><span>/万/\n]'))
    df.unitPrice=df.unitPrice.apply(lambda unitPrice:getNum(unitPrice,r'[<span>单价元/平米</span>\n]'))
    df["square"]=df["totalPrice"]*10000/df["unitPrice"]
    df["cmName"]=df.cmRaw.replace(to_replace=['''<div class="positionInfo">\n                  <span class="positionIcon"></span>\n                                      <a href="https://gz.ke.com/xiaoqu/.*?/">''',
                                  '''</a>\n                                                    </div>\n'''],value="", regex=True)
    df["cmCode"]=df.cmRaw.replace(to_replace=['''<div class="positionInfo">\n                  <span class="positionIcon"></span>\n                                      <a href="https://gz.ke.com/xiaoqu/''',
                                  '''/">.*?</a>\n                                                    </div>\n'''],value="", regex=True)
    df=df.drop(columns=['cmRaw'])
    return(df)
    
def getResult(communityName):
    url=searchKe(communityName)
    df=getBasicInfo(url)
    print(df)
    sns.scatterplot(x="square",y="unitPrice",data=df)
    sns.scatterplot(x="square",y="totalPrice",data=df)

def getResultDataFrame(communityName):
    url=searchKe(communityName)
    df=getBasicInfo(url)
    return(df)
    
def getMultiResultDataFrame(communityList):
    cl=communityList.split("/")
    dfRes=pd.DataFrame()
    for i in range(len(cl)):
        df=getResultDataFrame(cl[i])
        df["cmNameS"]=cl[i]
        dfRes=dfRes.append(df)
    return(dfRes)
    
def plotUnitPrice(communityList):
    df=getMultiResultDataFrame(communityList)
    sns.boxplot(y='unitPrice', x='cmNameS', 
                 data=df)
    plt.xlabel("")
    plt.ylabel("unit price")

def plotTotalPrice(communityList):
    df=getMultiResultDataFrame(communityList)
    sns.boxplot(y='totalPrice', x='cmNameS', 
                 data=df)
    plt.xlabel("")
    plt.ylabel("total price")  

def plotSquare(communityList):
    df=getMultiResultDataFrame(communityList)
    sns.boxplot(y='square', x='cmNameS', 
                 data=df)
    plt.xlabel("")
    plt.ylabel("square")
    
def plotSquareTotalPrice(communityList):
    df=getMultiResultDataFrame(communityList)
    sns.scatterplot(x='square', y='totalPrice',size="unitPrice",hue="cmNameS", 
                 data=df)
    plt.xlabel("Square")
    plt.ylabel("Total Price")

plotSquareTotalPrice("丽园雅庭/名雅苑/嘉仕花园")
