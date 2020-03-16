from bs4 import BeautifulSoup
import requests
import re
import numpy as np
import time


f = open("log.txt", "w",encoding='utf-8-sig')

def aprint(*args):
    print(*args)
    print(*args,file=f)

def _get_source(word):
    time.sleep(1)
    conti=True
    while conti:
        try:
            src = requests.get("http://www.weblio.jp/content/" + word)
            conti=False
        except:
            time.sleep(60)
    return src.textw


def get_meaning(word):
    src = _get_source(word)

    soup = BeautifulSoup(src, 'html5lib')
    main=soup.find("div",class_="pbarTL")
    first=soup.find("div",class_="kijiWrp")
    if main==None or first==None:
        return None
    vary=main.find_all(title="活用形辞書")+main.find_all(title="丁寧表現辞書")
    if(len(vary)>0):
        midashigo=first.find_all("h2",class_="midashigo")
        tmp=midashigo[0].getText()
        choices=tmp.split('、')
        if len(choices)==1:
            newwords=re.findall(r'(?<=「)(.*?)(?=」)',first.getText())
            newword=newwords[len(newwords)-1]
            aprint("redirect to", newword)
            return get_meaning(newword)
        else:
            aprint("recheck", word, "\n", midashigo[0].getText())
            return None
    kijis=first.find_all("h2",class_="midashigo")
    exp=[]
    for kiji in kijis:
        little=kiji.find("span",style="font-size:75%;")#the smaller font
        if little!=None:
            little.extract()
        s=kiji.getText()
        s=str(s)
        # s=re.sub(r'\[[0-9]\]',s)
        aprint(s)
        kanji=re.search("【(.*?)】",s)
        if kanji!=None:
            kana=re.search(r'(.*?)(?=【)',s)
            exp.append((kana.group(1),kanji.group(1)))
        else:
            exp.append((s,s))
    if len(exp)>=2:
        aprint("warning: multiple meanings")
    return exp

if __name__=="__main__":
    mat=np.loadtxt(open("./初级下.csv",encoding='utf-8-sig'),dtype=np.str,delimiter=',')
    for id,word in enumerate(mat[:,0]):
        aprint("\n\n",word)
        m=get_meaning(word)
        if m!=None:
            mat[id,1]=m[0][0]
            mat[id, 0] = m[0][1]
    np.savetxt("out.csv",mat,encoding='utf_8_sig',fmt='%s',delimiter=',')
