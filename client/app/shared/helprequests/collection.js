import HelpRequest from './model';
import {Collection} from 'backbone';

export default Collection.extend({
  initialize(models, attributes) {
    this.organization = attributes.organization;
  },
  model: HelpRequest,
  url() {
    return '/helprequests?organization_id=' + this.organization.get('id');
  }
});
