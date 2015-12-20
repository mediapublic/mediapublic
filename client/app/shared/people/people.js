import Person from './person';
import {Collection} from 'backbone';

export default Collection.extend({
  initialize(models, attributes) {
    this.organization = attributes.organization;
  },
  model: Person,
  url() {
    return '/people?organization_id=' + this.organization.get('id');
  }
});
