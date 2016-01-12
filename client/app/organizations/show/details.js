import ItemView from 'shared/views/itemview';
import template from './detailstemplate.jade';
import _ from 'underscore';

export default ItemView.extend({
  initialize(options) {
    ItemView.prototype.initialize.apply(this, arguments);
    this.state.set('expanded', options.expanded || false);
  },

  events: _.extend({}, ItemView.prototype.events, {
    'click .read-more': function() {
      this.state.set('expanded', true);
    },
    'click .read-less': function() {
      this.state.set('expanded', false);
    }
  }),

  template,
  className: 'organization-details',
});
