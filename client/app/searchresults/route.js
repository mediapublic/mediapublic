import {Route} from 'backbone-routing';
import View from './layoutview';
import util from 'shared/utilities';
import _ from 'underscore';

export default Route.extend({
  initialize(options = {}) {
    this.container = options.container;
    this.collections = {};
    this.query = '';
  },

  fetch() {
    var self = this;
    var params = util.getQueryParams();
    this.type = params.type || 'all';
    this.query = params.q || '';
    this.collections = app.services.search.getCollectionsForQuery(this.query, this.type);
  },

  render() {
    this.view = new View({
      collections: this.collections,
      query: this.query,
      activeType: this.type
    });
    this.container.show(this.view);
  }
});
