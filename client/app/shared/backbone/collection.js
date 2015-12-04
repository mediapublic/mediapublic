import {Collection} from 'backbone';

export default Collection.extend({
  // Automatically unwrap data from the server
  parse: (data) => data.data
});
