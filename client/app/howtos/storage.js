import Storage from 'backbone.storage';
import Model from 'shared/howtos/model';
import Collection from 'shared/howtos/collection';

let RecordingsStorage = Storage.extend({
  model: Model,
  collection:  Collection,
});

export default new RecordingsStorage();
