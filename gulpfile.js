'use strict';

var gulp = require('gulp');
var sass = require('gulp-sass');
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

gulp.task('sass', function () {
    return gulp.src('./sass/**/*.sass')
        .pipe(sass().on('error', sass.logError))
        .pipe(gulp.dest('./css'));
});

gulp.task('jasmine', function() {
    return gulp.src('./tests/**/*.js')
        .pipe( jasmine() );
});

gulp.task('reload', function() {
    electron.reload();
});

gulp.task('serve', function () {

    electron.start( cliParams, callback );

    gulp.watch('./sass/**/*.sass', ['sass']);

    // Restart browser process
    gulp.watch('main.js', function() { electron.restart( cliParams, callback ) } );

    // Reload renderer process
    gulp.watch(['./css/**/*.css'], electron.reload);
    gulp.watch(['js/**.js', 'tests/**.js'], ['jasmine'] );
    gulp.watch(['js/index.js', 'index.html'], ['reload'] );
});
