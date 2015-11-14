import {Model} from 'backbone';

export default Model.extend({
  schema: {
    short_name: 'Text',
    phone: 'Text',
    primary_website: 'Text',
    long_description: 'TextArea',
    address_0: 'Text',
    address_1: 'Text',
    city: 'Text',
    zipcode: 'Text',
    state: 'Text'
  },

  urlRoot() {
    return app.config.apiUrl + '/organizations';
  }
});
