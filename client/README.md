# Media Public Web Client
This is the html/css/javascript that powers the mediapublic.io UI.

## Contributing
Make sure you have the following dependencies installed:
1. [Node](https://nodejs.org) (I recommend version 0.10.x, `node -v` to check what you have installed). You will also need NPM, which comes with Node.
2. [Compass](http://compass-style.org/install/). (Note: I think this will be removed soon, but for now it is necessary to compile the stylesheets).
3. [http-server](https://www.npmjs.com/package/http-server) or similar tool for serving static files.

To get the development workflow up and running follow these steps:
1. `git clone` the repository
2. `cd mediapublic-server/client`
3. Run `npm install`. This will install all of the dependencies.
4. Run `gulp watch`. This will start listening for changes to the javascript and sass files, dynamically recompiling them as necessary.
5. `http-server`. This will start a server on port 8080 that is serving the files in the `public` folder. You can now see the running client by visiting `localhost:8080`.

### Toolchain
- The application framework is [Marionette](http://marionettejs.com/) on top of [Backbone](http://backbonejs.org/docs/backbone.html).
- Automation is handled by [gulp](http://gulpjs.com/).
- Javascript builds are done through [browserify](http://browserify.org/).
- ES6 is converted to browser-friendly JS by [babel](https://babeljs.io/).
- Templates are written in [Jade](http://jade-lang.com/).
- Stylesheets are written in [Sass](http://sass-lang.com/).
- Base-styling is provided by [Bootstrap](https://github.com/twbs/bootstrap-sass).

### Application Structure
`/app` - everything that runs in the browser

`/app/main.js` - the script that buts up the application, initializes any necessary singletons, and starts the router.

`/app/router.js` - the router that defines the mapping between urls and views.

`/app/<resource_type>` - directory containing everything related to a given resource: views, templates, routes, models, stores, and styles.

`/app/<resource_type>/<route_name>` - directory containing everything related to a give _route_: the view, the template, the styles.
