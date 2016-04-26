# -*- coding: utf-8 -*-
'''
Universe Notebook Widget
=============================
'''
import subprocess
import pandas as pd
from glob import glob
from os import sep, getcwd, path
from base64 import b64decode
from traitlets import Unicode
from exa.widget import ContainerWidget


class UniverseWidget(ContainerWidget):
    '''
    Custom widget for the :class:`~atomic.universe.Universe` data container.
    '''
    _view_module = Unicode('nbextensions/exa/atomic/universe').tag(sync=True)
    _view_name = Unicode('UniverseView').tag(sync=True)

    def _handle_field(self, data):
        values = pd.read_json(data.pop('values'), typ='series')
        values.sort_index(inplace=True)
        field = pd.DataFrame.from_dict({key: [val] for key, val in data.items()})
        field['frame'] = 0
        field['dxj'] = field['dxk'] = 0
        field['dyi'] = field['dyk'] = 0
        field['dzi'] = field['dzj'] = 0
        self.container.add_field(field, None, [values])

    def _handle_image(self, data):
        savedir = getcwd()
        if self.params['save_dir']:
            savedir = self.params['save_dir']
        if self.params['file_name']:
            imgname = filename
        else:
            nxt = 0
            try:
                lgfls = [fl.split(sep)[-1] for fl in glob(sep.join([savedir, '*png']))]
                numbers = [''.join([c for c in fl if c.isdigit()]) for fl in lgfls]
                last = sorted([int(num) for num in numbers if num])[-1]
                nxt = last + 1
                imgname = '{:06d}.png'.format(nxt)
            except:
                imgname = '{:06d}.png'.format(nxt)
        if path.isfile(sep.join([savedir, imgname])):
            print("Automatic file name generation failed. Use uni._widget.params['file_name']")
            return
        with open(sep.join([savedir, imgname]), 'wb') as f:
            f.write(b64decode(data.replace('data:image/png;base64,', '')))
        # TODO : this likely won't work on windows but SHOULD automatically
        #        crop the image to minimize whitespace of the final image.
        try:
            crop = ' '.join(['convert -trim', imgname, imgname])
            subprocess.call(crop, cwd=savedir, shell=True)
        except:
            pass
