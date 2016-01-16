import Person from 'shared/people/person';
import {Route} from 'backbone-routing';

import View from '../show/view';

export default Route.extend({
  initialize(options = {}) {
    this.container = options.container;
  },

  render() {
    this.view = new View({
      model: new Person({
        organization_id: app.currentUser.get('organization_id'),
        org_approved: app.currentUser.get('is_org_admin')
      }),
      editing: true
    });
    this.container.show(this.view);
  }
});
