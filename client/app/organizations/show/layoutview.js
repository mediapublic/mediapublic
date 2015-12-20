import {LayoutView} from 'backbone.marionette';
import OrganizationView from './view';
import PeopleView from 'shared/people/collectionview';
import template from './layouttemplate.jade';

export default LayoutView.extend({
  initialize(options) {
    this.peopleCollection = options.people;
  },
  template,
  regions: {
    organization: '.organization-container',
    people: '.people-container',
    recordings: '.recordings-container'
  },

  onBeforeShow() {
    this.showChildView(
        'organization', new OrganizationView({ model: this.model }));
    this.showChildView('people', new PeopleView({ collection: this.peopleCollection }));
  },
});
