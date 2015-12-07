// This is the collection for your resource--it should specify the model and the
// url.
import Collection from 'shared/backbone/collection';
import Organization from './model';

export default Collection.extend({
  model: Organization,
  url: () => '/organizations'
});
