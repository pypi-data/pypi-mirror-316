#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
# mman, Multi-Language, Multi-Platform Man Pager.
# Copyright (C) 2024 MikeTurkey All rights reserved.
# contact: voice[ATmark]miketurkey.com
# license: GPLv3 License
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# ADDITIONAL MACHINE LEARNING PROHIBITION CLAUSE
#
# In addition to the rights granted under the applicable license(GPL-3),
# you are expressly prohibited from using any form of machine learning,
# artificial intelligence, or similar technologies to analyze, process,
# or extract information from this software, or to create derivative
# works based on this software.
#
# This prohibition includes, but is not limited to, training machine
# learning models, neural networks, or any other automated systems using
# the code or output of this software.
#
# The purpose of this prohibition is to protect the integrity and
# intended use of this software. If you wish to use this software for
# machine learning or similar purposes, you must seek explicit written
# permission from the copyright holder.
#
# see also 
#     GPL-3 Licence: https://www.gnu.org/licenses/gpl-3.0.html.en
#     Mike Turkey.com: https://miketurkey.com/

import os
import time
import re
import sys
import unicodedata
import tomllib
import types
import typing
import pydoc
import copy
import gzip
import hashlib
if __name__ == '__main__':
    from man_common import Mainfunc
else:
    try:
        from .man_common import Mainfunc
    except:
        from man_common import Mainfunc


