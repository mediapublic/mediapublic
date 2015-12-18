import {LayoutView} from 'backbone.marionette';
import SearchView from 'shared/search/searchview';
import HowtosView from 'shared/howtos/collectionview';
import PeopleView from 'shared/people/collectionview';
import RecordingsView from 'shared/recordings/collectionview';
import HelpRequestsView from 'shared/helprequests/collectionview';
import template from './layouttemplate.jade';

export default LayoutView.extend({
  initialize(options) {
    this.query = options.query;
    this.activeType = options.activeType || 'all';
    this.sections = options.sections;
    this.searchView = new SearchView({
      query: this.query,
      active: this.activeType
    });
    this.listenTo(this.searchView, 'search:updated', this.handleSearchUpdated);
  },
  template,
  regions: {
    search: '.search-container',
    organizations: '.organizations-container',
    howtos: '.howtos-container',
    people: '.people-container',
    recordings: '.recordings-container'
  },
  onBeforeShow() {
    this.showChildView('search', this.searchView);
    this.setCollections(this.collections);
  },

  setCollections(collections) {
    this.collections = collections;

    this._createOrEmptyRegionView('howtos', HowtosView);
    this._createOrEmptyRegionView('people', PeopleView);
    this._createOrEmptyRegionView('recordings', RecordingsView);
  },

  handleSearchUpdated(event) {
    this.setCollections(
        app.services.search.getCollectionsForQuery(event.query, event.type));
  },

  _createOrEmptyRegionView(region, collectionView) {
    if (this.collections[region]) {
      this.showChildView(region, new collectionView({ collection: this.collections[region] }));
    } else {
      this.getRegion(region).empty();
    }
  }

});
