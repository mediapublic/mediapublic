// This is the collection for your resource--it should specify the model and the
// url.
import {Collection} from 'backbone';
import Organization from './model';

export default Collection.extend({
  model: Organization,
  url: () => '/organizations'
});
