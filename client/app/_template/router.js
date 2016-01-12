// This is the router that hooks everything up! You'll need to import and
// instantiate this file in main.js for your route to be connected.
import {Router} from 'backbone-routing';
import IndexRoute from './index/route';
import ShowRoute from './show/route';
import NewRoute from './new/route';

export default Router.extend({
  initialize(options = {}) {
    this.container = options.container;
  },

  routes: {
    'your-resource': 'index',
    'your-resource/new': 'new',
    'your-resource/:id': 'show',
  },

  index() {
    return new IndexRoute({
      container: this.container
    });
  },

  show() {
    return new ShowRoute({
      container: this.container
    });
  },

  new() {
    return new NewRoute({
      container: this.container
    });
  }
});
