
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
          }
          resolve( nameProp.data.toString() );
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
* 
* @param {integer} wid - window ID 
* @returns {Promise}
*/
var setStrutValues = function (wid, 
        left, right, 
        top, bottom, 
        left_start_y, left_end_y, 
        right_start_y, right_end_y, 
        top_start_x, top_end_x, 
        bottom_start_x, bottom_end_x ) {

    var values = new Buffer( 4 * 12 );
    values.writeUInt32LE(left           ,0*4 );
    values.writeUInt32LE(right          ,1*4 );
    values.writeUInt32LE(top            ,2*4 );
    values.writeUInt32LE(bottom         ,3*4 );
    values.writeUInt32LE(left_start_y   ,4*4 );
    values.writeUInt32LE(left_end_y     ,5*4 );
    values.writeUInt32LE(right_start_y  ,6*4 );
    values.writeUInt32LE(right_end_y    ,7*4 );
    values.writeUInt32LE(top_start_x    ,8*4 );
    values.writeUInt32LE(top_end_x      ,9*4 );
    values.writeUInt32LE(bottom_start_x ,10*4 );
    values.writeUInt32LE(bottom_end_x   ,11*4 );

    X.InternAtom( false, '_NET_WM_STRUT_PARTIAL', function( err, strutAtom ) {
        X.ChangeProperty(0, wid, strutAtom, X.atoms.CARDINAL, 32, values) ;
    } );
}

module.exports = {
    getWindowId : getWindowId,
    getWindowName: getWindowName,
    setStrutValues: setStrutValues
}
