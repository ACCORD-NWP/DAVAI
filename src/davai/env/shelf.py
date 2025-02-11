#!/usr/bin/env python3
# -*- coding:Utf-8 -*-
"""
A shelf is a Vortex pseudo-experiment in which are stored input data as in a Vortex experiment.
A Shelf object helps to move a shelf between archive, marketplace cache and tarfiles.
"""

import os
import configparser
import tempfile
import subprocess
import tarfile

from . import config, guess_host
from .util import expandpath

# set variables
host = guess_host()
vortex_cache_config = os.path.join(config['packages']['vortex'],
                                   'conf', 'cache-{}.ini'.format(host))
cache_config = configparser.ConfigParser()
cache_config.read(expandpath(vortex_cache_config))
cache_config.read(expandpath(cache_config['marketplace-vortex']['externalconf_davai_path']))
marketplacecache_rootdir = cache_config['marketplace_xp']['rootdir']


class Shelf(object):
    """A shelf is a Vortex pseudo-experiment in which are stored input data as in a Vortex experiment."""

    vtx_vapp_vconf = os.path.join('vortex', 'davai', 'shelves')
    rootdir = os.path.join(marketplacecache_rootdir, vtx_vapp_vconf)

    def __init__(self, shelf):
        if shelf.endswith('.tar') or shelf.endswith('.tgz'):
            self.name = shelf[:-4]
            self.tarfile = shelf
        else:
            self.name = shelf
            self.tarfile = shelf + '.tar'
        self.radical, self.user = shelf.split('@')
        if self.user == 'davai':
            self.user = config['defaults']['davai_alias_user']
            self.vtx_vapp_vconf = os.path.join(config['defaults']['davai_alias_arch_subdir'], self.vtx_vapp_vconf)

    def mkt2tar(self, out_dir=None, gz_compression=False, **_):
        """Tar (and compress) a shelf into a tar/tgz."""
        openmode = 'w'
        if gz_compression:
            self.tarfile = self.tarfile.replace('.tar', '.tgz')
            openmode = 'w:gz'
        current = os.getcwd()
        if out_dir is None:
            out_dir = current
        os.chdir(self.rootdir)
        out_filename = os.path.join(out_dir, self.tarfile)
        with tarfile.open(out_filename, openmode) as t:
            t.add(self.name)
        os.chdir(current)

    def tar2mkt(self, **_):
        """Extracts a tar/tgz shelf into marketplacecache."""
        assert os.path.exists(self.tarfile)
        with tarfile.open(self.tarfile, 'r') as t:
            def is_within_directory(directory, target):
                
                abs_directory = os.path.abspath(directory)
                abs_target = os.path.abspath(target)
            
                prefix = os.path.commonprefix([abs_directory, abs_target])
                
                return prefix == abs_directory
            
            def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
            
                for member in tar.getmembers():
                    member_path = os.path.join(path, member.name)
                    if not is_within_directory(path, member_path):
                        raise Exception("Attempted Path Traversal in Tar File")
            
                tar.extractall(path, members, numeric_owner=numeric_owner) 
                
            
            safe_extract(t, path=self.rootdir)

    def _mkt_arch(self, archive, to='arch'):
        if to == 'arch':
            mirror_args = ['-R', self.name, self.radical]
        else:
            mirror_args = ['', self.radical, self.name]
        lftp_script = [
            '#!/usr/bin/bash',
            'cd {}'.format(self.rootdir),
            'lftp {}@{} <<EOG'.format(self.user, archive),
            'cd {}'.format(self.vtx_vapp_vconf),
            'mirror {} {} {}'.format(*mirror_args),
            'bye',
            'EOG',
            ]
        temp_request = tempfile.mkstemp()[1]
        print("Temp request:", temp_request)
        with open(temp_request, 'w') as req:
            req.writelines([line + '\n' for line in lftp_script])
        subprocess.check_call(['bash', temp_request])

    def arch_prestage(self, archive, **_):
        """ """
        from bronx.system.mf import prestage
        prestage([os.path.join('/home', self.vtx_vapp_vconf, self.radical, '*')],
                 mail='alexandre.mary@meteo.fr',
                 archive_machine=archive)

    def mkt2arch(self, archive, **_):
        """For a shelf = radical@user, mirrors *shelf* from marketplacecache to *radical* in user@archive"""
        self._mkt_arch(archive, to='arch')

    def arch2mkt(self, archive, **_):
        """For a shelf = radical@user, mirrors *radical* from user@archive into marketplacecache as *shelf*"""
        self._mkt_arch(archive, to='mkt')
