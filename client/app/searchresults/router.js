import {Router} from 'backbone-routing';
import SearchRoute from './route';

export default Router.extend({
  initialize(options = {}) {
    this.container = options.container;
  },

  routes: {
    'search': 'search'
  },

  search() {
    return new SearchRoute({
      container: this.container
    });
  }
});
