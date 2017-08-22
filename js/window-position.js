
const electronScreen = require('electron').screen
const winProp = require('./window-properties')

function computeWinProperties( w, positionName, screenId ) {
    let displays = electronScreen.getAllDisplays()
    console.log( displays )
    var position = {x:0,y:0};
    let screenSize = electronScreen.getPrimaryDisplay().size
    var [winWidth,winHeight] = w.getSize()
    let strutValues = {
        left: 0,
        right: 0,
        top: 0,
        bottom: 0,
        left_start_y: 0,
        left_end_y: 0,
        right_start_y: 0,
        right_end_y: 0,
        top_start_x: 0,
        top_end_x: 0,
        bottom_start_x: 0,
        bottom_end_x : 0
    }

    switch( positionName ) {
        case 'bottom' :
            position.y = screenSize.height - winHeight;
            winWidth = screenSize.width
            strutValues.bottom = winHeight
            break;
        case 'top' :
        default:
            position.y = 0;
            winWidth = screenSize.width
            strutValues.top = winHeight

    }
    w.setPosition( position.x, position.y )
    w.setSize( winWidth, winHeight )

    return new Promise( function( resolve, reject ) {
        winProp.getWindowId( w.getTitle() ).then( function( wid ) {
            winProp.setStrutValues( wid, strutValues )
            resolve( true );
        } ).catch( function( err ) {
            reject( err );
        });
    });

}

module.exports = {
    computeWinProperties : computeWinProperties
}
