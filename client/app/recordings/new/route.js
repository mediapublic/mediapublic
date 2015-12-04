import {Route} from 'backbone-routing';
import View from '../show/view';
import Model from 'shared/recordings/model';

export default Route.extend({
  initialize(options = {}) {
    this.container = options.container;
  },

  render() {
    this.view = new View({
      model: new Model(),
      editing: true
    });
    this.container.show(this.view);
  }
});
