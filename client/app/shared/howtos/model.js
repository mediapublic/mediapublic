import Model from 'shared/backbone/model';

export default Model.extend({
  schema: {
    title: {
      type: 'Text',
      validators: ['required'],
    },
    contents: 'WYSIWYG'
  },

  permalink() {
    return '/howtos/' + this.get('id');
  },

  urlRoot() {
    return '/howtos';
  }
});
