const fernet = require('fernet');
const bs58 = require('bs58')

const bookmark = window.location.hash;
const ciphertext = document.getElementById('ciphertext').innerHTML;

var regex = /webui:(\w+)/g;
var secret58 = regex.exec(bookmark)[1];
var secret64 = bs58.decode(secret58).toString();
console.log('Base64 secret: ' + secret64);

var token = new fernet.Token({
  secret: new fernet.Secret(secret64),
  token: ciphertext,
  ttl: 0,
});

var cleartext = token.decode();

document.getElementById('cleartext').innerHTML = cleartext;

console.log('Got cleartext:\n' + cleartext);
