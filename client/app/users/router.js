import {Router} from 'backbone-routing';
import IndexRoute from './index/route';
import ShowRoute from './show/route';
import NewRoute from './new/route';
import SignupRoute from './signup/route';

export default Router.extend({
  initialize(options = {}) {
    this.container = options.container;
  },

  routes: {
    'users': 'index',
    'users/new': 'new',
    'users/:id': 'show',
    'people': 'index',
    'people/new': 'new',
    'people/:id': 'show',
    'signup': 'signup',
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
  },

  signup() {
    return new SignupRoute({
      container: this.container
    });
  }
});
