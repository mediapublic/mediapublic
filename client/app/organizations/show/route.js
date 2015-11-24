import {Route} from 'backbone-routing';
import View from './layoutview';
import storage from '../storage';
import People from 'shared/people/people';

export default Route.extend({
  initialize(options = {}) {
    this.container = options.container;
  },

  fetch(id) {
    return storage.find(id).then(model => {
      this.model = model;
      this.people = new People([], { organization: this.model });
      this.people.fetch();
    });
  },

  render() {
    this.view = new View({
      model: this.model,
      people: this.people
    });
    this.container.show(this.view);
  }
});
