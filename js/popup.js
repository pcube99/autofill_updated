var flag = [];
var updateflag = [];
var update_data =[];
var url;
var data,data1;
var count=0;
var boolemail =false;
var boolpassword = false;
var istransactioncomplete=true;
setTimeout(function(){
  chrome.storage.local.get(['islogin'], function(result) {
    if(result.islogin){
      document.getElementById('container').style.display = "none";
      document.getElementById('logined').style.display = "block";
    }
  else{
    document.getElementById('container').style.display = "block";
    document.getElementById('logined').style.display = "none";
  }
  });  
},1500);


function url_convert(url){
  var website_url = url.split('//').pop().split('/')[0];
  return website_url.split(".").join("");
}
function httpGetAsync(theUrl, callback)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() { 
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
            callback(xmlHttp.responseText);
    }
    xmlHttp.open("GET", theUrl, false); // true for asynchronous 
    xmlHttp.send(null);
}


function timer(ms) {
  return new Promise(res => setTimeout(res, ms));
 }

async function fill(data, data1,xx ){
  document.getElementById('autofill_btn').style.display = 'none';

  for(var yy=0;yy<data.length;yy++){
    if(data1[xx] == 'email' && boolemail==true)
    continue;

    
    

    if(data[yy]['area-label'].includes(data1[xx].toLowerCase()) || data[yy]['dname'].includes(data1[xx].toLowerCase()) || data[yy]['name'].includes(data1[xx].toLowerCase())){
       if(flag[yy]==0){ 
         flag[yy] = 1;
         await timer(500);
         var dta;
      
        chrome.storage.local.get(['login_response'],function(resultt){
        dta = JSON.parse(resultt.login_response)[xx][data1[xx]];
         chrome.storage.local.set({d1 : data[yy]['name']},function(){
           chrome.storage.local.set({d2: dta},function(){
             chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
               chrome.storage.local.get(['d1'],function(result1){
                 chrome.storage.local.get(['d2'],function(result2){
                   chrome.tabs.executeScript(
                       tabs[0].id,
                       {code: "document.getElementsByName('"+result1.d1+"')[0].value = '"+result2.d2+"';"});
               
           });
         });
       });
      });  
    
    });  
  });
         break;
       }
       
    }
     await timer(1500);
     if(yy == xx-1)
        document.getElementById('autofill_btn').style.display = 'block';
     await password_manager();
    }

  
}
document.addEventListener('DOMContentLoaded', documentEvents  , false);
document.addEventListener('DOMContentLoaded', documentEvents1  , false);
document.addEventListener('DOMContentLoaded', documentEvents2  , false);
document.addEventListener('DOMContentLoaded', documentEvents3  , false);

var email;
var password;
var login_response;
function myAction(email, pass) { 
  email = email.value;
  password = pass.value;
  chrome.storage.local.set({login_email : email},function(){
  });
  chrome.storage.local.set({login_password : password},function(){
  });
  httpGetAsync(("https://autofill-sen.herokuapp.com/login?email=" + email +"&password=" + password), function(response) {
    chrome.storage.local.set({login_response : response},function(){
    });
  //login_response=response;
  chrome.storage.local.get(['login_response'],function(resultt){
    if(resultt.login_response){
      //chrome.storage.local.get({islogin:}, function(result) {
        chrome.storage.local.set({islogin: true}, function(value) {
          chrome.storage.local.get(['islogin'], function(result) {
            if(result.islogin){
          document.getElementById('container').style.display = "none";
          document.getElementById('logined').style.display = "block";
            }
          else{
            document.getElementById('container').style.display = "block";
          document.getElementById('logined').style.display = "none";
          }
            
          });     
        });
    }
  });
  
});
}
function documentEvents() {    
  document.getElementById('ok_btn').addEventListener('click', 
    function() { myAction(document.getElementById('name_textbox'), document.getElementById('pass_textbox'));
  });
  // you can add listeners for other objects ( like other buttons ) here 
}

async function password_manager(){
  //add here
  var fill_website_email = 'email' + url_convert(url);
  var fill_website_password = 'password' + url_convert(url);

  
  for(var i=0;i<data1.length;i++){
      if(fill_website_email==data1[i]){
        var temp =i;
        boolemail=true;
        chrome.storage.local.get(['login_response'],function(resultt){
        chrome.storage.local.set({data_website_email : JSON.parse(resultt.login_response)[temp][data1[temp]]},  function(){
          chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
            chrome.storage.local.get(['data_website_email'],function(new_fill_website_email){
                chrome.tabs.executeScript(
                    tabs[0].id,
                    {code: "document.getElementsByName('email')[0].value = '"+new_fill_website_email.data_website_email+"';"});
            
        });
      });
      });
    });
      }
    
    if(fill_website_password == data1[i]){

    var temp1 =i;
    boolpassword=true;
      chrome.storage.local.get(['login_response'],function(resultt){
      chrome.storage.local.set({data_website_password : JSON.parse(resultt.login_response)[temp1][data1[temp1]]},  function(){
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
          chrome.storage.local.get(['data_website_password'],function(new_fill_website_password){
              chrome.tabs.executeScript(
                  tabs[0].id,
                  {code: "document.getElementsByName('password')[0].value = '"+new_fill_website_password.data_website_password+"';"});
          
      });
    });
    });
  });
    }
    
  }
}
function documentEvents1() {   
   
  document.getElementById('autofill_btn').addEventListener('click', 
    function() { 
      

        chrome.tabs.query({'active': true, 'lastFocusedWindow': true}, function (tabs) {
          url = tabs[0].url;
      });
     
    httpGetAsync(("https://autofill-sen.herokuapp.com/autofill?url=" + url), function(response) {
  var ans=response;
  flag=[];
  if(ans){
    data = JSON.parse(ans)[0];
    data1 = JSON.parse(ans)[1];
    count = data1.length;
    for(var i =0;i<data1.length;i++){
      flag.push(0);
    }
    for(var j=0;j<data.length;j++){
      updateflag.push(0);
    }
    var i,j;
    for (var xx=0;xx<=data1.length;xx++){
      fill(data,data1,xx);
        }
        
      }
    });

    

  // you can add listeners for other objects ( like other buttons ) here 
});
  if(typeof url === "undefined")
  {
    document.getElementById("autofill_btn").click();
  }
}

