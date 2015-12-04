import BackboneForm from 'backbone-forms/distribution/backbone-forms.js';

var OriginalText = BackboneForm.editors.Text;
var Text = BackboneForm.editors.Text.extend({
  // Add a placeholder attribute
  initialize(options) {
    options.schema = options.schema || {};
    options.schema.editorAttrs = options.schema.editorAttrs || {};
    options.schema.editorAttrs.placeholder =
        options.schema.placeholder || options.schema.title || titleize(options.key);
    options.schema.editorAttrs['aria-label'] =
        options.schema.editorAttrs['aria-label'] || options.schema.editorAttrs.placeholder;
    return OriginalText.prototype.initialize.apply(this, arguments);
  }
});

module.exports = Text;
