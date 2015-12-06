import Storage from 'backbone.storage';
import Model from 'shared/recordings/model';
import Collection from 'shared/recordings/collection';

let RecordingsStorage = Storage.extend({
  model: Model,
  collection:  Collection,
});

export default new RecordingsStorage();