function documentEvents2() {    
  document.getElementById('logout_btn').addEventListener('click', 
    function() { 
      chrome.storage.local.set({islogin: false}, function(value) {
        var islogin;
        chrome.storage.local.get(['islogin'], function(result) {
          if(result.islogin){
        document.getElementById('container').style.display = "none";
        document.getElementById('logined').style.display = "block";
          }
        else{
          document.getElementById('container').style.display = "block";
        document.getElementById('logined').style.display = "none";
        }
          
        });     
      });

  });
  // you can add listeners for other objects ( like other buttons ) here 
}

var ii = 0;                     
var timeoutt;
function myLoop (x) {    
  document.getElementById('autoupdate_btn').style.display = "none";       
   timeoutt = setTimeout(function () {  
    if(updateflag[ii] == 0){
      chrome.storage.local.set({curr : data[ii]['name']},  function(){
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
          chrome.storage.local.get(['curr'],function(result1){
              chrome.tabs.executeScript(
                  tabs[0].id,
                  {code: "var xmlHttp = new XMLHttpRequest(); xmlHttp.open('POST', 'https://autofill-sen.herokuapp.com/autoupdate?id=' + document.getElementsByName('"+result1.curr+"')[0].name.replace(/[^a-zA-Z ]/g, '') + '&value=' + document.getElementsByName('"+result1.curr+"')[0].value, false); xmlHttp.send(null);"});
        });    
      });
    
  });
  updateflag[ii]=1;
    }
flag.push(1);
      ii++;                     
      if (ii < x) {            
         myLoop(x);              
      }       
      else{

        document.getElementById('autoupdate_btn').style.display = "block";
        istransactioncomplete=true;
        clearTimeout(timeoutt);
      }                 
   }, 2000)
}

function documentEvents3() {    
  document.getElementById('autoupdate_btn').addEventListener('click', 
    function() { 
      istransactioncomplete =false;
      chrome.tabs.query({'active': true, 'lastFocusedWindow': true}, function (tabs) {
        url = tabs[0].url;
    });
    httpGetAsync(("https://autofill-sen.herokuapp.com/autofill?url=" + url), function(response) {
  var ans=response;
  flag=[];
  updateflag = []
    data = JSON.parse(ans)[0];
    data1 = JSON.parse(ans)[1];
    count = data1.length;
    for(var i =0;i<data1.length;i++){
      flag.push(0);
    }
    for(var j=0;j<data.length;j++){
      updateflag.push(0);
    }
    });
    
       //myLoop(data1.length);
       for(var ii=0;ii<data1.length;ii++){
       for(var j=0;j<data.length;j++){
         if((data1[ii].includes("password")))
          continue;
        if(data[j]['dname'].includes(data1[ii].replace(/[^a-zA-Z ]/g, "").toLowerCase()) && updateflag[j]==0 ){
          fla=1;
          updateflag[j]=1;
          break;  
        }
      }
    }
      myLoop(data.length);
      httpGetAsync(("https://autofill-sen.herokuapp.com/autofill?url=" + url), function(response) {
        var ans=response;
        if(ans){
          data = JSON.parse(ans)[0];
          data1 = JSON.parse(ans)[1];
        }
        });
        var website_url = url_convert(url);
        var website_password =url_convert(url) ;
        chrome.storage.local.set({website_url : website_url},  function(){
        });
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
          chrome.storage.local.get(['website_url'],function(website){

              chrome.tabs.executeScript(
                  tabs[0].id,
                  {code: "var xmlHttp = new XMLHttpRequest(); xmlHttp.open('POST', 'https://autofill-sen.herokuapp.com/autoupdate?id=email' +'"+ website.website_url+"'  + '&value=' + document.getElementsByName('email')[0].value, false); xmlHttp.send(null);"});
          
      });
    });
    

    chrome.storage.local.set({website_password : website_password},  function(){
    });
      chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        chrome.storage.local.get(['website_password'],function(website){
                      chrome.tabs.executeScript(
                tabs[0].id,
                {code: "var xmlHttp = new XMLHttpRequest(); xmlHttp.open('POST', 'https://autofill-sen.herokuapp.com/autoupdate?id=password' +'"+ website.website_password+"'  + '&value=' + document.getElementsByName('password')[0].value, false); xmlHttp.send(null);"});
        
    });
  });
  
 
  chrome.storage.local.get(['login_email'],function(result111){
    chrome.storage.local.get(['login_password'],function(result112){
  httpGetAsync(("https://autofill-sen.herokuapp.com/login?email=" + result111.login_email +"&password=" + result112.login_password), function(response) {
    chrome.storage.local.set({login_response : response},function(){
    });
  });

    
}); 
});
 
         
  if(typeof url === "undefined")
  {
    document.getElementById("autoupdate_btn").click();
  }
});
}
