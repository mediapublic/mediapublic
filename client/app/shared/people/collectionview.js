import {CompositeView} from 'backbone.marionette';
import SingleView from './singleview';
import Person from './person';
import template from './collectiontemplate.jade'

export default CompositeView.extend({
  template,
  events: {
    'click .add': 'addPerson'
  },
  className: 'people',
  childView: SingleView,
  childViewContainer: '.people-list',
  addPerson() {
    this.collection.add(new Person({ organization_id: this.collection.organization.get('id') }));
  }
});
