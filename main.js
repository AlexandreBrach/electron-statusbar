let DEBUG = process.env.DEBUG
let DEV = process.env.DEV

const {app, BrowserWindow} = require('electron')
const path = require('path')
const url = require('url')
const readline = require('readline');
const Positioner = require('electron-positioner')
const winProp = require('./js/window-properties')
const BarOptions = require('./js/options')
const ipc = require('electron').ipcMain

if( DEV ) {
    var client = require('electron-connect').client;
}

// parse cli parameter
var cliArgs = require( './js/cli-arguments.js' )
cliArgs.init( process.argv )
global.cliArgs = cliArgs

var barHeight = 40
var cssFile = cliArgs.get( 'css' )
//var cssFile = "/home/alex/workspace/electron-status-bar/examples/custom.css"

// Keep a global reference of the window object, if you don't, the window will
// be closed automatically when the JavaScript object is garbage collected.
let mainWindow
let positioner

let windowTitle = BarOptions.createWindowTitle( 'electronbar' )

var debug = (str) => {
    mainWindow.webContents.send('debug', str);
}

/**
 * Load index.html in the bar
 * 
 */
var loadHTML = function () {
    mainWindow.loadURL(url.format({
      pathname: path.join(__dirname, 'index.html'),
      'node-integration': true,
      protocol: 'file:',
      slashes: true
    }));
}

ipc.on( 'getCustomCss', function (event, data) {
    // Second step : read and load CSS from the file
    BarOptions.retrieveCss( cssFile ).then( function( css ) {
        //mainWindow.webContents.send('cssInjection', css);
        event.sender.send( 'cssReply', css );
    }).catch( function( err ) {
        console.error( err );
    });
} );

function createWindow () {
    //var  {w, h} = electron.screen.getPrimaryDisplay().workAreaSize;
    
    var windowOptions =  {
        x: 0,
        y: 0,
        width: 800, 
        height: barHeight,
        frame: false,
        title: windowTitle,
        transparent: !DEV,
        type: 'dock',
        show: false
    }

    mainWindow = new BrowserWindow( windowOptions );

    // Emitted when the window is closed.
    mainWindow.on('closed', () => {
      mainWindow = null
    });

    positioner = new Positioner( mainWindow )
    var p = positioner.calculate( 'topLeft', 'trayRight') 
    mainWindow.setPosition( p.x, p.y )

    loadHTML()
    mainWindow.show()

    // Open the DevTools.
    if( DEBUG ) {
        mainWindow.webContents.openDevTools()
    }

    winProp.getWindowId( windowTitle ).then( function( wid ) {
        winProp.setStrutValues( wid, 0, 0, barHeight, 0, 0, 0, 0, 0, 0, 0, 0, 0 );
    } ).catch( function( err ) {
      console.log( err );
    });
}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on('ready', function() {
    createWindow()

    var rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout,
      terminal: false
    });

    rl.on('line', function(line){
        mainWindow.webContents.send('stdinAction', line);
    })

    rl.on('close', () => {
        app.quit()
    });

} );

// Quit when all windows are closed.
app.on('window-all-closed', () => {
  // On macOS it is common for applications and their menu bar
  // to stay active until the user quits explicitly with Cmd + Q
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('activate', () => {
  // On macOS it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (mainWindow === null) {
    createWindow()
  }
})

