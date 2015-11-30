import _ from 'underscore';

function guid() {
  function s4() {
    return Math.floor((1 + Math.random()) * 0x10000)
      .toString(16)
      .substring(1);
  }
  return s4() + s4() + '-' + s4() + '-' + s4() + '-' +
    s4() + '-' + s4() + s4() + s4();
}

export default {
  fakePerson: {
    first: 'Gabe',
    last: 'Isman',
    phone: '(413) 559-0176',
    primary_website: 'http://gabe.link',
    address_0: '71 29th St.',
    address_1: 'Apt. 2',
    city: 'San Francisco',
    zipcode: '94110',
    state: 'CA',
    twitter: '@gabeisman',
    facebook: 'https://www.facebook.com/gabeisman',
    instagram: '@gabeisman',
    profile_picture: 'https://scontent-iad3-1.xx.fbcdn.net/hphotos-xfa1/t31.0-8/11203569_10153158191676187_9040442632983579616_o.jpg'
  },

  replicate(fake, times, opt_new) {
    var fakes = [];
    for (var i = 0; i < 25; i++) {
      if (opt_new) {
        fakes.push(fake);
      } else {
        fakes.push(_.extend({id: guid()}, fake));
      }
    }
    return fakes;
  }
};