class Man_roottoml(object):
    __d: typing.Final[dict] =\
        {('fb', 'jpn', 'arm64'): (104, 116, 116, 112, 115, 58, 47, 47,
                                  100, 50, 52, 109, 119, 121, 108, 48,
                                  98, 107, 106, 112, 112, 51, 46, 99,
                                  108, 111, 117, 100, 102, 114, 111,
                                  110, 116, 46, 110, 101, 116, 47,
                                  109, 97, 110, 106, 112, 102, 98, 47,
                                  114, 111, 111, 116, 46, 116, 111,
                                  109, 108, 46, 103, 122),
         ('fb', 'eng', 'arm64'): (104, 116, 116, 112, 115, 58, 47, 47,
                                  100, 50, 52, 109, 119, 121, 108, 48,
                                  98, 107, 106, 112, 112, 51, 46, 99,
                                  108, 111, 117, 100, 102, 114, 111,
                                  110, 116, 46, 110, 101, 116, 47,
                                  109, 97, 110, 101, 110, 102, 98, 47,
                                  114, 111, 111, 116, 46, 116, 111,
                                  109, 108, 46, 103, 122),
         ('ob', 'eng', 'arm64'): (104, 116, 116, 112, 115, 58, 47, 47,
                                  100, 50, 52, 109, 119, 121, 108, 48,
                                  98, 107, 106, 112, 112, 51, 46, 99,
                                  108, 111, 117, 100, 102, 114, 111,
                                  110, 116, 46, 110, 101, 116, 47,
                                  109, 97, 110, 101, 110, 111, 98, 47,
                                  114, 111, 111, 116, 46, 116, 111,
                                  109, 108, 46, 103, 122)}

    def __init__(self):
        self.og_vernamekey: str = ''
        self.og_manhashfpath: str = ''
        self.og_roottomlfpath: str = ''
        self.og_manenv_os2: str = ''
        self.og_manenv_lang: str = ''
        self.og_manenv_arch: str = ''
        self._status: str = ''
        self._thedate: str = ''
        self._osname: str = ''
        self._urls: list = list()
        self._baseurls: list = list()
        self._manhashfpath: str = ''
        self._message: str = ''
        self._rootstr: str = ''
        self._rootdic: dict = dict()
        self._mantomlurls: list = list()
        return

    @property
    def status(self) -> str:
        return self._status

    @property
    def thedate(self) -> str:
        return self._thedate

    @property
    def osname(self) -> str:
        return self._osname

    @property
    def urls(self) -> list:
        return self._urls

    @property
    def baseurls(self) -> list:
        return self._baseurls

    @property
    def manhashfpath(self) -> str:
        return self._manhashfpath

    @property
    def message(self) -> str:
        return self._message

    def print_attributes(self):
        for k, v in self.__dict__.items():
            print('k: ', k)
            print('  v:', v)
        return

    def _getrooturl(self):
        d: dict = self.__d.copy()
        t: tuple = (self.og_manenv_os2, self.og_manenv_lang,
                    self.og_manenv_arch)
        errmes: str = ''
        skip1: bool = False
        if not skip1:
            if t not in d.keys():
                errmes = 'Error: Not root key. [{0}]'.format(t)
                print(errmes, file=sys.stderr)
                exit(1)
            data: typing.Final[tuple] = d[t]
            roottomlurl: typing.Final[str] = ''.join([chr(i) for i in data])
        return roottomlurl

    def make(self):
        mainfunc = Mainfunc
        roottomlurl: typing.Final[str] = self._getrooturl()
        errmes: str
        vname: str
        chklist: list = [('og_veramekey', self.og_vernamekey),
                         ('og_manhashfpath', self.og_manhashfpath),
                         ('og_roottomlfpath', self.og_roottomlfpath)]
        for vname, v in chklist:
            if isinstance(v, str) != True:
                errmes = 'Error: {0} is NOT string type.'.format(vname)
                raise TypeError(errmes)
        if self.og_vernamekey == '':
            errmes = 'Error: Not og_vernamekey value.'
            raise ValueError(errmes)
        rootdic: typing.Final[dict]
        rootstr: typing.Final[str]
        gzbys: bytes
        rootbys: typing.Final[bytes]
        s: str
        if self.og_roottomlfpath != '':
            if self.og_roottomlfpath.endswith('.toml'):
                with open(self.og_roottomlfpath, 'rt') as fp:
                    rootstr = fp.read()
            elif self.og_roottomlfpath.endswith('.toml.gz'):
                with open(self.og_roottomlfpath, 'rb') as fp:
                    gzbys = fp.read()
                rootbys = gzip.decompress(gzbys)
                rootstr = rootbys.decode('UTF-8')
        else:
            if roottomlurl.endswith('toml.gz'):
                gzbys = mainfunc.loadbytes_url(roottomlurl)
                rootbys = gzip.decompress(gzbys)
                rootstr = rootbys.decode('UTF-8')
                roottomlurl_sha3 = roottomlurl + '.SHA3-256'
                try:
                    s = mainfunc.loadstring_url(roottomlurl_sha3)
                except:
                    s = ''
                if s != '':
                    templist: list = s.split(' ', 1)
                    hashdg_url = templist[1].rstrip()
                    hobj = hashlib.new('SHA3-256')
                    hobj.update(gzbys)
                    hashdg_body: str = hobj.hexdigest()
                    if hashdg_url != hashdg_body:
                        mes = 'Warning: Not match hashdigest.'
                        print(mes)
                        print('  hashdg_url :', hashdg_url)
                        print('  hashdg_body:', hashdg_body)
            if roottomlurl.endswith('.toml'):
                rootstr = mainfunc.loadstring_url(roottomlurl)
        rootdic = tomllib.loads(rootstr)
        self._rootstr = rootstr
        self._rootdic = copy.copy(rootdic)
        self._baseurls = rootdic.get('baseurls', [])
        if len(self.baseurls) == 0:
            errmes = 'Error: Empty baseurls values in root.toml'
            print(errmes, file=sys.stderr)
            exit(1)
        self._message = rootdic.get('message', '')
        url: str
        s: str
        tpl: tuple
        vernamekey: str = ''
        if self.og_manhashfpath == '':
            tpl = mainfunc.geturlpath_man(self._rootdic, self.og_vernamekey)
            self._mantomlurls, self._osname, self._status, self._thedate, vernamekey = tpl
            for url in self._mantomlurls:
                if url.endswith('.toml'):
                    s = mainfunc.loadstring_url(url)
                    tomldic = tomllib.loads(s)
                elif url.endswith('.toml.gz'):
                    gzbys = mainfunc.loadbytes_url(url)
                    mantomlbys: bytes = gzip.decompress(gzbys)
                    mantomlstr: str = mantomlbys.decode('UTF-8')
                    tomldic = tomllib.loads(mantomlstr)
        else:
            with open(self.og_manhashfpath, 'rb') as fp:
                tomldic = tomllib.load(fp)
        return copy.copy(tomldic)


