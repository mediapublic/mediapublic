import {Route} from 'backbone-routing';
import View from './layoutview';
import storage from 'shared/organizations/storage';
import People from 'shared/people/collection';
import Recordings from 'shared/recordings/collection';
import HelpRequests from 'shared/helprequests/collection';
import Howtos from 'shared/howtos/collection';
import _ from 'underscore';
import faker from 'shared/utilities/faker';

var fakePeople = faker.replicate(faker.fakePerson, 25);
var fakeRecordings = faker.replicate(faker.fakeRecording, 13);
var fakeRequests = faker.replicate(faker.fakeHelpRequest, 3);

export default Route.extend({
  initialize(options = {}) {
    this.container = options.container;
  },

  fetch(id) {
    return storage.find(id).then(model => {
      this.model = model;
      this.people = new People(fakePeople, {organization: this.model});
      this.people.fetch();
      this.recordings =
          new Recordings(fakeRecordings, {organization: this.model});
      this.recordings.fetch();
      this.helpRequests =
          new HelpRequests(fakeRequests, {organization: this.model});
      this.helpRequests.fetch();
      this.howtos = new Howtos([], {organization: this.model});
      this.howtos.fetch();
    });
  },

  render() {
    this.view = new View({
      model: this.model,
      people: this.people,
      recordings: this.recordings,
      helpRequests: this.helpRequests,
      howtos: this.howtos
    });
    this.container.show(this.view);
  }
});
