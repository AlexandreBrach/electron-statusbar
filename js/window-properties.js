
const x11 = require( 'x11');

var X;

/**
* Return the window name using its id
*
* @param {integer} wid - window id
* @returns {Promise}
*/
var getWindowName = function( wid ) {
  return new Promise( function( resolve, reject ) {
    X.InternAtom(false, '_NET_WM_NAME', function (wmNameErr, wmNameAtom) {
      X.InternAtom(false, 'UTF8_STRING', function (utf8Err, utf8Atom) {
        X.GetProperty(0, wid, wmNameAtom, utf8Atom, 0, 10000000, function(err, nameProp) {
          if( err ) {
            reject( err );
              return
          }
          if( nameProp == undefined ) {
            reject( "unknown window " + wid );
          } else {
              resolve( nameProp.data.toString() );
          }
        });
      });
    });
  });
}

/**
* Return the id of the named window
*
* @param {string} name - window name
* @returns {Promise}
*/
var getWindowId = function (name) {

  return new Promise( function( resolve, reject ) {
      x11.createClient(function( err, display ) {
        X = display.client;
        var root = display.screen[0].root;
        X.QueryTree(root, function(err, tree) {
            tree.children.map( function( id ) {
                let prop = getWindowName( id ).then( function( n ) {
                    if( n === name ) {
                        resolve( id );
                    }
                })
            } );
        })
      });
  });
}

/**
* Set the strut value of the window
* The strut value is an object with the folowing structure :
*
*    strutValues = {
*       left: 0
*       right: 0
*       top: 0
*       bottom: 0
*       left_start_y: 0
*       left_end_y: 0
*       right_start_y: 0
*       right_end_y: 0
*       top_start_x: 0
*       top_end_x: 0
*       bottom_start_x: 0
*       bottom_end_x : 0
*   }
*
* @param {integer} wid - window ID
* @param {object} strutValue - strut values
* @returns {Promise}
*/
var setStrutValues = function (wid, sv ) {

    var values = new Buffer( 4 * 12 );
    values.writeUInt32LE(sv.left           ,0*4 );
    values.writeUInt32LE(sv.right          ,1*4 );
    values.writeUInt32LE(sv.top            ,2*4 );
    values.writeUInt32LE(sv.bottom         ,3*4 );
    values.writeUInt32LE(sv.left_start_y   ,4*4 );
    values.writeUInt32LE(sv.left_end_y     ,5*4 );
    values.writeUInt32LE(sv.right_start_y  ,6*4 );
    values.writeUInt32LE(sv.right_end_y    ,7*4 );
    values.writeUInt32LE(sv.top_start_x    ,8*4 );
    values.writeUInt32LE(sv.top_end_x      ,9*4 );
    values.writeUInt32LE(sv.bottom_start_x ,10*4 );
    values.writeUInt32LE(sv.bottom_end_x   ,11*4 );

    X.InternAtom( false, '_NET_WM_STRUT_PARTIAL', function( err, strutAtom ) {
        X.ChangeProperty(0, wid, strutAtom, X.atoms.CARDINAL, 32, values) ;
    } );
}

module.exports = {
    getWindowId : getWindowId,
    getWindowName: getWindowName,
    setStrutValues: setStrutValues
}
