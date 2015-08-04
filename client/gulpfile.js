var gulp = require('gulp');

var jshint = require('gulp-jshint');
var sass = require('gulp-sass');
var source = require('vinyl-source-stream');
var watchify = require('watchify');
var browserify = require('browserify');
var notify = require('gulp-notify');
var plumber = require('gulp-plumber');
var autoprefixer = require('gulp-autoprefixer');

var DEST = 'public/';
var APP = 'app/';


// Monitor js files and rebuild dependency trees on change
gulp.task('bundlejs', function() {
  var bundler = watchify(browserify('./' + APP + 'main.js', watchify.args));

  function rebundle() {
    return bundler.bundle()
      .on('error', notify.onError('JS error: <%= error.message %>'))
      .pipe(source('build.js'))
      .pipe(gulp.dest(DEST + '/javascript/'));
  }


  bundler.on('update', rebundle);

  return rebundle();
});

// Monitor less and main jade template for changes
gulp.task('watch', ['bundlejs'], function() {

  gulp.watch(APP + '**/*.scss', ['styles']);
});

// Watch sass files for changes and compile to css
gulp.task('styles', function() {
  gulp.src(APP + 'main.scss')
    .pipe(plumber())
    .pipe(sass({
      includePaths: ['node_modules/']
    }).on('error', sass.logError))
    .pipe(autoprefixer())
    .pipe(gulp.dest(DEST + 'css/'))
    .on('error', notify.onError('Styles error: <%= error.message %>'));
});

// Lint all the javascript
gulp.task('lint', function() {
  gulp.src(['./app/**/*.js', 'gulpfile.js'])
    .pipe(jshint())
    .pipe(jshint.reporter('default', { verbose: true }));
});
