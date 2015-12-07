import {Route} from 'backbone-routing';
import View from '../show/view';
import Person from 'shared/people/person';

export default Route.extend({
  initialize(options = {}) {
    this.container = options.container;
  },

  render() {
    this.view = new View({
      model: app.currentUser,
      editing: true,
      flashSuccess: 'Thanks for signing up! Please complete your profile.'
    });
    this.container.show(this.view);
  }
});
