import _ from 'underscore';

import {sources} from './sources';

var datasets = {
  organizations: {
    name: 'organizations',
    source: sources.organizations,
    templates: {
      header: '<div class="suggestion-header">Organizations</div>',
      suggestion: _.template('<div class="suggestion"><%= short_name %></div>')
    },
    display: (suggestion) => suggestion.short_name,
    limit: 3
  },
  recordings: {
    name: 'recordings',
    source: sources.recordings,
    templates: {
      header: '<div class="suggestion-header">Recordings</div>',
      suggestion: _.template('<div class="suggestion"><%= title %></div>')
    },
    display: (suggestion) => suggestion.title,
    limit: 3
  },
  people: {
    name: 'people',
    source: sources.people,
    templates: {
      header: '<div class="suggestion-header">People</div>',
      suggestion: _.template('<div class="suggestion"><%= first + last %></div>')
    },
    display: (suggestion) => suggestion.first + ' ' + suggestion.last,
    limit: 3
  },
  howtos: {
    name: 'howtos',
    source: sources.howtos,
    templates: {
      header: '<div class="suggestion-header">Howtos</div>',
      suggestion: _.template('<div class="suggestion"><%= title %></div>')
    },
    display: (suggestion) => suggestion.title,
    limit: 3
  },
  helprequests: {
    name: 'helprequests',
    source: sources.helprequests,
    templates: {
      header: '<div class="suggestion-header">Help Requests</div>',
      suggestion: _.template('<div class="suggestion"><%= title %></div>')
    },
    display: (suggestion) => suggestion.title,
    limit: 3
  }
};

export default datasets;
