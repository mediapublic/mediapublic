import ItemView from 'shared/itemview';
import template from './template.jade';

export default ItemView.extend({
  template,
  className: 'organization',

  events: {
    'click .edit': 'renderEditor',
    'click .save': 'saveChanges'
  },
});
