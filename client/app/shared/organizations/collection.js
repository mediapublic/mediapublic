import Collection from 'shared/backbone/collection';
import Organization from './model';

export default Collection.extend({
  initialize(models, options) {
    options = options || {};
    this.count = options.count || 25;
  },
  model: Organization,
  url() {
    return '/organizations?count=' + this.count;
  }
});
