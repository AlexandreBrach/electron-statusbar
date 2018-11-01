
var dbus = require('dbus-native');

var sessionBus = dbus.sessionBus();

const INTERFACE = 'org.alexandrebrach.toolbar'
const SIGNALNAME = 'changes'

// Check the connection was successful
if (!sessionBus) {
	throw new Error ('Could not connect to the DBus session bus.')
}

var dbObject = []

/**
 * return the state of the service
 *
 * @returns {string}
 */
var getState = function (iface) {
    return new Promise( function( resolve, reject ) {
        iface.getState( function( err, state ) {
            if( err ) {
                reject( err );
            } else {
                console.log(state);
                resolve( state );
            }
        } );
    });
}

/**
 * Attach a configuration service to a callback
 * The callback will be called a first time after the attachment
 *
 * @param {object} serviceName - the name of the dbus service
 * @param {object} objectName - name of the dbus object
 * @returns {null}
 */
var attach = function ( serviceName, objectName, callback ) {
    var service = sessionBus.getService( serviceName );

    console.log('retrieveing interface ' + objectName + '...');
    service.getInterface( objectName, INTERFACE, function( e, iface ) {
        if(e) {
            console.error(e.join('\n'))
        } else {
            console.log(iface)
            //if (e || (iface === undefined )) {
                //console.error ('Failed to request interface \''
                        //+ INTERFACE + '\' at \'' + objectName )
                //console.log( e? e : '(no error)' )
                //process.exit (1)
            //}

            iface.on( SIGNALNAME, function( data ) {
                getState(iface).then( function (state ) {
                    (callback)( state );
                });
            });

            getState(iface).then( function (state ) {
                (callback)( state );
            });
            dbObject.push( iface )
        }

    });
}

module.exports = {
    attach : attach
}
