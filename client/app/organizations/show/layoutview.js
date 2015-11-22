import {LayoutView} from 'backbone.marionette';
import OrganizationView from './view';
import PeopleView from 'shared/people/collection';
import People from 'shared/people/people';
import Person from 'shared/people/person';
import template from './layouttemplate.jade';

export default LayoutView.extend({
  template,
  regions: {
    organization: '.organization-container',
    people: '.people-container',
    recordings: '.recordings-container'
  },

  onBeforeShow() {
    this.showChildView(
        'organization', new OrganizationView({ model: this.model }));
    this.showChildView('people', new PeopleView({
      collection: new People([ new Person() ], { organization: this.model })}));
  },
});
