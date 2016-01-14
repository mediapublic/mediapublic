import {ItemView} from 'backbone.marionette';
import template from './orglist.jade';
import _ from 'underscore';

export default ItemView.extend({
  className: 'view-container index',
  template,
  serializeData() {
    var data = ItemView.prototype.serializeData.apply(this, arguments);
    data.groups = _.groupBy(data.items, 'state');
    return data;
  }
});
