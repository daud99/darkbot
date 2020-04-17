/*
document.cookie = 'ip'+'='+'192.101.1.1';
console.log('aaaa')
$(document).ready(function(){
    console.log('aaaa')
    document.cookie = 'ip'+'='+'192.101.1.1';
});

*/
// FREE: no request linit for ipify.org
console.log('hay hay hay');

function getIP(json) {
    $.getJSON('https://api.ipify.org?format=json', function(data){
    //alert(data.ip);
    document.cookie= 'ip'+'='+data.ip;
    //return data.ip;
});
}
var x = getIP();
//console.log(x);



//console.log(ipAddress)
