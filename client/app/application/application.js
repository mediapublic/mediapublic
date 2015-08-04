// import $ from 'jquery';
// import _ from 'underscore';
import {Application} from 'backbone.marionette';

import LayoutView from './layout-view';


export default Application.extend({
  initialize() {
    this.layout = new LayoutView();
    this.layout.render();
  },
});
