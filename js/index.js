const ipc = require('electron').ipcRenderer;
 
var appendContent = function( content ) {
    var container = document.getElementById( 'box' )
    var c = container.innerHTML;
    container.innerHTML = content;
}

var setCustomCss = function(css) {
    var node = document.getElementById('customcss');
    node.innerHTML = css;
}

var debug = function( str ) {
    document.getElementById( 'debug' ).innerHTML = str;
}

ipc.on('debug', function(event, str) {
    debug( str );
} );

ipc.on('stdinAction', function(event, str){
    appendContent( str );
} );

ipc.once( 'cssReply', function(event, css) {
    setCustomCss( css );

});
ipc.send( 'getCustomCss', null );
