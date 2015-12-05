import Backbone from 'shared/backbone/backbone';

import Application from './application/application';
import IndexRouter from './index/router';
import OrganizationRouter from './organizations/router';
import UserRouter from './users/router';
import RecordingsRouter from './recordings/router';
import HowtosRouter from './howtos/router';
import config from './config.json';
import Header from './header/view';
import templateHelpers from 'shared/utilities/templatehelpers';

// Global namespace
window.app = new Application();

app.config = config;
app.templateHelpers = templateHelpers;

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

app.layout.header.show(new Header());

// Navigate to the current url
Backbone.history.start();
