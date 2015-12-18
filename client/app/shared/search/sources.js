import {Bloodhound} from 'typeahead.js-browserify';
import config from '../../config.js';
import _ from 'underscore';

var sharedOptions = {
  local: [],
  datumTokenizer: Bloodhound.tokenizers.whitespace,
  queryTokenizer: Bloodhound.tokenizers.whitespace,
  identify: (datum) => datum.id
};

var remote = function(source) {
  return {
    wildcard: 'query',
    transform: (response) => response.data,
    url: config.apiUrl + '/' + source + '?q=query',
    prepare: function(query, settings) {
      var originalSuccess = settings.success;
      settings.success = function(response) {
        app.services.search.cache(source, query, response.data);
        if (originalSuccess) {
          return originalSuccess.apply(this, arguments);
        }
      };
      return settings;
    }
  };
};

var sources = {};

sources.organizations = new Bloodhound(_.extend({}, sharedOptions, {
  remote: remote('organizations')
}));


sources.recordings = new Bloodhound(_.extend({}, sharedOptions, {
  remote: remote('recordings')
}));


sources.people = new Bloodhound(_.extend({}, sharedOptions, {
  remote: remote('/people')
}));


sources.howtos = new Bloodhound(_.extend({}, sharedOptions, {
  remote: remote('howtos')
}));


var getSources = function(names) {
  return _.compact(_.map(names, function(name) {
    if (!sources[name]) {
      console.log('WARNING: Source', name, 'not found.');
    }
    return sources[name];
  }));
};


export default {
  sources,
  getSources
};
