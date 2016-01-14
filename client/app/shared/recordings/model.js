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
    return '/recordings/' + this.get('id');
  },

  urlRoot() {
    return '/recordings';
  },

  canUserEdit(user) {
    return user.get('id') === this.get('user_id') || user.isOrgAdmin(this.get('organization_id'));
  }
});
