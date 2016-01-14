import {LayoutView} from 'backbone.marionette';
import SearchView from 'shared/search/searchview';
import HowtosView from 'shared/howtos/collectionview';
import PeopleView from 'shared/people/collectionview';
import RecordingsView from 'shared/recordings/collectionview';
import HelpRequestsView from 'shared/helprequests/collectionview';
import OrganizationsView from 'shared/organizations/collectionview';
import template from './layouttemplate.jade';

export default LayoutView.extend({
  initialize(options) {
    this.query = options.query;
    this.activeType = options.activeType || 'all';
    this.collections = options.collections;
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
    this._createOrEmptyRegionView('organizations', OrganizationsView);
  },

  handleSearchUpdated(event) {
    this.setCollections(
        app.services.search.getCollectionsForQuery(event.query, event.type));
  },

  // There are a ton of possible optimizations around this functionality, but
  // I'm deferring them all for now.
  _createOrEmptyRegionView(region, collectionView) {
    if (!this.collections[region]) {
      this.getRegion(region).empty();
      return;
    }

    this.showChildView(region, new collectionView({collection: this.collections[region]}));
  }

});
