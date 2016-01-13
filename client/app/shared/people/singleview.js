import ItemView from 'shared/views/itemview';
import template from './singletemplate.jade';

export default ItemView.extend({
  template,
  className: 'person-container user-tile',
  render() {
    ItemView.prototype.render.apply(this, arguments);
    console.log(this.model.attributes);
    return this;
  }
});
