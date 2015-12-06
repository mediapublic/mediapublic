import ItemView from 'shared/views/itemview';
import User from 'shared/people/person';
import template from './loginout.jade';

export default ItemView.extend({
  initialize(options) {
    this.model = new User();
    return ItemView.prototype.initialize.apply(this, arguments);
  },
  template: template,
  events: {}
});
