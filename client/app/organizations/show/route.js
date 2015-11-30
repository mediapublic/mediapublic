import {Route} from 'backbone-routing';
import View from './layoutview';
import storage from '../storage';
import People from 'shared/people/people';
import Recordings from 'shared/recordings/collection';
import _ from 'underscore';
import faker from 'shared/utilities/faker';

var fakePeople = faker.replicate(faker.fakePerson, 25);
var fakeRecordings = faker.replicate(faker.fakeRecording, 13);

export default Route.extend({
  initialize(options = {}) {
    this.container = options.container;
  },

  fetch(id) {
    return storage.find(id).then(model => {
      this.model = model;
      this.people = new People(fakePeople, { organization: this.model });
      this.people.fetch();
      this.recordings = new Recordings(fakeRecordings, { organization: this.model });
      this.recordings.fetch();
    });
  },

  render() {
    this.view = new View({
      model: this.model,
      people: this.people,
      recordings: this.recordings
    });
    this.container.show(this.view);
  }
});
