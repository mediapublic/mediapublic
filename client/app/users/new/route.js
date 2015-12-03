import {Route} from 'backbone-routing';
import View from '../show/view';
import Person from 'shared/people/person';

export default Route.extend({
  initialize(options = {}) {
    this.container = options.container;
  },

  render() {
    this.view = new View({
      model: new Person(),
      editing: true
    });
    this.container.show(this.view);
  }
});
