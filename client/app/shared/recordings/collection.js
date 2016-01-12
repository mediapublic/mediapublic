import Recording from './model';
import Collection from 'shared/backbone/collection';

export default Collection.extend({
  initialize(models, attributes) {
    if (attributes && attributes.organization) {
      this.organization = attributes.organization;
    }
  },
  model: Recording,
  url() {
    if (this.organization) {
      return '/recordings?organization_id=' + this.organization.get('id');
    } else {
      return '/recordings';
    }
  }
});
