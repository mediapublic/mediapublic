import Organizations from 'shared/organizations/collection';
import {Route} from 'backbone-routing';

import View from './view';

export default Route.extend({
  initialize(options = {}) {
    this.container = options.container;
  },

  fetch() {
    this.collection = new Organizations([], {count: 10000});
    return this.collection.fetch();
  },

  render() {
    this.view = new View({
      collection: this.collection
    });
    this.container.show(this.view);
  }
});
