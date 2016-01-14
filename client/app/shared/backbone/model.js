import {Model} from './backbone';
import _ from 'underscore';

export default Model.extend({
  extraFields: [],
  parse(data) {
    return _.extend(data, _.pick(data.extra, this.extraFields));
  },
  save(attributes, options) {
    options = options || {};
    attributes = attributes || _.clone(this.attributes);

    var extra = _.pick(attributes, this.extraFields);
    attributes = _.omit(attributes, this.extraFields);
    attributes.extra = extra;

    options.contentType = 'application/json';
    options.data = JSON.stringify(attributes);

    return Model.prototype.save.call(this, attributes, options);
  },
  canUserEdit(user) {
    throw new Error('CanUserEdit not implemented for ' + this.urlRoot());
  }
});
