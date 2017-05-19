'use strict';

var gulp = require('gulp');
var jasmine = require('gulp-jasmine');
var cliParams = require('./cli-params.json' )

var electron = require('electron-connect').server.create( 
    {
        stopOnClose: true
    }
);

electron.on( 'error', function( error ) {
    console.log( error );
});

var callback = function(electronProcState) {
  if (electronProcState == 'stopped') {
    process.exit();
  }
};

gulp.task('jasmine', function() {
    return gulp.src('./tests/**/*.js')
        .pipe( jasmine() );
});

gulp.task('reload', function() {
    electron.reload();
});

gulp.task('serve', function () {

    electron.start( cliParams, callback );

    // Restart browser process
    gulp.watch('main.js', electron.restart);

    // Reload renderer process
    gulp.watch(['./css/**/*.css'], electron.reload);
    gulp.watch(['js/**.js', 'tests/**.js'], ['jasmine'] );
    gulp.watch(['js/index.js', 'index.html'], ['reload'] );
});
