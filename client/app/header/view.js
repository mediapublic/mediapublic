import {LayoutView} from 'backbone.marionette';
import LogInOutView from './loginoutview';
import template from './template.jade';

export default LayoutView.extend({
  initialize(options) {
    this.logInOutView = new LogInOutView();
    return LayoutView.prototype.initialize.apply(this, arguments);
  },
  template,
  className: 'header navbar navbar-default navbar-fixed-top',

  attributes: {
    role: 'navigation'
  },

  templateHelpers: function() {
    return {
      menuItems: this.menuItems
    };
  },

  menuItems: {
    'home': '#',
    'organizations': '#organizations',
  },

  regions: {
    logInOut: '.log-in-out'
  },

  onBeforeShow() {
    this.showChildView('logInOut', this.logInOutView);
  }
});
