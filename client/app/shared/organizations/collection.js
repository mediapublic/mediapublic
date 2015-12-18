import Collection from 'shared/backbone/collection';
import Organization from './model';

export default Collection.extend({
  model: Organization,
  url: () => '/organizations',
});
