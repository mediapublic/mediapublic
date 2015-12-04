// This is the model, it should specify a schema--so the model can be edited--
// and a urlRoot--so the model can be saved.
import {Model} from 'backbone';

export default Model.extend({
  schema: {
    short_name: {
      type: 'Text',
      title: 'Short Name',
      validators: ['required']
    },
    phone: {
      type: 'Text',
      validators: ['phone']
    },
    primary_website: {
      type: 'Text',
      validators: ['url'],
      title: 'Website'
    },
    long_description: {
      type: 'TextArea',
      title: 'Long Description',
      validators: ['required']
    },
    address_0: {
      type: 'Text',
      validators: ['required'],
      title: 'Address line 1'
    },
    address_1: {
      type: 'Text',
      title: 'Address line 2',
    },
    city: {
      type: 'Text',
      validators: ['required']
    },
    zipcode: {
      type: 'Text',
      validators: ['required', 'zip']
    },
    state: {
      type: 'Text',
      validators: ['required', 'state']
    }
  },

  urlRoot() {
    return '/organizations';
  }
});
