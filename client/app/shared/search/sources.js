import _ from 'underscore';
import {Bloodhound} from 'typeahead.js-browserify';

import config from '../../config.js';

var sharedOptions = {
  local: [],
  datumTokenizer: Bloodhound.tokenizers.whitespace,
  queryTokenizer: Bloodhound.tokenizers.whitespace,
  identify: (datum) => datum.id
};

var remote = function(source) {
  return {
    transform: (response) => response.data,
    url: config.apiUrl + '/' + source + '?q=query',
    prepare: function(query, settings) {
      settings.url = settings.url.replace('query', encodeURIComponent(query));
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
  remote: remote('users')
}));


sources.howtos = new Bloodhound(_.extend({}, sharedOptions, {
  remote: remote('howtos')
}));

sources.helprequests = new Bloodhound(_.extend({}, sharedOptions, {
  remote: remote('help-requests')
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
