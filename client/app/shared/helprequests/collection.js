import HelpRequest from './model';
import {Collection} from 'backbone';

export default Collection.extend({
  initialize(models, attributes) {
    if (attributes && attributes.organization) {
      this.organization = attributes.organization;
    }
  },
  model: HelpRequest,
  url() {
    if (this.organization) {
      return '/helprequests?organization_id=' + this.organization.get('id');
    } else {
      return '/helprequests';
    }
  }
});
