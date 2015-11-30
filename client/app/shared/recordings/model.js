import {Model} from 'backbone';

export default Model.extend({
  schema: {
    title: {
      type: 'Text',
      validators: ['required'],
    },
    title: {
      type: 'Text',
      validators: ['url', 'required'],
    }
  },

  urlRoot() {
    return app.config.apiUrl + '/recordings';
  }
});
