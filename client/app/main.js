import Backbone from 'shared/backbone/backbone';

import Application from './application/application';
import IndexRouter from './index/router';
import OrganizationRouter from './organizations/router';
import UserRouter from './users/router';
import RecordingsRouter from './recordings/router';
import HowtosRouter from './howtos/router';
import HelpRequestsRouter from './helprequests/router';
import SearchResultsRouter from './searchresults/router';
import UserService from './services/userservice';
import TypeaheadService from './services/typeaheadservice';
import SearchService from './services/searchservice';
import config from './config';
import Header from './header/view';
import templateHelpers from 'shared/utilities/templatehelpers';
import _ from 'underscore';
import 'bootstrapjs';

// Global namespace
window.app = new Application();

app.config = config;
app.templateHelpers = templateHelpers;

app.services = {
  user: UserService,
  typeahead: TypeaheadService,
  search: SearchService
};
_.each(app.services, function(service) {
  service.start();
});

app.indexRouter = new IndexRouter({
  container: app.layout.content
});

app.organizationRouter = new OrganizationRouter({
  container: app.layout.content
});

app.userRouter = new UserRouter({
  container: app.layout.content
});

app.recordingsRouter = new RecordingsRouter({
  container: app.layout.content
});

app.howtosRouter = new HowtosRouter({
  container: app.layout.content
});

app.helpRequestsRouter = new HelpRequestsRouter({
  container: app.layout.content
});

app.searchResultsRouter = new SearchResultsRouter({
  container: app.layout.content
});

app.layout.header.show(new Header());

// Navigate to the current url
Backbone.history.start();

