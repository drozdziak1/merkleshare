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

window.copy_btn_click = function(id) {
  document.getElementById(id).select();
  document.execCommand('copy');
  console.log('Copied ' + id + ' to clipboard!');

  var button = document.getElementById('copy-button')
  var before = button.getAttribute('value');

  // Display "Copied!" inside the button for 2 seconds
  button.setAttribute('value', 'Copied!');
  setTimeout(
    function() {
      button.setAttribute('value', before);
    },
    2000
  );

};
