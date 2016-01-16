import CompositeView from 'shared/views/compositeview';

import template from './collectiontemplate.jade';
import SingleView from './singleview';

export default CompositeView.extend({
  template,
  className: 'help-requests',
  childView: SingleView,
  childViewContainer: '.help-requests-list'
});