class Man_mantoml(object):
    def __init__(self):
        self.og_tomldic: dict = dict()
        self.og_osname_root: str = ''
        self.og_mannum: str = ''
        self.og_manname: str = ''
        self.og_baseurls: list = list()
        self.og_fnamemode: str = 'hash'
        self._osname: str = ''
        self._arch: str = ''
        self._lang: str = ''
        self._retmake: list[tuple] = list()
        return

    @property
    def osname(self) -> str:
        return self._osname

    @property
    def arch(self) -> str:
        return self._arch

    @property
    def lang(self) -> str:
        return self._lang

    @property
    def retmake(self) -> list[tuple]:
        return self._retmake

    def vcheck_og_tomldic(self):
        vname: str
        for vname in self.og_tomldic.keys():
            if vname == 'OSNAME':
                return
        errmes: str = 'Error: RuntimeError, Invalid tomldic.'
        print(errmes, file=sys.stderr)
        exit(1)

    def vcheck_og_osname_root(self):
        ptns: typing.Final[tuple] = ('FreeBSD', 'OpenBSD')
        ptn: str
        for ptn in ptns:
            if self.og_osname_root.startswith(ptn):
                return
        errmes: str = 'Error: Invalid OSNAME on man metadata.'
        print(errmes, file=sys.stderr)
        exit(1)

    def vcheck_og_mannum(self):
        ptns: typing.Final[tuple] = ('', '1', '2', '3', '4',
                                     '5', '6', '7', '8', '9')
        ptn: str = ''
        for ptn in ptns:
            if self.og_mannum == ptn:
                return
        errmes: str = 'Error: Invalid Man section number(1-9). [{0}]'.format(
            self.on_mannum)
        print(errmes, file=sys.stderr)
        exit(1)

    def vcheck_og_manname(self):
        ptn: typing.Final[str] = r'^[A-Za-z0-9\_\-\[]+'
        reobj: typing.Final = re.match(ptn, self.og_manname)
        if reobj == None:
            errmes: str = 'Error: Invalid man name string. [{0}]'.format(
                self.og_manname)
            print(errmes, file=sys.stderr)
            exit(1)
        return

    def vcheck_og_baseurls(self):
        errmes: str
        url: str
        if isinstance(self.og_baseurls, list) != True:
            errmes = 'Error: Man_mantoml.og_baseurls is NOT list type.'
            raise TypeError(errmes)
        if len(self.og_baseurls) == 0:
            errmes = 'Error: Runtime Error, Empty Man_mantoml.og_baseurls.'
            raise ValueError(errmes)
        for url in self.og_baseurls:
            if isinstance(url, str) != True:
                errmes = 'Error: Man_mantoml.og_baseurls element is NOT string type.'
                raise TypeError(errmes)
            if url.startswith('https://') != True:
                errmes = 'Error: baseurl protocol is NOT "https://". [{0}]'.format(
                    url)
                print(errmes, file=sys.stderr)
                exit(1)
            if ('miketurkey.com' not in url) and ('cloudfront.net' not in url):
                errmes = 'Error: baseurl is NOT "miketurkey.com". [{0}]'.format(
                    url)
                print(errmes, file=sys.stderr)
                exit(1)
        return

    def vcheck_og_fnamemode(self):
        errmes: str
        if isinstance(self.og_fnamemode, str) != True:
            errmes = 'Error: og_fnamemode is NOT string type.'
            raise TypeError(errmes)
        if self.og_fnamemode not in ('raw', 'hash'):
            errmes = 'Error: og_fnamemode is NOT raw and hash.'
            print(errmes, file=sys.stderr)
            exit(1)
        return

    @staticmethod
    def _mkfname_webdb(fname: str, hashdg: str, fnamemode: str) -> str:
        errmes: str = ''
        ptn_hashdg: typing.Final[str] = r'[0-9a-f]{64}'
        ptn_fname:  typing.Final[str] = r'.+\.[1-9]'
        if re.fullmatch(ptn_fname, fname) == None:
            errmes = 'Error: Invalid fname. [{0}]'.format(fname)
            print(errmes, file=sys.stderr)
            exit(1)
        if re.fullmatch(ptn_hashdg, hashdg) == None:
            errmes = 'Error: Runtime Error, Invalid hashdg pattern. [{0}]'.format(
                hashdg)
            print(errmes, file=sys.stderr)
            exit(1)
        if fnamemode == 'raw':
            return fname
        templist: list
        if fnamemode == 'hash':
            templist = fname.rsplit('.', 1)
            fname_ext: typing.Final[str] = templist[1]
            retstr: typing.Final[str] = hashdg[0:6] + '.' + fname_ext + '.gz'
            return retstr
        errmes = 'Error: Runtime Error, Invalid fnamemode. [{0}]'.format(
            fnamemode)
        print(errmes, file=sys.stderr)
        exit(1)

    def print_attributes(self):
        for k, v in self.__dict__.items():
            print('k: ', k)
            print('  v:', v)
        return

    def make(self) -> list[tuple]:
        self.vcheck_og_tomldic()
        self.vcheck_og_osname_root()
        self.vcheck_og_mannum()
        self.vcheck_og_manname()
        self.vcheck_og_baseurls()
        self.vcheck_og_fnamemode()
        fnameurldic: dict = dict()
        for k, v in self.og_tomldic.items():
            if k in ('OSNAME', 'ARCH', 'LANG'):
                self._osname = v if k == 'OSNAME' else self._osname
                self._arch = v if k == 'ARCH' else self._arch
                self._lang = v if k == 'LANG' else self._lang
                continue
            fname: str = k
            hashdg: str = v['hash']
            fname_new: str = self._mkfname_webdb(
                fname, hashdg, self.og_fnamemode)

            def inloop1(baseurl: str, hashdg: str, fname: str) -> str:
                mainfunc = Mainfunc
                s: typing.Final[str] = baseurl + '/' + \
                    hashdg[0:2] + '/' + hashdg + '/' + fname
                return (mainfunc.normurl(s), hashdg)
            hashurls: list = [inloop1(baseurl, hashdg, fname_new)
                              for baseurl in self.og_baseurls]
            fnameurldic[fname] = hashurls
        if self.og_osname_root != self.osname:
            errmes = 'Error: Mismatch OSNAME. [{0}, {1}]'.format(
                self.og_osname_root, self.osname)
            print(errmes)
            exit(1)
        fnameurldictkeys: list
        if self.og_mannum != '':
            fnameurldictkeys = [self.og_manname + '.' + self.og_mannum]
        else:
            fnameurldictkeys = ['{0}.{1}'.format(
                self.og_manname, i) for i in range(1, 10)]
        retlist: list
        for fname in fnameurldictkeys:
            retlist = fnameurldic.get(fname, [])
            if len(retlist) >= 1:
                self._retmake = retlist
                return retlist
        return list()


