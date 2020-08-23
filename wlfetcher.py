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
    return src.text


def get_meaning(word):
    src = _get_source(word)

    soup = BeautifulSoup(src, 'html5lib')
    title=soup.find("div",class_="pbarTL")
    mean=soup.find("div",class_="kijiWrp")
    if title==None or mean==None:
        aprint("warning: no meaning on ",word)
        return None
    # titles = soup.find_all("div", class_="pbarTL")
    # means = soup.find_all("div",class_="kijiWrp")
    # for i,m in enumerate(titles):
    vary1= title.find_all(title="活用形辞書")+title.find_all(title="丁寧表現辞書")
    if(len(vary1)>0):
        midashigo=mean.find_all("h2",class_="midashigo")
        tmp=midashigo[0].getText()
        choices=tmp.split('、')
        if len(choices)==1:
            newwords=re.findall(r'(?<=「)(.*?)(?=」)',mean.getText())
            newword=newwords[len(newwords)-1]
            aprint("redirect to", newword)
            return get_meaning(newword)
        else:
            aprint("recheck", word, "\n", midashigo[0].getText())
            return None
        # vary2=m.find_all(title="丁寧表現辞書")
        # if (len(vary2) > 0):
        #     reddiv = means[i].find("div",class_="Tnhgj").find("div").find_all("a")
        #     if len(reddiv)>1:
        #         aprint("recheck", word )
        #         return None
        #     newword = reddiv[0]["title"]
        #     aprint("redirect to", newword)
        #     return get_meaning(newword)
    kijis=mean.find_all("h2",class_="midashigo")
    exp=[]
    for kiji in kijis:
        little=kiji.find("span",style="font-size:75%;")#the smaller font
        if little!=None:
            little.extract()
        s=kiji.getText()
        s=str(s)
        # s=re.sub(r'\[[0-9]\]',s)
        kanji=re.search("【(.*?)】",s)
        if kanji!=None:
            kana=re.search(r'(.*?)(?=【)',s)
            exp.append((kana.group(1),kanji.group(1)))
        else:
            yomitag=mean.find("div",class_="Jtnhj")
            if yomitag!=None and yomitag.get_text().find("読み方")>=0:
                yomitext=yomitag.get_text(separator = " ")
                yomi=re.match(r'\s*読み方：\s*(.*?) ',yomitext).group(1)
                exp.append((yomi,s))
            else:
                exp.append((s,s))
    if len(exp)>=2:
        aprint("warning: multiple meanings")
    return exp

if __name__=="__main__":
    # print(get_meaning("出来栄え"))
    mat=np.loadtxt(open("./本好.csv",encoding='utf-8-sig'),dtype=np.str,delimiter=',')
    col=mat.shape[1]
    mat=np.insert(mat, col, values=mat[:,0], axis=1)
    mat=np.insert(mat, col+1, values=mat[:, 1], axis=1)
    for id,word in enumerate(mat[:,0]):
        aprint("\n\n",word)
        m = get_meaning(word)
        aprint(m)
        if m!=None:
            mat[id,col+1]=m[0][0]
            mat[id, col] = m[0][1]
    np.savetxt("out.csv",mat,encoding='utf_8_sig',fmt='%s',delimiter=',')
