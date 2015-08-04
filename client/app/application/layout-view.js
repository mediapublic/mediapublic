import {LayoutView} from 'backbone.marionette';
import template from './layout.jade';

export default LayoutView.extend({
  el: '.application',
  template,

  regions: {
    header: '.app-header',
    notifications: '.app-notifications',
    content: '.app-content',
    footer: '.app-footer',
    overlay: '.app-overlay'
  }
});
