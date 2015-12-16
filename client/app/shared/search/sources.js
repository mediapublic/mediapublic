import {Bloodhound} from 'typeahead.js-browserify';
import config from '../../config.js';
import _ from 'underscore';

var sharedOptions = {
  local: [],
  datumTokenizer: Bloodhound.tokenizers.whitespace,
  queryTokenizer: Bloodhound.tokenizers.whitespace,
  identify: (datum) => datum.id
};

var remote = {
  wildcard: 'query',
  transform: (response) => response.data
};

var sources = {};

sources.organizations = new Bloodhound(_.extend({}, sharedOptions, {
  remote: _.extend({}, remote, {
    url: config.apiUrl + '/organizations?q=query'
  })
}));


sources.recordings = new Bloodhound(_.extend({}, sharedOptions, {
  remote: _.extend({}, remote, {
    url: config.apiUrl + '/recordings?q=query'
  })
}));


sources.people = new Bloodhound(_.extend({}, sharedOptions, {
  remote: _.extend({}, remote, {
    url: config.apiUrl + '/people?q=query'
  })
}));


sources.howtos = new Bloodhound(_.extend({}, sharedOptions, {
  remote: _.extend({}, remote, {
    url: config.apiUrl + '/howtos?q=query'
  })
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