class _Main_man(object):
    @staticmethod
    def norm_punctuation(pagerstr: str) -> str:
        ptn = r'[\u2011]|[\u2012]|[\u2013]'
        return re.sub(ptn, '-', pagerstr)

    @staticmethod
    def show_listman_n(secnum: int, vernamekey: str, os2: str, lang: str, arch: str):
        roottomlobj = Man_roottoml()
        roottomlobj.og_vernamekey = '@LATEST-RELEASE'
        roottomlobj.og_manhashfpath = ''
        roottomlobj.og_roottomlfpath = ''
        roottomlobj.og_manenv_os2 = os2
        roottomlobj.og_manenv_lang = lang
        roottomlobj.og_manenv_arch = arch
        tomldic: typing.Final[dict] = roottomlobj.make()

        def inloop(name: str, secnum: int) -> str:
            ptns = ('.1', '.2', '.3', '.4', '.5', '.6', '.7', '.8', '.9')
            ptn: str = ptns[secnum - 1]
            if name.endswith(ptn):
                return name.removesuffix(ptn)
            return ''
        mannames = [inloop(name, secnum) for name,
                    d in tomldic.items() if isinstance(d, dict) == True]
        mannames = [name for name in mannames if name != '']
        mannames.sort()
        for name in mannames:
            print(name)
        exit(0)

    @staticmethod
    def show_listman(vernamekey: str, os2: str, lang: str, arch: str):
        roottomlobj = Man_roottoml()
        roottomlobj.og_vernamekey = '@LATEST-RELEASE'
        roottomlobj.og_manhashfpath = ''
        roottomlobj.og_roottomlfpath = ''
        roottomlobj.og_manenv_os2 = os2
        roottomlobj.og_manenv_lang = lang
        roottomlobj.og_manenv_arch = arch
        tomldic: typing.Final[dict] = roottomlobj.make()

        def inloop(name: str) -> str:
            ptns = ('.1', '.2', '.3', '.4', '.5', '.6', '.7', '.8', '.9')
            for ptn in ptns:
                if name.endswith(ptn):
                    return name.removesuffix(ptn)
            return name
        mannames = [inloop(name) for name, d in tomldic.items()
                    if isinstance(d, dict) == True]
        mannames.sort()
        for name in mannames:
            print(name)
        exit(0)

    @staticmethod
    def show_listos(os2: str, lang: str, arch: str):
        mainfunc = Mainfunc
        roottomlobj = Man_roottoml()
        roottomlobj.og_vernamekey = '@LATEST-RELEASE'
        roottomlobj.og_manhashfpath = ''
        roottomlobj.og_roottomlfpath = ''
        roottomlobj.og_manenv_os2 = os2
        roottomlobj.og_manenv_lang = lang
        roottomlobj.og_manenv_arch = arch
        roottomlobj.make()
        rootdic: typing.Final[dict] = roottomlobj._rootdic
        osnames = [osname for vername, osname, status,
                   thedate, urls in mainfunc.iter_rootdic(rootdic)]
        [print(s) for s in osnames]
        exit(0)

    @staticmethod
    def getstring_pagerurl(pagerurl: typing.Final[str], hashdg: typing.Final[str]) -> str:
        mainfunc = Mainfunc
        b: typing.Final[bytes]
        if pagerurl.endswith('.gz'):
            gzbys: typing.Final[bytes]
            gzbys = mainfunc.loadbytes_url(pagerurl, exception=False)
            if len(gzbys) == 0:
                return ''
            try:
                b = gzip.decompress(gzbys)
            except:
                return ''
            hobj: typing.Final = hashlib.new('SHA3-256')
            hobj.update(gzbys)
            if hashdg != hobj.hexdigest():
                return ''
            return b.decode('UTF-8')
        else:
            b = mainfunc.loadbytes_url(pagerurl, exception=False)
            if len(b) == 0:
                return ''
            hobj: typing.Final = hashlib.new('SHA3-256')
            hobj.update(b)
            if hashdg != hobj.hexdigest():
                return
            return b.decode('UTF-8')


