// This is the route for the index page. It should load the list of resources
// from the API in `fetch`, and instantiate + show the view in `render`

import {Route} from 'backbone-routing';
import View from './view';
import storage from '../storage';

export default Route.extend({
  initialize(options = {}) {
    this.container = options.container;
  },

  fetch() {
    return storage.findAll().then(collection => {
      this.collection = collection;
    });
  },

  render() {
    this.view = new View({
      collection: this.collection
    });
    this.container.show(this.view);
  }
});
