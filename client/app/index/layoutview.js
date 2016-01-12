import {LayoutView} from 'backbone.marionette';
import SearchView from 'shared/search/searchview';
import template from './layouttemplate.jade';
import Backbone from 'backbone';

export default LayoutView.extend({
  initialize(options) {
    this.searchView = new SearchView();
    this.listenTo(this.searchView, 'search:updated', this.handleSearch);
  },
  template,
  regions: {
    search: '.homepage-search'
  },
  onBeforeShow() {
    this.showChildView('search', this.searchView);
  },
  handleSearch(event) {
    var url = '#search?q=' + encodeURIComponent(event.query) + '&type=' + event.type;
    Backbone.history.navigate(url, { trigger: true });
  }
});
