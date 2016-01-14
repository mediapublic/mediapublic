/**
 * This is a service that caches search results as they are fetched for auto-
 * complete and provides the capability to turn cached results into collections.
 */

import _ from 'underscore';
import Cache from 'shared/utilities/cache';
import HelpRequests from 'shared/helprequests/collection';
import Howtos from 'shared/howtos/collection';
import Organizations from 'shared/organizations/collection';
import People from 'shared/people/collection';

function SearchService() {
  this._cache = new Cache();
}

var collections = {
  organizations: Organizations,
  people: People,
  howtos: Howtos,
  helprequests: HelpRequests
};


SearchService.prototype.start = function() {};


SearchService.prototype.cache = function(type, query, data) {
  this._cache.set(this._getCacheKey(type, query), data);
};


SearchService.prototype.getCollection = function(type, query) {
  var data = this._cache.get(this._getCacheKey(type, query));
  return this._createCollection(type, query, data);
};


SearchService.prototype.getAllCollections = function(query) {
  var self = this;
  return _.mapObject(collections, function(val, key) {
    return self.getCollection(key, query);
  });
};

SearchService.prototype.getCollectionsForQuery = function(query, type) {
  if (type.toLowerCase() === 'all') {
    return this.getAllCollections(query);
  }
  return _.object([[type, this.getCollection(type, query)]]);
};


SearchService.prototype._getCacheKey = function(type, query) {
  return type + '_' + query;
};


SearchService.prototype._createCollection = function(type, query, data) {
  if (!collections[type]) {
    throw new Error('Collection ' + type + ' missing from SearchService');
  }

  var SearchCollection = collections[type].extend({
    url() {
      var superUrl = collections[type].prototype.url.apply(this, arguments);
      return superUrl.indexOf('?') !== -1 ?
          superUrl + '&q=' + query :
          superUrl + '?q=' + query;
    }
  });

  var collection = new SearchCollection(data || []);
  if (!data) {
    collection.fetch();
  }

  return collection;
};

export default new SearchService();
