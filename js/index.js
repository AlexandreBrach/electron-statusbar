//const getStdin = require('get-stdin');
const fs = require( 'fs' );
const ipc = require('electron').ipcRenderer;
 
var appendContent = function( content ) {
    var container = document.getElementById( 'box' )
    var c = container.innerHTML;
    container.innerHTML = content;
    //container.innerHTML = c + content;
}

ipc.on('stdinAction', function(event, str){
    appendContent( str );
} )
.catch( err => { 
    document.write( JSON.stringify( err ) )
} );
        
var remote = require('electron').remote
var args = remote.getGlobal('cliArgs');

