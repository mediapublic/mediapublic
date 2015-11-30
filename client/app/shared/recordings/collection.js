import Recording from './model';
import {Collection} from 'backbone';

export default Collection.extend({
  initialize(models, attributes) {
    this.organization = attributes.organization;
  },
  model: Recording,
  url() {
    return '/recordings?organization_id=' + this.organization.get('id');
  }
});
