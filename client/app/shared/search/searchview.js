import {ItemView} from 'backbone.marionette';
import datasets from 'shared/search/datasets';
import {sources} from './sources';
import template from './searchtemplate.jade';
import util from 'shared/utilities';
import _ from 'underscore';

export default ItemView.extend({
  initialize(options) {
    if (options.availableDatasets) {
      this.availableDatasets = _.compact(_.map(options.availableDatasets, function(name) {
        if (!datasets[name]) {
          console.log('WARNING: no dataset named', name);
        }
        return datasets[name];
      }));
    } else {
      this.availableDatasets = _.values(datasets);
    }
    if (options.active) {
      this.active = this._getDataset(options.active);
    }
    this.initialQuery = options.query || '';
    this.placeholder = options.placeholder || '';
  },

  template,
  className: 'search-view',

  ui: {
    input: 'input[type=text]',
    filters: '.dropdown-menu li',
    filterName: '.active-filter-name',
    search: '.search'
  },

  events: {
    'click @ui.filters': 'handleFilterChosen',
    'keyup': 'handleKeyup',
    'click @ui.search': 'handleSearch'
  },

  onAttach() {
    this.ui.input.val(this.initialQuery);
    this.ui.input.attr('placeholder', this.placeholder);
    this.initializeTypeahead();
  },

  templateHelpers() {
    return {
      availableDatasets: this.availableDatasets
    }
  },

  initializeTypeahead() {
    var activeDatasets = this.active ? [this.active] : this.availableDatasets;
    var activeName = this.active ? this.active.name : 'All';
    this.ui.filterName.text(activeName);
    this.ui.input.typeahead({}, ...activeDatasets);
  },

  setActiveDataset(name) {
    this.active = this._getDataset(name);
    // Remove and re-render typeahead
    this.ui.input.typeahead('destroy');
    this.initializeTypeahead();
  },

  handleFilterChosen(event) {
    var filter = this.$(event.currentTarget).data('dataset');
    if (this.active && this.active.name == filter) {
      return;
    }
    this.setActiveDataset(filter);
  },

  handleKeyup(event) {
    if (event.keyCode == 13) {
      this.handleSearch(event);
    }
  },

  handleSearch(event) {
    var query = this.ui.input.val();
    var type = this._getActiveName();
    util.updateQueryParams({ q: query, type: type });
    this.trigger('search:updated', { query, type });
  },

  _getDataset(name) {
    var dataset = _.find(this.availableDatasets, function(ds) {
      return ds.name == name;
    });
    if (!dataset && name !== 'all') {
      console.log('WARNING: dataset with name', name, 'not available');
    }
    return dataset;
  },

  _getActiveName() {
    return this.active ? this.active.name : 'all';
  }
});
