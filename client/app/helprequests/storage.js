import Storage from 'backbone.storage';
import Model from 'shared/helprequests/model';
import Collection from 'shared/helprequests/collection';

let HelpRequestsStorage = Storage.extend({
  model: Model,
  collection:  Collection,
});

export default new HelpRequestsStorage();
