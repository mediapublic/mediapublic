var gulp = require('gulp');

var eslint = require('gulp-eslint');
var sass = require('gulp-sass');
var source = require('vinyl-source-stream');
var watchify = require('watchify');
var browserify = require('browserify');
var notify = require('gulp-notify');
var plumber = require('gulp-plumber');
var autoprefixer = require('gulp-autoprefixer');
var gulpUtil = require('gulp-util');
var rename = require('gulp-rename');
var minifyCss = require('gulp-minify-css');
var streamify = require('gulp-streamify');
var uglify = require('gulp-uglify');
var crypto = require('crypto');
var fs = require('fs');
var jade = require('gulp-jade');
var del = require('del');
var argv = require('yargs').argv;
var rsync = require('gulp-rsync');


var DEST = 'public/';
var APP = 'app/';
var PROD_JS = DEST + '/javascript/main.min.js';
var PROD_CSS = DEST + '/css/main.min.css';


// Monitor less and main jade template for changes
gulp.task('watch', ['styles', 'html', 'bundlejs'], function() {
  gulp.watch(APP + '**/*.scss', ['styles']);
  gulp.watch(APP + 'index.jade', ['html']);
});

gulp.task('deploy', ['build:production'], function() {
  if (!argv.server) {
    console.log('Usage: gulp deploy --server <server address> [--user <remote user>]');
    return;
  }

  return gulp.src(DEST + '/**')
    .pipe(rsync({
      root: DEST,
      destination: '/var/www/mediapublic/client/public',
      hostname: argv.server,
      username: argv.user || process.env.USER,
      port: 22,
      progress: true,
      incremental: true
    }));
});

gulp.task('build:production', ['styles:production', 'js:production'], function() {
  var jsChecksum = fileChecksum(PROD_JS);
  var cssChecksum = fileChecksum(PROD_CSS);
  var cacheBustedJsName = 'main-' + jsChecksum + '.min.js';
  var cacheBustedCssName = 'main-' + cssChecksum + '.min.css';

  gulp.src(PROD_JS)
    .pipe(rename(cacheBustedJsName))
    .pipe(gulp.dest(DEST + '/javascript/'));

  gulp.src(PROD_CSS)
    .pipe(rename(cacheBustedCssName))
    .pipe(gulp.dest(DEST + '/css/'));

  return compileHtml({
    mainJs: '/javascript/' + cacheBustedJsName,
    mainCss: '/css/' + cacheBustedCssName
  });
});

// Monitor js files and rebuild dependency trees on change
gulp.task('bundlejs', function() {
  // Set the env so that configuration code knows this is for development
  process.env.NODE_ENV = 'development';

  var bundler = watchify(browserify('./' + APP + 'main.js', watchify.args));

  function rebundle() {
    return bundler.bundle()
      .on('error', notify.onError('JS error: <%= error.message %>'))
      .pipe(source('main.js'))
      .pipe(gulp.dest(DEST + '/javascript/'))
      .on('end', function() {
        gulpUtil.log('build.js rebuilt');
      });
  }

  bundler.on('update', rebundle);

  return rebundle();
});

gulp.task('js:production', ['js:clean'], function() {
  // Set the env so that configuration code knows this is for production
  process.env.NODE_ENV = 'production';
  return browserify('./' + APP + 'main.js')
    .bundle()
    .pipe(source('main.min.js'))
    .pipe(streamify(uglify()))
    .pipe(gulp.dest(DEST + '/javascript/'))
    .on('error', notify.onError('JS error: <%= error.message %>'))
    .on('end', function() {
      gulpUtil.log('production js built');
    });
});

gulp.task('js:clean', function() {
  return del([DEST + 'javascript/main-*.min.js']);
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

gulp.task('styles:production', ['css:clean'], function() {
  return gulp.src(APP + 'main.scss')
    .pipe(plumber())
    .pipe(sass({
      includePaths: ['node_modules/']
    }).on('error', sass.logError))
    .pipe(autoprefixer())
    .pipe(rename('main.min.css'))
    .pipe(minifyCss())
    .pipe(gulp.dest(DEST + 'css/'))
    .on('error', notify.onError('Styles error: <%= error.message %>'))
    .on('end', function() {
      gulpUtil.log('production css built');
    });
});

gulp.task('css:clean', function() {
  return del([DEST + 'css/main-*.min.css']);
});

gulp.task('html', function() {
  return compileHtml({
    mainJs: '/javascript/main.js',
    mainCss: '/css/main.css'
  });
});

function compileHtml(locals) {
  return gulp.src(APP + 'index.jade')
    .pipe(jade({
      pretty: true,
      locals: locals
    }))
    .pipe(gulp.dest(DEST))
    .on('error', notify.onError('HTML error: <%= error.message %>'));
}

// Lint all the javascript
gulp.task('lint', function() {
  return gulp.src(['./app/**/*.js', 'gulpfile.js'])
    .pipe(eslint())
    .pipe(eslint.format())
    .pipe(eslint.failAfterError());
});

function checksum(str) {
  return crypto
    .createHash('md5')
    .update(str, 'utf8')
    .digest('hex');
}

function fileChecksum(filename) {
  return checksum(fs.readFileSync(filename));
}
