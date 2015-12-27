import {Model} from 'backbone';

export default Model.extend({
  schema: {
    title: {
      type: 'Text',
      validators: ['required'],
    },
    description: 'TextArea',
    url: {
      type: 'Text',
      validators: ['url', 'required'],
    }
  },

  permalink() {
    return '/podcasts/' + this.get('id');
  },

  urlRoot() {
    return '/podcasts';
  }
});
