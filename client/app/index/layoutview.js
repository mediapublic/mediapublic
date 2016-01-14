import {LayoutView} from 'backbone.marionette';
import SearchView from 'shared/search/searchview';
import HomepageTiles from './homepagetiles';
import template from './layouttemplate.jade';
import Backbone from 'backbone';

export default LayoutView.extend({
  initialize(options) {
    this.searchView = new SearchView({placeholder: 'Search for your local station...'});
    this.tilesView = new HomepageTiles({collection: this.collection});
    this.listenTo(this.searchView, 'search:updated', this.handleSearch);
  },
  template,
  regions: {
    search: '.homepage-search',
    tiles: '.homepage-tiles'
  },
  onBeforeShow() {
    this.showChildView('search', this.searchView);
    this.showChildView('tiles', this.tilesView);
  },
  handleSearch(event) {
    var url = '#search?q=' + encodeURIComponent(event.query) + '&type=' + event.type;
    Backbone.history.navigate(url, {trigger: true});
  }
});
