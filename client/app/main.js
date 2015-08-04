import Backbone from 'backbone';

import Application from './application/application';
import Router from './router';


let app = new Application();

app.index = new Router({
  container: app.layout.content
});

// Navigate to the current url
Backbone.history.start();
