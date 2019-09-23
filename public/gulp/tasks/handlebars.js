var path = require('path');
var gulp = require('gulp');
var wrap = require('gulp-wrap');
var concat = require('gulp-concat');
var hb = require('handlebars');
var merge = require('merge-stream');
var handlebars = require('../../src/_templates/helpers.js')(hb);

import { config, taskTarget, browserSync } from '../utils';

let dirs = config.directories;
let entries = config.entries;

let dest = path.join(taskTarget, dirs.scripts.replace(/^_/, ''));

var gulp_handlebars = require('gulp-handlebars');
var wrap = require('gulp-wrap');
var declare = require('gulp-declare');
var concat = require('gulp-concat');
var uglify = require('gulp-uglify');
 
gulp.task('handlebars', function(){
  var partials = gulp.src(entries.handlebars, { cwd: path.join(dirs.source, dirs.templates, 'partials')})
    .pipe(gulp_handlebars({handlebars: handlebars}))
    .pipe(wrap('Handlebars.registerPartial(<%= processPartialName(file.relative) %>, Handlebars.template(<%= contents %>));', {}, {
      imports: {
        processPartialName: function(fileName) {
          // Strip the extension and the underscore
          // Escape the output with JSON.stringify
          return JSON.stringify(path.basename(fileName, '.js').substr(1));
        }
      }
    }));

  var templates = gulp.src(entries.handlebars, { cwd: path.join(dirs.source, dirs.templates)})
    .pipe(gulp_handlebars({handlebars: handlebars}))
    .pipe(wrap('Handlebars.template(<%= contents %>)'))
    .pipe(declare({
      namespace: 'foaf',
      noRedeclare: true, // Avoid duplicate declarations
    }));

    return merge(partials, templates)
      .pipe(concat('templates.js'))
      .pipe(uglify())
      .pipe(gulp.dest(dest))
      .pipe(browserSync.stream({ match: 'scripts/templates**.js' }));
});