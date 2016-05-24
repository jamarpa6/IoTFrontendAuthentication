function ReplaceContentInContainer(id,content) {
var container = document.getElementById(id);
container.innerHTML = content;
}

function httpGetSync(theUrl, callback)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", theUrl, false); // true for asynchronous 
    xmlHttp.send(null);
    if (xmlHttp==200) callback(xmlHttp.responseText);
    
}
$.get("/volumen",function(resp){ReplaceContentInContainer("volumen_Div",resp);});
