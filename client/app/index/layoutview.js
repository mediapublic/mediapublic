import {LayoutView} from 'backbone.marionette';
import SearchView from 'shared/search/searchview';
import template from './layouttemplate.jade';

export default LayoutView.extend({
  initialize(options) {
    this.searchView = new SearchView();
  },
  template,
  regions: {
    search: '.homepage-search'
  },
  onBeforeShow() {
    this.showChildView('search', this.searchView);
  }
});
