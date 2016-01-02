import {Route} from 'backbone-routing';
import View from '../show/view';
import Person from 'shared/people/person';

export default Route.extend({
  initialize(options = {}) {
    this.container = options.container;
  },

  render() {
    this.view = new View({
      // Fix this when people and users have been unified on the server
      model: new Person(app.currentUser.attributes),
      editing: true,
      flashSuccess: 'Thanks for signing up! Please complete your profile.'
    });
    this.container.show(this.view);
  }
});
