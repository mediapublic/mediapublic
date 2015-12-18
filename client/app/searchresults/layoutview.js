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
    this.showChildView('howtos', new HowtosView({ collection: this.sections.howtos }));
    this.showChildView('people', new PeopleView({ collection: this.sections.people }));
    this.showChildView('recordings', new RecordingsView({ collection: this.sections.recordings }));
  }
});
