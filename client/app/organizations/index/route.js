import {Route} from 'backbone-routing';
import View from './view';
import storage from 'shared/organizations/storage';

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
