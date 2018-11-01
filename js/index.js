const fs = require( 'fs' );
const dbus = require( './js/dbus' );
const ipc = require('electron').ipcRenderer;
const ejs = require( 'ejs' )

var setContentWithTemplate = function( data, elementId, template ) {
    setContent( template( {data:data} ), elementId )
}

var setContent = function( content, elementId ) {
    var element = document.getElementById( elementId );
    debug(content)
    if( null === element ) {
        var container = document.getElementById( 'container' )
        element = document.createElement( 'div' );
        element.id = elementId
        container.appendChild( element );
    }
    var c = element.innerHTML;
    element.innerHTML = content;
}

var resolveFilename = function ( filename ) {
    var c = filename.charAt(0)
    return ( '/' == c )
        ? filename
        : CONFIGPATH + '/' + filename;
}

/**
 * Apply Css from a file content
 *
 * @param string filename - path and name of the file to read
 * @param string id - id of the element to apply the css on
 * @returns void
 */
var setCssFromFile = function (filename, id) {
    var filename = resolveFilename(filename)
    fs.readFile( filename, 'UTF-8', function( err, strcss ) {
        if( err ) {
            console.error( err );
        } else {
            setCss( strcss, id );
        }
    } );
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
// get a copy of command line params
var args =  JSON.parse(JSON.stringify( remote.getGlobal('cliArgs')));

console.log('Parameters :')
console.log(args);

var DEBUG = ( 1 == args.params.debugmode ) ? true : false;
function debug( str ) {
    if( DEBUG ) {
        console.log( str );
    }
}

fs.readFile( args.params.css, 'UTF-8', function( err, data ) {
    if (err) {
        setContent( JSON.stringify( err ) );
    } else {
        setCss( data, 'body' );
    }
});

var DBUSCONFIG = args.params.dbus
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
    debug("load template " + config.template + " and attach to event " + config['object'])
    let id = config.id
    var templateFile = resolveFilename(config.template)
    fs.readFile( templateFile, 'UTF-8', function( err, strtemplate ) {
        if( err ) {
            throw 'Unable to open template file "' + templateFile + '"';
        }
        let template = ejs.compile( strtemplate )
        dbus.attach( config.service, config['object'], function( data ) {
            data = JSON.parse( data )
            debug(data);
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
        debug(data);
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
                debug( 'Load following configuration :');
                debug(config);
                if( config['css-file'] ) {
                    debug("load css file" + config['css-file'])
                    setCssFromFile( config['css-file'], config.id );
                }
                if( config.css ) {
                    debug("load raw css " + config.css)
                    setCss( config.css, config.id );
                }
                if( config.template ) {
                    attachEventToTemplate( config )
                } else {
                    debug("no template, the service provide the output ")
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
