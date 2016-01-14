import Model from 'shared/backbone/model';

export default Model.extend({
  schema: {
    short_name: {
      type: 'Text',
      title: 'Short Name',
      validators: ['required']
    },
    phone: {
      type: 'Text',
      validators: ['phone']
    },
    primary_website: {
      type: 'Text',
      validators: ['url'],
      title: 'Website'
    },
    long_description: {
      type: 'WYSIWYG',
      title: 'Long Description',
      validators: ['required']
    },
    address_0: {
      type: 'Text',
      validators: ['required'],
      title: 'Address line 1'
    },
    address_1: {
      type: 'Text',
      title: 'Address line 2',
    },
    city: {
      type: 'Text',
      validators: ['required']
    },
    zipcode: {
      type: 'Text',
      validators: ['required', 'zip']
    },
    state: {
      type: 'Text',
      validators: ['required', 'state']
    },
    image_url: {
      title: 'Cover Photo Url',
      type: 'Text'
    },
    'facebook': {
      type: 'Text',
      help: 'This should be the URL of your profile page.',
      validators: ['url']
    },
    'twitter': {
      type: 'Text',
      help: 'This should be the URL of your profile page.',
      validators: ['url']
    },
    'github': {
      type: 'Text',
      help: 'This should be the URL of your profile page.',
      validators: ['url']
    },
    'instagram': {
      type: 'Text',
      help: 'This should be the URL of your profile page.',
      validators: ['url']
    },
  },

  extraFields: ['facebook', 'twitter', 'github', 'instagram'],

  permalink() {
    return '/organizations/' + this.get('id');
  },

  urlRoot() {
    return '/organizations';
  },

  canUserEdit(user) {
    return user.isAdmin() || user.isOrgAdmin(this);
  }
});
