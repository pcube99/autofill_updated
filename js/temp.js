var flag = [];
var updateflag = [];
var update_data =[];
var url;
var data,data1;
var count=0;
function httpGetAsync(theUrl, callback)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() { 
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
            callback(xmlHttp.responseText);
    }
    console.log(xmlHttp.responseText)
    xmlHttp.open("GET", theUrl, false); // true for asynchronous 
    xmlHttp.send(null);
}
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

function timer(ms) {
  return new Promise(res => setTimeout(res, ms));
 }

async function fill(data, data1,xx ){
  var login_response;
  chrome.storage.local.get(['login_response'],function(resultt){
   login_response = resultt.login_response;
  });

  for(var yy=0;yy<data.length;yy++){
    if(data[yy]['area-label'].includes(data1[xx]) || data[yy]['dname'].includes(data1[xx]) || data[yy]['name'].includes(data1[xx]) ){
      // console.log(data1[i])
       if(flag[yy]==0){ 
         flag[yy] = 1;
         console.log(data[yy]['dname'].includes(data1[xx]));
         await timer(1000);
         console.log(login_response);
         var dta = JSON.parse(login_response)[xx][data1[xx]];
         chrome.storage.local.set({d1 : data[yy]['id']},function(){
           chrome.storage.local.set({d2: dta},function(){
             chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
               chrome.storage.local.get(['d1'],function(result1){
                 chrome.storage.local.get(['d2'],function(result2){
                   console.log(xx + " " + result1.d1);
                   console.log(xx + " " + result2.d2);
                   chrome.tabs.executeScript(
                       tabs[0].id,
                       {code: "document.getElementById('"+result1.d1+"').value = '"+result2.d2+"';"});
               });
             });    
           });
         });
       });
                  // document.getElementById(data[j]['id']).value = login_response[data1[i]];
         break;
       }
     }
     await timer(1000);
     console.log("time");

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
  httpGetAsync(("https://afss.herokuapp.com/login?email=" + email +"&password=" + password), function(response) {
    chrome.storage.local.set({login_response : response},function(){
    });
  //login_response=response;
  chrome.storage.local.get(['login_response'],function(resultt){
    if(resultt.login_response){
      console.log(resultt.login_response);
      //chrome.storage.local.get({islogin:}, function(result) {
        chrome.storage.local.set({islogin: true}, function(value) {
          console.log('Value is set to ' + value);
          chrome.storage.local.get(['islogin'], function(result) {
           console.log(result);
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

function documentEvents1() {   
   
  document.getElementById('autofill_btn').addEventListener('click', 
    function() { 
      chrome.tabs.query({'active': true, 'lastFocusedWindow': true}, function (tabs) {
        url = tabs[0].url;
    });
    console.log(url);
    httpGetAsync(("https://afss.herokuapp.com/autofill?url=" + url), function(response) {
  var ans=response;
  
  if(ans){
    data = JSON.parse(ans)[0];
    data1 = JSON.parse(ans)[1];
    count = data1.length;
    console.log("count " + count);
    console.log(data)
    console.log(data1.length)
    for(var i =0;i<data1.length;i++){
      flag.push(0);
    }
    for(var j=0;j<data.length;j++){
      updateflag.push(0);
    }
    console.log(flag);
    var i,j;
    for (var xx=0;xx<count;xx++){
      fill(data,data1,xx);
        }
        
      }
    });
  // you can add listeners for other objects ( like other buttons ) here 
});
}

function documentEvents2() {    
  document.getElementById('logout_btn').addEventListener('click', 
    function() { 
      console.log("logouted");
      chrome.storage.local.set({islogin: false}, function(value) {
        console.log('Value is set to ' + value);
        var islogin;
        chrome.storage.local.get(['islogin'], function(result) {
         console.log(result);
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

async function autoupdate_detail(count,i) {
  var fla=0;
  for(var j=0;j<data1.length;j++){
    await timer(2000);
    if(data[i]['dname'].includes(data1[j].replace(/[^a-zA-Z ]/g, "")) == false && updateflag[i]==0 ){
      fla=1;
      updateflag[i]=1;
      break;  
    }
    else{
      fla=0;
    }
  }
  console.log("flag is " + i + " " + fla);
    if(fla == 1){
      await timer(2000);
      chrome.storage.local.set({curr : data[i]['id']},  function(){
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
          chrome.storage.local.get(['curr'],function(result1){
              console.log(i + " " + result1.curr);
              chrome.tabs.executeScript(
                  tabs[0].id,
                  {code: "var xmlHttp = new XMLHttpRequest(); xmlHttp.open('POST', 'https://afss.herokuapp.com/autoupdate?id=' + document.getElementById('"+result1.curr+"').id + '&value=' + document.getElementById('"+result1.curr+"').value, false); xmlHttp.send(null);"});
        });    
      });
    
  });
  fla=0;
  flag.push(1);
    await timer(2000);
    return 0;
}
else return 1;

}


function documentEvents3() {    
  document.getElementById('autoupdate_btn').addEventListener('click', 
    function() { 
      console.log("autoupdate");
      console.log(data);
      console.log(data1);
      for(var i=0;i<data.length;i++){
        var pp =autoupdate_detail(data1.length,i);
        if(pp ==1)
        continue;
        else timer(5000);
      }
  });
}
