/**
 * This is a service that loads data on the current user from the server.
 */
import User from 'shared/people/person';

var CurrentUser = User.extend({
  url: '/users/logged-in'
});


var UserService = function() {};


UserService.prototype.start = function() {
  this.currentUser = new CurrentUser();
  this.currentUser.fetch();
  app.currentUser = this.currentUser;
};

export default new UserService();
