import colorbrewer from '../colors/colorbrewer';
import _ from 'underscore';
import truncate from 'underscore.string/truncate';

export default {
  randomColor(cid, palette, tones) {
    var palette = colorbrewer[palette || 'Spectral'][tones || 9];
    var index = parseInt(cid.replace('c', ''), 10) % palette.length;
    return palette[index];
  },
  _,
  truncate
};
