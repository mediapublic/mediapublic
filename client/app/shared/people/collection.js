import Person from './person';
import Collection from 'shared/backbone/collection';

export default Collection.extend({
  initialize(models, attributes) {
    if (attributes && attributes.organization) {
      this.organization = attributes.organization;
    }
  },
  model: Person,
  url() {
    if (this.organization) {
      return '/users?org_id=' + this.organization.get('id');
    } else {
      return '/users';
    }
  }
});
