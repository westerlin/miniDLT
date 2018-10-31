function ajax(url,data,callback) {
        var req = false;
        try{
                req = new XMLHttpRequest();
                }
        catch(e) {
                try {
                        req = new ActiveXObject("Msxml2.XMLHTTP");
                        }
                catch(e) {
                        try{
                                req = new ActiceXObject("Microsoft.XMLHTTP");
                                }
                        catch(e) {
                                // browser does not support AJAX
                                return false;
                                }
                        }
                }
        req.open("POST",url,true);
        req.setRequestHeader("Content-Type","application/json");
        req.onreadystatechange = function() {
                if (req.readyState == 4) callback(req);
                    }
        req.send(data);
        return true;
        }

function log(text){
        obj = document.getElementById("logger");
        if(obj)
            obj.innerHTML += "<p class=\"logentry\">"+text+"</p>";
            obj.scrollTop = obj.scrollHeight-obj.offsetHeight -1;
        }        


function sendMessage(){
        msgObj = document.getElementById("message");
        portObj = document.getElementById("port");
        data = JSON.stringify({"payload":{"command":msgObj.value},"port":parseInt(portObj.value)});
        url = "http://localhost:5000/miniDLT";
        if (!ajax(url,data,receiver))
            log("Something went wrong when communicating with rest-API..");
      }


function receiver(req){
        if (req.status==200){
                message = JSON.parse(req.responseText);
                
                strjson = JSON.stringify(message["message"],replacer);
                strjson = strjson.split("\"").join("");
                strjson = strjson.split("{").join("{<ul class=\"logentry\">");
                strjson = strjson.split("}").join("</ul><span class=\"logentry\">}</span>");
                strjson = strjson.split("[").join("<ul class=\"logentry\">");
                strjson = strjson.split("]").join("</ul>");
                strjson = strjson.split(",").join(",<br/>");
                //strjson = strjson.split("\"").join();
                //strjson = strjson.replaceAll("{","<ul class=\"logentry\">");
                //strjson = strjson.replaceAll("}","</ul>");
                //strjson = strjson.replaceAll(",",",<br/>");
                log(strjson);
                }
        else {
            alert("Error Message Code:"+req.status+", "+req.statusText);
                }
        }

function init() {
         log("Servers are online .. ");
         log("Mini DLT is up and running");
        }

function onEnterDown(callback){
        if (event.keyCode==13) callback();
     }

// example replacer function
function replacer(name, val) {
    // convert RegExp to string
    if ( val && val.constructor === RegExp ) {
        return val.toString();
    } else if ( name === 'publicKey' ) { // 
        return beautifyKey(val); // remove from result
    } else {
        return val; // return as is
    }
}
    
function beautifyKey(value){
        fraction = Math.floor(value.length/8);
        count = 0;
        output = "";
        while ((count)*fraction <= value.length) {
            newval = value.slice(count*fraction,(count+1)*fraction);
            if (newval.length>0)
                output += newval+"<br/>";
            count++;                
        }
        return "[["+output+"]]";
 }