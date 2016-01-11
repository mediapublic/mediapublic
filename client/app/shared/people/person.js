import Model from 'shared/backbone/model';

export default Model.extend({
  schema: {
    display_name: {
      type: 'Text',
      title: 'Name',
      validators: ['required']
    },
    email: {
      type: 'Text',
      validators: ['email', 'required']
    }
  },

  permalink() {
    return '/users/' + this.get('id');
  },

  urlRoot() {
    return '/users';
  }
});
