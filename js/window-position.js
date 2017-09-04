
const electronScreen = require('electron').screen
const winProp = require('./window-properties')

function computeWinProperties( w, positionName, screenNumber ) {
    let displays = electronScreen.getAllDisplays()
    var position = {x:0,y:0};
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

    if( 1 != screenNumber ) {
        if( 1 == displays.length ) {
            screenIndex = 0;
        } else {
            screenIndex = Math.min( screenNumber, displays.length ) - 1
        }
    } else {
        screenIndex = 0;
    }

    let display = displays[screenIndex];
    let screenSize = display.size;
    let screenX = display.bounds.x;
    let screenY = display.bounds.y;

    switch( positionName ) {
        case 'bottom' :
            position.x = screenX;
            position.y = screenY + screenSize.height - winHeight;
            winWidth = screenSize.width
            strutValues.bottom = winHeight
            strutValues.top_start_x = position.x;
            strutValues.top_end_x = position.x + winWidth;
            break;
        case 'top' :
        default:
            position.x = screenX;
            position.y = screenY + 0;
            winWidth = screenSize.width;
            strutValues.top = winHeight;
            strutValues.top_start_x = position.x;
            strutValues.top_end_x = position.x + winWidth;

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
