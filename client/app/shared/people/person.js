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
  },

  isAdmin() {
    return this.get('is_site_admin');
  },

  isOrgAdmin(organization) {
    if (!organization) {
      return false;
    }

    if (typeof organization !== 'string') {
      organization = organization.get('id');
    }

    return this.get('is_org_admin') && organization == this.get('organization_id');
  },

  canUserEdit(user) {
    return user.isOrgAdmin(this.get('organization_id')) || user.get('id') == this.get('id');
  }
});
