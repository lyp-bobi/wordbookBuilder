suc=""
fail=""
xmlHttp = new XMLHttpRequest();


function loadWords(){
  nl=document.getElementsByClassName("wordlist")[0].childNodes[0].childNodes[0].childNodes
  for(i=0;i<nl.length;i++){
    if(nl[i].nodeName=="TR"){
      word = nl[i].childNodes[1].innerText
      exp = nl[i].childNodes[3].innerText
      ahref = "https://dict.hjenglish.com/jp/jc/"+word
      xmlHttp.open("GET",ahref,false);
      xmlHttp.send(null);
      let res = xmlHttp.responseText.replace(/\n/g,"");
      if(res.match(/class=\"pronounces\">(.*?)<\Sdiv/)!=null){
        sound="\t" + res.match(/class=\"pronounces\">(.*?)<\Sdiv/)[1].replace(/<.*?>/g,"").replace(/^\s+/,"").replace(/\s+/g," ");
        suc += word +"\t"+sound+"\t"+exp+"\n";
      }
      else{
        sound = word;
        fail+= word +"\t"+sound+"\t"+exp+"\n";
      }
    }
  }
}

function nextPage(){
  foot=document.getElementsByClassName("pagination-next-page")[0];
  foot.click()
}

function fakeClick(obj) {
  var ev = document.createEvent("MouseEvents");
  ev.initMouseEvent("click", true, false, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
  obj.dispatchEvent(ev);
}

function exportRaw(name, data) {
  var urlObject = window.URL || window.webkitURL || window;
  var export_blob = new Blob([data]);
  var save_link = document.createElementNS("http://www.w3.org/1999/xhtml", "a")
  save_link.href = urlObject.createObjectURL(export_blob);
  save_link.download = name;
  fakeClick(save_link);
}

function recursive(){
  if(document.getElementsByClassName("pagination-foot active").length==0&&document.getElementsByClassName("pagination-next-page").length>0){
    window.setTimeout(function(){loadWords();nextPage();recursive()},10000);
  }else{
    loadWords();
    words=suc+fail
    exportRaw("words.txt",words)
  }
}

recursive()


