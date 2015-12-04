import {LayoutView} from 'backbone.marionette';
import OrganizationBanner from './banner';
import OrganizationDetails from './details';
import PeopleView from 'shared/people/collectionview';
import RecordingsView from 'shared/recordings/collectionview';
import HelpRequestsView from 'shared/helprequests/collectionview';
import template from './layouttemplate.jade';

export default LayoutView.extend({
  initialize(options) {
    this.peopleCollection = options.people;
    this.recordingsCollection = options.recordings;
    this.helpRequestsCollection = options.helpRequests;
  },
  template,
  regions: {
    banner: '.organization-banner-container',
    details: '.organization-details-container',
    people: '.people-container',
    recordings: '.recordings-container',
    helprequests: '.help-requests-container'
  },

  onBeforeShow() {
    this.showChildView(
        'banner', new OrganizationBanner({ model: this.model }));
    this.showChildView(
        'details', new OrganizationDetails({ model: this.model }));
    this.showChildView(
        'people', new PeopleView({ collection: this.peopleCollection }));
    this.showChildView(
        'recordings',
        new RecordingsView({ collection: this.recordingsCollection }));
    this.showChildView(
        'helprequests',
        new HelpRequestsView({ collection: this.helpRequestsCollection}));
  },
});
