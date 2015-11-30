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
    bio: 'I tell computers to do things and sometimes they listen to me.'
  },

  fakeRecording: {
    title: 'Amid A Violent Religious Rift, Pope Preaches Harmony In CAR',
    url: 'http://www.npr.org/2015/11/29/457795088/amid-a-violent-religious-rift-pope-preaches-harmony-in-car',
    description: 'Pope Francis is calling for communal and religious harmony during a visit to the Central African Republic, the final stop of his first African tour. The country has been racked by a deadly conflict driven by Christian and Muslim militias.'
  },

  fakeHelpRequest: {
    title: 'Help us tag audio',
    text: 'We need help going through our audio archives and tagging content so we can surface it.',
    contact_email: 'gabe.isman@fake.com'
  },

  replicate(fake, times, opt_new) {
    var fakes = [];
    for (var i = 0; i < times; i++) {
      if (opt_new) {
        fakes.push(fake);
      } else {
        fakes.push(_.extend({id: guid()}, fake));
      }
    }
    return fakes;
  }
};
