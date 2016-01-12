import {Route} from 'backbone-routing';
import View from '../show/layoutview';
import Organization from 'shared/organizations/model';

export default Route.extend({
  initialize(options = {}) {
    this.container = options.container;
  },

  render() {
    this.view = new View({
      model: new Organization(),
      editing: true
    });
    this.container.show(this.view);
  }
});
