import HelpRequest from './model';
import {Collection} from 'backbone';

export default Collection.extend({
  initialize(models, attributes) {
    this.organization = attributes.organization;
  },
  model: HelpRequest,
  parse: (data) => data.helpRequests,
  url() {
    return '/helprequests?organization_id=' + this.organization.get('id');
  }
});
