import Storage from 'backbone.storage';
import Model from 'shared/people/person';
import Collection from 'shared/people/collection';

let PeopleStorage = Storage.extend({
  model: Model,
  collection:  Collection,
});

export default new PeopleStorage();
