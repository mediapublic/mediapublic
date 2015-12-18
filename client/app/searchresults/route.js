import {Route} from 'backbone-routing';
import View from './layoutview';
import util from 'shared/utilities';
import _ from 'underscore';

export default Route.extend({
  initialize(options = {}) {
    this.container = options.container;
    this.sections = {};
    this.query = '';
  },

  fetch() {
    var self = this;
    var params = util.getQueryParams();
    if (params.q) {
      this.query = params.q;
    }
    if (params.type && params.type != 'all') {
      this.type = params.type;
      self.sections[this.type] = app.services.search.getCollection(this.type, this.query);
    } else {
      this.sections = app.services.search.getAllCollections(this.query);
    }
  },

  render() {
    this.view = new View({
      sections: this.sections,
      query: this.query,
      activeType: this.type
    });
    this.container.show(this.view);
  }
});
