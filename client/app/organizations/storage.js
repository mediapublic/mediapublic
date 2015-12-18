import Storage from 'backbone.storage';
import Organization from 'shared/organizations/model';
import Organizations from 'shared/organizations/collection';

let OrganizationsStorage = Storage.extend({
  model: Organization,
  collection:  Organizations,
});

export default new OrganizationsStorage();
