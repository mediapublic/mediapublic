// This is the route for creating a new resource.
import {Route} from 'backbone-routing';
import View from '../show/view';
import YourResource from '../model';

export default Route.extend({
  initialize(options = {}) {
    this.container = options.container;
  },

  render() {
    this.view = new View({
      model: new YourResource(),
      editing: true
    });
    this.container.show(this.view);
  }
});
