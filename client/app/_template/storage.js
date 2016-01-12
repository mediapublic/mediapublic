// This is the storage for your resource. It's basically just a client-side
// caching layer.
import Storage from 'backbone.storage';
import YourResource from './model';
import YourResourceCollection from './collection';

let YourResourceStorage = Storage.extend({
  model: YourResource,
  collection:  YourResourceCollection,
});

export default new YourResourceStorage();
