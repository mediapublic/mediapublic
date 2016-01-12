import ItemView from 'shared/views/itemview';
import template from './bannertemplate.jade';

export default ItemView.extend({
  initialize(options) {
    this.listenTo(this.model, 'editing:cancel editing:done', this.render);
    return ItemView.prototype.initialize.apply(this, arguments);
  },
  template,
  className: 'organization-banner',
});
