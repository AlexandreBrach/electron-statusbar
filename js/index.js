const fs = require( 'fs' );
const dbus = require( './js/dbus' );
const ipc = require('electron').ipcRenderer;

var setContent = function( content, elementId ) {
    var element = document.getElementById( elementId );
    if( null === element ) {
        var container = document.getElementById( 'container' )
        element = document.createElement( 'div' );
        element.id = elementId
        container.appendChild( element );
    }
    var c = element.innerHTML;
    element.innerHTML = content;
}

var setCss = function( content, id ) {
    var element = document.getElementById( 'css-' + id )
    if( null === element ) {
        var container = document.getElementById( 'body' )
        element = document.createElement( 'style' );
        element.id = 'css-' + id
        container.appendChild( element );
    }
    var c = element.innerHTML;
    element.innerHTML = content;
}

var remote = require('electron').remote
var args = remote.getGlobal('cliArgs');

fs.readFile( args.params.css, 'UTF-8', function( err, data ) {

    if (err) {
        setContent( JSON.stringify( err ) );
    } else {
        setCss( data, 'body' );
    }

});

let dbusConfig = args.params.dbus
if( dbusConfig ) {
    mode = 'dbus'
} else {
    mode = 'stdin'
}

if( mode == 'dbus' ) {
    // DBUS mode
    fs.readFile( dbusConfig, 'UTF-8', function( err, data ) {

        if (err) {
            throw 'Unable to read config from ' + dbusConfig
        } else {
            data = data.replace( /\n/g, '' );
            try {
                var configs = JSON.parse( data )
            } catch (e) {
                throw 'Unable to parse config from ' + dbusConfig
            }
            if( !Array.isArray( configs )) {
                configs = [configs]
            }
            for( var i=0; i < configs.length; i++ ) {
                let config = configs[i]
                if( config.css ) {
                    setCss( config.css, config.id );
                }
                dbus.attach( config.service, config['object'], function( data ) {
                    setContent( data, config.id );
                });
            }
        }
    });

} else {
    // stdin mode
    ipc.on('stdinAction', function(event, str){
        setContent( str );
    } )
    .catch( err => {
        document.write( JSON.stringify( err ) )
    } );
}
