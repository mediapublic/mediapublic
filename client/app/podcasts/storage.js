import Storage from 'backbone.storage';
import Model from 'shared/podcasts/model';
import Collection from 'shared/podcasts/collection';

let PodcastsStorage = Storage.extend({
  model: Model,
  collection:  Collection,
});

export default new PodcastsStorage();
