import Recording from './model';
import {Collection} from 'backbone';

export default Collection.extend({
  initialize(models, attributes) {
    if (attributes && attributes.organization) {
      this.organization = attributes.organization;
    }
  },
  model: Recording,
  parse: (data) => data.recordings,
  url() {
    if (this.organization) {
      return '/recordings?organization_id=' + this.organization.get('id');
    } else {
      return '/recordings';
    }
  }
});
