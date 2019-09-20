# Fit On A Floppy readme

Generated on 2019-09-19 using
[generator-yeogurt@3.0.1](https://github.com/larsonjj/generator-yeogurt)

## Description

This is an example readme file.
Describe your site/app here.

## Technologies used

JavaScript

- [Browserify](http://browserify.org/)with ES6/2015 support through [Babel](https://babeljs.io/)
- [Node](https://nodejs.org/)

Testing

- [Karma](http://karma-runner.github.io/4.0/index.html)
- [Jasmine](http://jasmine.github.io/)

Styles

- [Sass](http://sass-lang.com/) via ([node-sass](https://github.com/sass/node-sass))

Markup
- [Nunjucks](https://mozilla.github.io/nunjucks/)

Optimization

- [Imagemin](https://github.com/imagemin/imagemin)
- [Uglify](https://github.com/mishoo/UglifyJS)

Server

- [BrowserSync](http://www.browsersync.io/)

Linting

- [ESlint](http://eslint.org/)

Automation

- [Gulp](http://gulpjs.com)

Code Management

- [Editorconfig](http://editorconfig.org/)
- [Git](https://git-scm.com/)

## Automated tasks

This project uses [Gulp](http://gulpjs.com) and npm scripts (i.e. `npm run...`) to run automated tasks for development and production builds.
The tasks are as follows:

`npm run build`: Build a production version of your site/app

`npm run serve`: Compiles preprocessors and boots up development server
`npm run serve -- --open`: Same as `npm run serve` but will also open up site/app in your default browser
`npm run serve:prod`: Same as `npm run serve` but will run all production tasks so you can view the site/app in it's final optimized form

`npm test`: Lints all `*.js` file in the `source` folder using eslint and runs all `*.test.js` file unit tests through [Karma](http://karma-runner.github.io/0.13/index.html) and Jasmine
`npm test -- --watch`: Same as `npm test` but will constantly watch `*.test.js` files and rerun tests when changes are detected

**_Adding the `-- --debug` option to any npm script command to display extra debugging information (ex. data being loaded into your templates)_**
