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
            obj.innerHTML += "<p>"+text+"</p>";
            obj.scrollTop = obj.scrollHeight-obj.offsetHeight -1;
        }        


function sendMessage(){
        data = JSON.stringify({"message":"Hello"});
        url = "http://localhost:3401";
        if (ajax(url,data,receiver))
            log("Message was sent");
         ;
      }


function receiver(req){
        if (req.status==200){
                message = JSON.parse(req.responseText);
                log(message["message"])
                }
        else {
            alert("Error Message Code:"+req.status+", "+req.statusText);
                }
        }

function init() {
         log("Servers are online .. ");
        }