class Main_manXXYY(object):
    version:     str = '0.0.4'
    versiondate: str = '21 Dec 2024'

    def __init__(self):
        self._manenv_os2: str = ''
        self._manenv_lang: str = ''
        self._manenv_arch: str = ''
        return

    @property
    def manenv_os2(self):
        return self._manenv_os2

    @property
    def manenv_lang(self):
        return self._manenv_lang

    @property
    def manenv_arch(self):
        return self._manenv_arch

    @staticmethod
    def show_helpmes(os2: str, lang: str):
        version: str = Main_manXXYY.version
        versiondate: str = Main_manXXYY.versiondate
        langptn: dict = {'eng': 'English', 'jpn': 'Japanese'}
        language: str = langptn[lang]
        cmdnames: dict = {('fb', 'eng'): 'manenfb', ('fb', 'jpn'): 'manjpfb',
                          ('ob', 'eng'): 'manenob'}
        cmdname: str = cmdnames[(os2, lang)]
        doclicenses: dict = {'fb': 'FDL License including a prohibition clause for AI training.',
                             'ob': '3-Clause BSD License including a prohibition clause for AI training.'}
        doclicense: str = doclicenses[os2]
        osnames: dict = {'fb': 'FreeBSD', 'ob': 'OpenBSD'}
        osname: str = osnames[os2]
        copyright_engmans: dict = {('fb', 'eng'): 'Copyright of man pages: FreeBSD Project.',
                                   ('ob', 'eng'): 'Copyright of man pages: The copyright belongs to the authors of the man pages.'}
        copyright_engman: str = copyright_engmans.get((os2, lang), '')
        meses: list = list()
        meses_eng: list = list()
        meses =\
            ['{0} written by MikeTurkey'.format(cmdname),
             'ver {0}, {1}'.format(version, versiondate),
             '2024 Copyright MikeTurkey ALL RIGHT RESERVED.',
             'ABSOLUTELY NO WARRANTY.',
             'Software: GPLv3 License including a prohibition clause for AI training.',
             'Document: {0}'.format(doclicense),
             '{0} man documents were translated by MikeTurkey using Deep-Learning.'.format(
                 osname),
             '',
             'SYNOPSIS',
             '  {0} [OPT] [mannum] [name]'.format(cmdname),
             '',
             'Summary',
             '  {0} {1}-man Pager.'.format(osname, language),
             '',
             'Description',
             '  {0} is pager of {1} {2} man using python3.'.format(
                 cmdname, osname, language),
             '  The program does not store man-data and download it with each request.',
             '  Since it is a Python script, it is expected to run on many operating systems in the future.',
             '  We can read the {0} {1} man on many Operating Systems.'.format(
                 osname, language),
             '  There is man-data that is not fully translated, but this is currently by design.',
             '  Please note that I do not take full responsibility for the translation of the documents.',
             '',
             'Example',
             '  $ {0} ls'.format(cmdname),
             '      print ls man.',
             '  $ {0} 1 head'.format(cmdname),
             '      print head 1 section man.',
             '  $ {0} --version'.format(cmdname),
             '      Show the message',
             '  $ {0} --listman'.format(cmdname),
             '      Show man page list.',
             '  $ {0} --listman1'.format(cmdname),
             '      Show man 1 page list.',
             '  $ {0} --listos'.format(cmdname),
             '      Show os name list of man.',
             '']
        meses_eng =\
            ['{0} written by MikeTurkey'.format(cmdname),
             'ver {0}, {1}'.format(version, versiondate),
             '2024 Copyright MikeTurkey ALL RIGHT RESERVED.',
             'ABSOLUTELY NO WARRANTY.',
             'Software: GPLv3 License including a prohibition clause for AI training.',
             '{0}'.format(copyright_engman),
             '',
             'SYNOPSIS',
             '  {0} [OPT] [mannum] [name]'.format(cmdname),
             '',
             'Summary',
             '  {0} {1}-man Pager.'.format(osname, language),
             '',
             'Description',
             '  {0} is pager of {1} {2} man using python3.'.format(
                 cmdname, osname, language),
             '  The program does not store man-data and download it with each request.',
             '  Since it is a Python script, it is expected to run on many operating systems in the future.',
             '  We can read the {0} {1} man on many Operating Systems.'.format(
                 osname, language),
             '',
             'Example',
             '  $ {0} ls'.format(cmdname),
             '      print ls man.',
             '  $ {0} 1 head'.format(cmdname),
             '      print head 1 section man.',
             '  $ {0} --version'.format(cmdname),
             '      Show the message',
             '  $ {0} --listman'.format(cmdname),
             '      Show man page list.',
             '  $ {0} --listman1'.format(cmdname),
             '      Show man 1 page list.',
             '  $ {0} --listos'.format(cmdname),
             '      Show os name list of man.',
             '']
        new_meses: list = list()
        new_meses = meses_eng if lang == 'eng' else meses
        for s in new_meses:
            print(s)
        exit(0)

    def set_manenv(self, os2: str, lang: str, arch: str):
        os2_ptn:  typing.Final[tuple] = ('fb', 'ob')
        lang_ptn: typing.Final[tuple] = ('eng', 'jpn')
        arch_ptn: typing.Final[tuple] = ('arm64')
        errmes: str = ''
        if os2 not in os2_ptn:
            errmes = 'Error: Invalid os2 type. [{0}]'.format(os2)
            print(errmes, file=sys.stderr)
            exit(1)
        if lang not in lang_ptn:
            errmes = 'Error: Invalid lang type. [{0}]'.format(lang)
            print(errmes, file=sys.stderr)
            exit(1)
        if arch not in arch_ptn:
            errmes = 'Error: Invalid arch type. [{0}]'.format(arch)
            print(errmes, file=sys.stderr)
            exit(1)
        self._manenv_os2 = os2
        self._manenv_lang = lang
        self._manenv_arch = arch
        return

    def main(self, os2: str = '', lang: str = '', arch: str = ''):
        mainfunc = Mainfunc
        _main_man = _Main_man
        opt = types.SimpleNamespace(manhashfpath='', mannum='', manname='',
                                    listos=False, listman=False, release='',
                                    listman1=False, listman2=False, listman3=False,
                                    listman4=False, listman5=False, listman6=False,
                                    listman7=False, listman8=False, listman9=False)
        self.set_manenv(os2, lang, arch)
        '''
        vernamekey = '@LATEST-RELEASE';
        roottomlobj = Man_roottoml()
        roottomlobj.og_vernamekey = vernamekey;
        roottomlobj.og_manhashfpath  = opt.manhashfpath;
        roottomlobj.og_roottomlfpath = '';
        roottomlobj.og_manenv_os2  = self.manenv_os2;
        roottomlobj.og_manenv_lang = self.manenv_lang;
        roottomlobj.og_manenv_arch = self.manenv_arch;
        tomldic = roottomlobj.make();
        roottomlobj.print_attributes();
        exit(0);
        '''
        arg1 = ''
        arg2 = ''
        on_manhash = False
        on_release = False
        listmandict: dict = {'--listman1': 'listman1', '--listman2': 'listman2',
                             '--listman3': 'listman3', '--listman4': 'listman4',
                             '--listman5': 'listman5', '--listman6': 'listman6',
                             '--listman7': 'listman7', '--listman8': 'listman8',
                             '--listman9': 'listman9'}
        for arg in sys.argv[1:]:
            if on_manhash:
                opt.manhashfpath = os.path.abspath(arg)
                on_manhash = False
                continue
            if on_release:
                opt.release = arg
                on_release = False
                continue
            if arg == '--manhash':
                on_manhash = True
                continue
            if arg == '--release':
                on_release = True
                continue
            if arg in ('--help', '-h'):
                self.show_helpmes(self.manenv_os2, self.manenv_lang)
                exit(0)
            if arg == '--version':
                print(self.version)
                exit(0)
            if arg == '--listos':
                opt.listos = True
                break
            if arg == '--listman':
                opt.listman = True
                break
            if arg in listmandict.keys():
                setattr(opt, listmandict[arg], True)
                break
            if arg1 == '':
                arg1 = arg
                continue
            if arg2 == '':
                arg2 = arg
                continue
            errmes = 'Error: Invalid args option. [{0}]'.format(arg)
            print(errmes, file=sys.stderr)
            exit(1)
        vernamekey = opt.release if opt.release != '' else '@LATEST-RELEASE'
        if opt.listos:
            _main_man.show_listos(
                self.manenv_os2, self.manenv_lang, self.manenv_arch)
            exit(0)
        if opt.listman:
            _main_man.show_listman(
                vernamekey, self.manenv_os2, self.manenv_lang, self.manenv_arch)
        chklist: list = [False, opt.listman1, opt.listman2, opt.listman3, opt.listman4,
                         opt.listman5, opt.listman6, opt.listman7, opt.listman8, opt.listman9]
        if any(chklist):
            n: int = chklist.index(True)
            if 1 <= n <= 9:
                _main_man.show_listman_n(
                    n, vernamekey, self.manenv_os2, self.manenv_lang, self.manenv_arch)
            errmes = 'Error: Runtime Error. Invalid --listman[N]'
            print(errmes)
            exit(1)
        if arg2 == '':
            opt.manname = arg1  # e.g. args: ls
        else:
            opt.mannum = arg1  # e.g. args: 1 ls
            opt.manname = arg2
        roottomlobj = Man_roottoml()
        roottomlobj.og_vernamekey = vernamekey
        roottomlobj.og_manhashfpath = opt.manhashfpath
        roottomlobj.og_roottomlfpath = ''
        roottomlobj.og_manenv_os2 = self.manenv_os2
        roottomlobj.og_manenv_lang = self.manenv_lang
        roottomlobj.og_manenv_arch = self.manenv_arch
        tomldic = roottomlobj.make()
        mantomlobj = Man_mantoml()
        mantomlobj.og_tomldic = tomldic.copy()
        mantomlobj.og_osname_root = roottomlobj.osname
        mantomlobj.og_mannum = opt.mannum
        mantomlobj.og_manname = opt.manname
        mantomlobj.og_baseurls = roottomlobj.baseurls
        mantomlobj.og_fnamemode = 'hash'
        urlhashlist: typing.Final[list] = mantomlobj.make()
        if len(urlhashlist) == 0:
            errmes = 'Error: Not found the manual name. [{0}]'.format(
                opt.manname)
            print(errmes, file=sys.stderr)
            exit(1)
        s = ''
        for tpl in urlhashlist:
            pagerurl, hashdg = tpl
            s = _main_man.getstring_pagerurl(pagerurl, hashdg)
            if s != '':
                break
        if s == '':
            errmes = 'Error: Not found the url. [{0}]'.format(pagerurl)
            print(errmes, file=sys.stderr)
            exit(1)
        if sys.platform == 'darwin':
            s = unicodedata.normalize('NFD', s)
        elif sys.platform == 'win32':
            s = unicodedata.normalize('NFC', s)
        s = _main_man.norm_punctuation(s)
        pydoc.pager(s)
        print('OSNAME(man):', mantomlobj.osname)
        print(roottomlobj.message)
        exit(0)


