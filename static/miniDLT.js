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
        keyObj = document.getElementById("private");
        data = JSON.stringify({"payload":{"command":msgObj.value},"port":parseInt(portObj.value),"key":keyObj.value});
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
                strjson = strjson.split("},").join("</ul>}<br/>");
                //strjson = strjson.split("}").join("</ul>}");
                strjson = strjson.split("[").join("<ul class=\"logentry\">");
                strjson = strjson.split("]").join("</ul>");
                strjson = strjson.split("%%,").join("<br/>");
                strjson = strjson.split("%%").join("");
                strjson = "<span class=\"logentry\">"+strjson+"</span>";
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
                if (typeof response["message"] === 'object') strjson = "A JSON Object was sent in response:<br/><br/>"+strjson;
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
        return val.toString()+"<br/><br/><br/>";
    } else if ( name.indexOf('Key') >0 && val.length>16) { // 
        return beautifyKey(val); // remove from result
    } else if ( typeof val === 'string' || typeof val === 'number'||typeof val === 'boolean' ||typeof val === 'date' ) {   
       return val + "%%";
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
        return "["+output+"]";
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
                
function changeVisibility(inputId, iconId){
        inputObj = document.getElementById(inputId);
        iconObj = document.getElementById(iconId);
        if (inputObj && iconObj){
            if (inputObj.type == "password") {
                    inputObj.type ="text";
                    iconObj.innerHTML = "visibility";
                } else {
                    inputObj.type ="password";
                    iconObj.innerHTML = "visibility_off";
                }
            }
        }                