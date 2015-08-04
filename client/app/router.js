import {Router} from 'backbone-routing';
import IndexRoute from './index/route';

export default Router.extend({
  initialize(options = {}) {
    this.container = options.container;
  },

  routes: {
    '': 'index'
  },

  index() {
    return new IndexRoute({
      container: this.container
    });
  }
});
