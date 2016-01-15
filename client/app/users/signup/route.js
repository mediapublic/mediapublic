import Person from 'shared/people/person';
import {Route} from 'backbone-routing';

import View from '../show/view';

export default Route.extend({
  initialize(options = {}) {
    this.container = options.container;
  },

  render() {
    this.model = new Person(app.currentUser.attributes);
    app.currentUser.on('sync', () => {
      this.model.set(app.currentUser.attributes);
      this.view.updatePermissions();
    });
    this.view = new View({
      model: this.model,
      editing: true,
      flashSuccess: 'Thanks for signing up! Please complete your profile.'
    });
    this.container.show(this.view);
  }
});
