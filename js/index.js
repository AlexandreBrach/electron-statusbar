const fs = require( 'fs' );
const dbus = require( './js/dbus' );
const ipc = require('electron').ipcRenderer;
const ejs = require( 'ejs' )

var setContentWithTemplate = function( data, elementId, template ) {
    setContent( template( {data:data} ), elementId )
}

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

var DBUSCONFIG = args.params.dbus
var DEBUG = ( 1 == args.params.debug ) ? true : false;
if( DBUSCONFIG ) {
    mode = 'dbus'
    var CONFIGPATH = require('path').dirname( DBUSCONFIG )
} else {
    mode = 'stdin'
}

/**
 * Attach a DBUS signal to a template rendering
 *
 * @param {object} config - configuration
 * @returns {null}
 */
var attachEventToTemplate = function (config) {
    let id = config.id
    let templateFile = CONFIGPATH + '/' + config.template
    fs.readFile( templateFile, 'UTF-8', function( err, strtemplate ) {
        if( err ) {
            throw 'Unable to open template file "' + templateFile + '"';
        }
        let template = ejs.compile( strtemplate )
        dbus.attach( config.service, config['object'], function( data ) {
            data = JSON.parse( data )
            if( DEBUG ) {
                console.log( data )
            }
            setContentWithTemplate( data, id, template );
        });
    } );
}

/**
 * Attach a DBUS signal to a direct rendering process
 *
 * @param {object} config - configuration
 * @returns {null}
 */
var attachEventToRendering = function (config) {
    let id = config.id
    dbus.attach( config.service, config['object'], function( data ) {
        if( DEBUG ) {
            console.log( data )
        }
        setContent( data, id );
    });
}

if( mode == 'dbus' ) {
    // DBUS mode
    fs.readFile( DBUSCONFIG, 'UTF-8', function( err, data ) {

        if (err) {
            throw 'Unable to read config from ' + DBUSCONFIG
        } else {
            data = data.replace( /\n/g, '' );
            try {
                var configs = JSON.parse( data )
            } catch (e) {
                throw 'Unable to parse config from ' + DBUSCONFIG
            }
            if( !Array.isArray( configs )) {
                configs = [configs]
            }
            for( var i=0; i < configs.length; i++ ) {
                var config = configs[i]
                if( config.css ) {
                    setCss( config.css, config.id );
                }
                if( config.template ) {
                    attachEventToTemplate( config )
                } else {
                    attachEventToRendering( config )
                }
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
