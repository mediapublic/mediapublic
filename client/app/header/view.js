import {ItemView} from 'backbone.marionette';
import template from './template.jade';

export default ItemView.extend({
  template,
  className: 'header navbar navbar-default navbar-fixed-top',

  attributes: {
    role: 'navigation'
  },

  templateHelpers: function() {
    return {
      menuItems: this.menuItems
    }
  },

  menuItems: {
    'home': '#',
    'organizations': '#organizations',
  }
});
