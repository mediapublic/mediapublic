import {Route} from 'backbone-routing';
import View from './layoutview';
import HomepageData from './homepagedata';
import {Collection} from 'backbone';
import Recording from 'shared/recordings/model';
import Howto from 'shared/howtos/model';
import HelpRequest from 'shared/helprequests/model';
import Person from 'shared/people/person';
import Organization from 'shared/organizations/model';


const modelMap = {
  recording: Recording,
  howto: Howto,
  helprequest: HelpRequest,
  person: Person,
  organization: Organization
};


export default Route.extend({
  initialize(options = {}) {
    this.container = options.container;
  },

  fetch() {
    var models = HomepageData.map((data) => {
      let model = new modelMap[data.type](data);
      model.fetch();
      return model;
    });
    this.collection = new Collection(models);
  },

  render() {
    this.view = new View({
      collection: this.collection
    });
    this.container.show(this.view);
  }
});
