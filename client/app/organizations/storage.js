import Storage from 'backbone.storage';
import Organization from './model';
import Organizations from './collection';

let OrganizationsStorage = Storage.extend({
  model: Organization,
  collection:  Organizations,
});

export default new OrganizationsStorage();
