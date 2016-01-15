import ItemView from 'shared/views/itemview';
import template from './singletemplate.jade';

export default ItemView.extend({
  template,
  className: 'person-container user-tile',
  serializeData() {
    let data = ItemView.prototype.serializeData.apply(this, arguments);
    data.viewState.needsApproval = this.model.needsApproval() &&
        (app.currentUser.isOrgAdmin(this.model.get('organization_id'))
            || app.currentUser.isAdmin());
    return data;
  },
  events: {
    'click .approve': function(event) {
      this.model.set('org_approved', true);
      this.model.save().then(() => {
        this.render();
      });
      event.stopImmediatePropagation();
      event.stopPropagation();
      event.preventDefault();
    },

    'click .reject': function(event) {
      this.model.set('organization_id', '');
      this.model.save().then(() => {
        this.model.collection.fetch();
      });
      event.stopImmediatePropagation();
      event.stopPropagation();
      event.preventDefault();
    }
  },
});
