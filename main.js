let DEBUG = process.env.DEBUG
let DEV = process.env.DEV

const {app, BrowserWindow, protocol} = require('electron')
const path = require('path')
const url = require('url')
const readline = require('readline');
const randomstring = require("randomstring");
const fs = require( 'fs' );

if( DEV ) {
    var client = require('electron-connect').client;
}

// parse cli parameter
var cliArgs = require( './js/cli-arguments.js' )
cliArgs.init( process.argv )
global.cliArgs = cliArgs

var debugmode = false
if( '1' == cliArgs.params.debugmode ) {
    debugmode = true
}

function debug( str ) {
    if( debugmode ) {
        console.log( str );
    }
}

// Keep a global reference of the window object, if you don't, the window will
// be closed automatically when the JavaScript object is garbage collected.
let mainWindow

let windowTitle = 'electronbar' + randomstring.generate( {
    length: 12,
    charset: 'alphabetic'
} );

function createWindow () {
  // Create the browser window.
  //var  {w, h} = electron.screen.getPrimaryDisplay().workAreaSize;

    const winPosition = require('./js/window-position')
    winPosition.setDebug( debugmode )

    console.log('window creation...');

    mainWindow = new BrowserWindow({
        x: 0,
        y: 0,
        height: 30,
        frame: false,
        toolbar: false,
        title: windowTitle,
        transparent: true,
        type: 'dock',
        show: false,
        'web-preferences': {
            'direct-write': true,
            'subpixel-font-scaling': true
        }
    });

    var barPosition = cliArgs.params.position || 'top';
    var screenNumber = cliArgs.params.screen || 1;
    winPosition.computeWinProperties( mainWindow, barPosition, screenNumber ).then( function() {
        var pageUrl = url.format({
          pathname: path.join(__dirname, 'index.html'),
          'node-integration': true,
          protocol: 'file:',
          slashes: true
        });
        console.log( 'Load url ' + pageUrl + '...');
        // and load the index.html of the app.
        mainWindow.loadURL( pageUrl );

        mainWindow.show()

        // Open the DevTools.
        //if( '1' == cliArgs.params.debugmode ) {
        if( debugmode ) {
            console.log("open the chrome console")
            mainWindow.webContents.openDevTools({mode:"detach"})
        }
    });


    // Emitted when the window is closed.
    mainWindow.on('closed', () => {
      // Dereference the window object, usually you would store windows
      // in an array if your app supports multi windows, this is the time
      // when you should delete the corresponding element.
      mainWindow = null
    });
}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.disableHardwareAcceleration()
app.on('ready', function() {
    console.log( 'Initializing application...');
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

    protocol.unregisterProtocol('', () => {
        createWindow()
    })
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

