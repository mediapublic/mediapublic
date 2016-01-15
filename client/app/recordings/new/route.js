import Model from 'shared/recordings/model';
import {Route} from 'backbone-routing';

import View from '../show/view';

export default Route.extend({
  initialize(options = {}) {
    this.container = options.container;
  },

  render() {
    this.view = new View({
      model: new Model({
        organization_id: app.currentUser.get('organization_id')
      }),
      editing: true
    });
    this.container.show(this.view);
  }
});
