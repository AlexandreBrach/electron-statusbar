
var dbus = require('dbus-native');

var sessionBus = dbus.sessionBus();

const SERVICE = 'org.alexandrebrach.toolbar'
const OBJECT = '/org/alexandrebrach/toolbar/xmonad'
const INTERFACE = 'org.alexandrebrach.toolbar.xmonad'
//const INTERFACE = 'org.freedesktop.NetworkManager.Settings'
const SIGNALNAME = 'changes'

// Check the connection was successful
if (!sessionBus) {
	throw new Error ('Could not connect to the DBus session bus.')
}

let service = sessionBus.getService( SERVICE )
let dbObject

/**
 * return the state of the WM
 *
 * @returns {string}
 */
var getState = function () {
    return new Promise( function( resolve, reject ) {
        dbObject.getState( function( err, state ) {
            if( err ) {
                reject( err );
            } else {
                resolve( state );
            }
        } );
    });
}

service.getInterface( OBJECT, INTERFACE, function( e, iface ) {
	if (e || (iface === undefined )) {
		console.error ('Failed to request interface \''
                + INTERFACE + '\' at \'' + OBJECT )
        console.log( e? e : '(no error)' )
		process.exit (1)
	}

    dbObject = iface

    dbObject.on( SIGNALNAME, function( data ) {
        getState().then( function (state ) {
            console.log( state );
        });
    });

});
