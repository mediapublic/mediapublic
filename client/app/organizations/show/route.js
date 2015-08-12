import {Route} from 'backbone-routing';
import View from './view';

export default Route.extend({
  initialize(options = {}) {
    this.container = options.container;
  },

  fetch() {
    // Make sure the models are loaded
  },

  render() {
    this.view = new View();
    this.container.show(this.view);
  }
});
