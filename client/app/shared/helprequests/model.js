import {Model} from 'backbone';

export default Model.extend({
  schema: {
    title: {
      type: 'Text',
      validators: ['required'],
    },
    text: {
      type: 'Text',
      validators: ['required'],
    },
    contact_email: {
      type: 'Text',
      title: 'Contact Email',
      validators: ['email', 'required']
    }
  },

  urlRoot() {
    return '/recordings';
  }
});
