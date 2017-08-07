
var dbus = require('dbus-native');

var sessionBus = dbus.sessionBus();

const INTERFACE = 'org.alexandrebrach.toolbar'
const SIGNALNAME = 'changes'

// Check the connection was successful
if (!sessionBus) {
	throw new Error ('Could not connect to the DBus session bus.')
}

let dbObject

/**
 * return the state of the service
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

/**
 * attach a configuration service to a callback
 *
 * @param {object} serviceName - the name of the dbus service
 * @param {object} objectName - name of the dbus object
 * @returns {null}
 */
var attach = function ( serviceName, objectName, callback ) {
    let service = sessionBus.getService( serviceName );

    service.getInterface( objectName, INTERFACE, function( e, iface ) {
        if (e || (iface === undefined )) {
            console.error ('Failed to request interface \''
                    + INTERFACE + '\' at \'' + objectName )
            console.log( e? e : '(no error)' )
            process.exit (1)
        }

        dbObject = iface

        dbObject.on( SIGNALNAME, function( data ) {
            getState().then( function (state ) {
                (callback)( state );
            });
        });

    });
}

module.exports = {
    attach : attach
}
