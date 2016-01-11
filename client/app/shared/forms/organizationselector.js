import Text from './text';
import {organizations} from 'shared/search/datasets';
import storage from 'shared/organizations/storage';
import _ from 'underscore';


export default Text.extend({
  dataset: _.extend({}, organizations, { limit: 5 }),

  storage,

  render() {
    Text.prototype.render.apply(this);

    _.defer(() => {
      this.$el.typeahead({}, this.dataset);
      this.$el.on('typeahead:select', (event, suggestion) => {
        this.value = suggestion.id;
        this.preview = this.$el.val();
      });
      this.$el.on('typeahead:change', (event) => {
        if (this.$el.val() !== this.preview) {
          this.value = '';
          this.$el.val('');
        }
      });
    });

    return this;
  },

  getValue() {
    return this.value;
  },

  setValue(value) {
    this.value = value;
    if (this.value) {
      this.storage.find(this.value).then((model) => {
        this.$el.val(model.get('short_name'));
        this.preview = model.get('short_name');
      });
    }
  },

  validate() {
    var ret = Text.prototype.validate.apply(this, arguments);
    if (this.$el.val() && !this.value) {
      return "Please select one of the options from the drop down."
    }
    return ret;
  }
});
