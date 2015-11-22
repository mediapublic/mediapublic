// This is the individual view, it should inherit from 'shared/itemview'.
import ItemView from 'shared/itemview';
import template from './template.jade';

export default ItemView.extend({
  template,
  className: 'your-resource',
});
