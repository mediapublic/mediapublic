import {Collection} from 'backbone';
import Organization from './model';

export default Collection.extend({
  model: Organization,
  url: () => '/organizations',
  parse: (data) => data.organizations
});
