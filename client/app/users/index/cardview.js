import {ItemView} from 'backbone.marionette';
import template from './cardtemplate.jade';

export default ItemView.extend({
  template,
  className: 'organization-card'
});
