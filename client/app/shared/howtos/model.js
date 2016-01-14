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
  },

  canUserEdit(user) {
    return this.get('author_id') == user.get('id') || user.isOrgAdmin(this.get('organization_id'));
  }
});
