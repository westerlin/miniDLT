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
            date = new Date();
            logtimer = date.toTimeString().slice(0,8)+" ";
            logtimer += ("0" + (date.getDay())).slice(-2)+"-";
            logtimer += ("0" + (date.getMonth() +　1)).slice(-2)+"-";
            logtimer += (""+date.getYear()).slice(-2);
            
            obj.innerHTML += "<p class=\"logentry\">"+logtimer+": "+text+"</p>";
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


function sendRaw(msg,port){
        data = JSON.stringify({"request":"user"});
        url = "http://localhost:5000/json";
        if (!ajax(url,data,receiver))
            log("Something went wrong when communicating with rest-API..");
      }


function receiver(req){
        if (req.status==200){
                response = JSON.parse(req.responseText);
                
                strjson = JSON.stringify(response["message"],replacer).slice(1, -1);
                strjson = strjson.split("\"").join("");
                strjson = strjson.split("{").join("{<ul class=\"logentry\">");
                strjson = strjson.split("}").join("</ul><span class=\"logentry\">}</span>");
                strjson = strjson.split("[").join("<ul class=\"logentry\">");
                strjson = strjson.split("]").join("</ul>");
                strjson = strjson.split(",").join(",<br/>");
                
                keys = response["message"]["base"];
                if (keys) {
                        obj = document.getElementById("prvkey")
                        obj.value = keys["privateKey"];
                        obj = document.getElementById("pubkey")
                        obj.value = keys["publicKey"];
                    }
                
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
         showPanel(0);
        }

function onEnterDown(callback){
        if (event.keyCode==13) callback();
     }

// example replacer function
function replacer(name, val) {
    // convert RegExp to string
    if ( val && val.constructor === RegExp ) {
        return val.toString();
    } else if ( name.indexOf('Key') >0 && val.length>16) { // 
        return beautifyKey(val); // remove from result
    } else {
        return val; // return as is
    }
}
    
function beautifyKey(value){
        fraction = Math.floor(value.length/16);
        count = 0;
        output = "";
        while ((count) <= fraction) {
            newval = value.slice(count*16,(count+1)*16);
            if (newval.length>0)
                output += newval+"<br/>";
            count++;                
        }
        return "[["+output+"]]";
 }
        
function showPanel(number){
        panels = document.getElementsByClassName("panel_form");
        console.log(panels.lenght)
        for (i=0;i<panels.length;i++){
                if (i != number){
                    console.log("Hiding panel "+i)
                    panels[i].classList.add("hide");
                } else {
                    panels[i].classList.remove("hide");
            }
     }
   }