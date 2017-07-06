const fs = require( 'fs' );
const ipc = require('electron').ipcRenderer;
 
var setContent = function( content ) {
    var container = document.getElementById( 'box' )
    var c = container.innerHTML;
    container.innerHTML = content;
}

var setCss = function( content ) {
    var container = document.getElementById( 'css-import' )
    var c = container.innerHTML;
    container.innerHTML = content;
}

var remote = require('electron').remote
var args = remote.getGlobal('cliArgs');

fs.readFile( args.params.css, 'UTF-8', function( err, data ) {

    if (err) {
        setContent( JSON.stringify( err ) );
    } else {
        setCss( data );
    }

});

ipc.on('stdinAction', function(event, str){
    setContent( str );
} )
.catch( err => { 
    document.write( JSON.stringify( err ) )
} );
