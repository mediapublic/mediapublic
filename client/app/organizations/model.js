import {Model} from 'backbone';

export default Model.extend({
  urlRoot() {
    return app.config.apiUrl + '/organizations';
  }
});
