import {Collection} from 'backbone';
import Organization from './model';

export default Collection.extend({
  model: Organization,
  url: () => app.config.apiUrl + '/organizations',
  parse: (data) => data.organizations
});
