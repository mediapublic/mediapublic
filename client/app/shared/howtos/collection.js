import Howto from './model';
import Collection from 'shared/backbone/collection';

export default Collection.extend({
  initialize(models, attributes) {
    if (attributes && attributes.organization) {
      this.organization = attributes.organization;
    }
  },
  model: Howto,
  url() {
    if (this.organization) {
      return '/howtos?org_id=' + this.organization.get('id');
    } else {
      return '/howtos';
    }
  }
});
