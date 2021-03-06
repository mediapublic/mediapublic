import HelpRequest from './model';
import Collection from 'shared/backbone/collection';

export default Collection.extend({
  initialize(models, attributes) {
    if (attributes && attributes.organization) {
      this.organization = attributes.organization;
    }
  },
  model: HelpRequest,
  url() {
    if (this.organization) {
      return '/help-requests?org_id=' + this.organization.get('id');
    } else {
      return '/help-requests';
    }
  }
});
