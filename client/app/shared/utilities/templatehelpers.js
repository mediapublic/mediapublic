import colorbrewer from '../colors/colorbrewer';
import _ from 'underscore';
import truncate from 'underscore.string/truncate';
import htmlTruncate from 'html-truncate';

export default {
  randomColor(cid, palette, tones) {
    palette = colorbrewer[palette || 'Spectral'][tones || 9];
    var index = parseInt(cid.replace('c', ''), 10) % palette.length;
    return palette[index];
  },
  _,
  truncate,
  htmlTruncate
};
