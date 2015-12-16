import {ItemView} from 'backbone.marionette';
import datasets from 'shared/search/datasets';
import {sources} from './sources';
import template from './searchtemplate.jade';
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
    this.initializeTypeahead();
  },

  templateHelpers() {
    return {
      availableDatasets: this.availableDatasets
    }
  },

  initializeTypeahead() {
    var activeDatasets = this.active ? [this.active] : this.availableDatasets;
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
    this.ui.filterName.text(filter);
    this.setActiveDataset(filter);
  },

  handleKeyup(event) {
    if(event.keyCode == 13){
      this.handleSearch(event);
    }
  },

  handleSearch(event) {
    console.log(this.ui.input.val());
  },

  _getDataset(name) {
    var dataset = _.find(this.availableDatasets, function(ds) {
      return ds.name == name;
    });
    if (!dataset && name !== 'all') {
      console.log('WARNING: dataset with name', name, 'not available');
    }
    return dataset;
  }
});
