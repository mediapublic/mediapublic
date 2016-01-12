import {ItemView} from 'backbone.marionette';
import User from 'shared/people/person';
import template from './loginout.jade';
import _ from 'underscore';

export default ItemView.extend({
  initialize(options) {
    this.model = app.currentUser;
    this.listenTo(this.model, 'change', this.render);
    _.bindAll(this, 'render');
    return ItemView.prototype.initialize.apply(this, arguments);
  },
  template: template,
  events: {
    'click .log-out': function() {
      app.currentUser.logout();
    }
  }
});
