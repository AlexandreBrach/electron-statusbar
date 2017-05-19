
const randomstring = require("randomstring");
const fs = require('fs');

/**
* Read the css from the passed file and put it in lib data
* 
* @param {string} filename - CSS Filename 
* @returns {Promise}
*/
var retrieveCss = function (filename) {
   return new Promise( function( resolve, reject ) {
       fs.readFile(filename, 'utf8', function (err,data) {
           if (err) {
               reject( err );
           } else {
               resolve( data );
           }
       });
   }); 
}

/**
* Generate a random window name based on a prefix
* 
* @param {string} prefix - name prefix 
* @returns {string}
*/
var createWindowTitle = function (prefix) {
    return prefix + randomstring.generate( {
        length: 12,
        charset: 'alphabetic'
    } );
}

module.exports = {
    createWindowTitle: createWindowTitle,
    retrieveCss: retrieveCss
}
