'use strict';

import path from 'path';
import gulp from 'gulp';
import { plugins, args, config, taskTarget, browserSync } from '../utils';

let dirs = config.directories;

// Watch task
gulp.task('watch', (done) => {
  if (!args.production) {
    // Styles
    gulp.watch([
      path.join(dirs.source, dirs.styles) + '/**/*.{scss,sass}',
      path.join(dirs.source, dirs.modules) + '/**/*.{scss,sass}'
    ], gulp.series('sass'));

    // Nunjucks Templates
    gulp.watch([
      dirs.source + '/**/*.nunjucks',
      path.join(dirs.source, dirs.data) + '/**/*.{json,yaml,yml}'
    ], gulp.series('nunjucks'));
    

    // Copy
    gulp.watch([
      dirs.source + '**/*',
      '!' + dirs.source + '/{**/\_*,**/\_*/**}',
      '!' + dirs.source + '/**/*.nunjucks'
    ], gulp.series('copy'));

    // Images
    gulp.watch([
      path.join(dirs.source, dirs.images) + '/**/*.{jpg,jpeg,gif,svg,png}'
    ], gulp.series('imagemin'));

    // All other files
    gulp.watch([
      dirs.temporary + '/**/*',
      '!' + dirs.temporary + '/**/*.{css,map,html,js}'
    ]).on('change', browserSync.reload);
  }
  done();
});
