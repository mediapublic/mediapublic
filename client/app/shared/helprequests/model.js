import {Model} from 'backbone';

export default Model.extend({
  schema: {
    title: {
      type: 'Text',
      validators: ['required'],
    },
    description: {
      type: 'TextArea',
      validators: ['required'],
      help: 'Keep it short and descriptive.'
    },
    contact_email: {
      type: 'Text',
      title: 'Contact Email',
      validators: ['email', 'required']
    }
  },

  permalink() {
    return '/help-requests/' + this.get('id');
  },

  urlRoot() {
    return '/help-requests';
  }
});
