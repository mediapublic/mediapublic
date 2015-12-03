import {Model} from 'backbone';

export default Model.extend({
  schema: {
    first: {
      type: 'Text',
      title: 'First Name',
      validators: ['required'],
    },
    last: {
      type: 'Text',
      title: 'Last Name',
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
    address_0: {
      type: 'Text',
      title: 'Address line 1'
    },
    address_1: {
      type: 'Text',
      title: 'Address line 2',
    },
    city: {
      type: 'Text',
    },
    zipcode: {
      type: 'Text',
      validators: ['zip']
    },
    state: {
      type: 'Text',
      validators: ['state']
    },
    twitter: 'Text',
    facebook: 'Text',
    instagram: 'Text',
    periscope: 'Text'
  },

  urlRoot() {
    return '/people';
  }
});