class Main_mman(object):
    version: str = Main_manXXYY.version
    versiondate: str = Main_manXXYY.versiondate

    def show_helpmes(self):
        version: str = self.version
        versiondate: str = self.versiondate
        meses: typing.Final[list] =\
            ['mman written by MikeTurkey',
             'ver {0}, {1}'.format(version, versiondate),
             '2024 Copyright MikeTurkey ALL RIGHT RESERVED.',
             'ABSOLUTELY NO WARRANTY.',
             'Software: GPLv3 License including a prohibition clause for AI training.',
             '',
             'Summary',
             '  Multi-Language, Multi-Platform Man Pager',
             '  Choose your language.',
             '',
             'How to use.',
             '  1) Select your language and platform.',
             '     FreeBSD, English -> manenfb',
             '  2) Run manpage command.',
             '     $ python3.xx -m manenfb test',
             '     or',
             '     $ manenfb test',
             '  3) More Information.',
             '     $ python3.xx -m manenfb --help',
             '',
             'English:',
             '  manenfb: FreeBSD English man pager.',
             '  manenob: OpenBSD English man pager.',
             '',
             'Japanese:',
             '  manjpfb: FreeBSD Japanese man pager.',
             '']
        for s in meses:
            print(s)
        return

    def main(self):
        for arg in sys.argv[1:]:
            if arg == '--version':
                print(self.version)
                exit(0)
            if arg == '--help':
                break
        self.show_helpmes()
        exit(0)


def main_manenfb():
    cls = Main_manXXYY()
    cls.main(os2='fb', lang='eng', arch='arm64')
    return


def main_manjpfb():
    cls = Main_manXXYY()
    cls.main(os2='fb', lang='jpn', arch='arm64')
    return


def main_manenob():
    cls = Main_manXXYY()
    cls.main(os2='ob', lang='eng', arch='arm64')
    return


def main_mman():
    cls = Main_mman()
    cls.main()
    return


if __name__ == '__main__':
    main_mman()
    exit(0)
