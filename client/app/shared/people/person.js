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
    },
    organization_id: {
      type: 'Organization',
      title: 'Organization',
      help: 'Are you associated with a public media organization? Note: may require authorization from organization administrator.',
      placeholder: 'Search for your organization...'
    }
  },

  permalink() {
    return '/users/' + this.get('id');
  },

  urlRoot() {
    return '/users';
  }
});
