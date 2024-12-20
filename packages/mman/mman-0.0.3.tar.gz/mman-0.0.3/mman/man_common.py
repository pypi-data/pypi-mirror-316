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
import urllib.request
import tomllib


class Mainfunc(object):
    @staticmethod
    def geturlpath_man(rootdic: dict, vernamekey: str) -> tuple:
        mainfunc = Mainfunc
        errmes: str
        if vernamekey == '@LATEST-RELEASE':
            timelist = list()  # list of tuple [ (release date(epoch), url) ]
            for tpl in mainfunc.iter_rootdic(rootdic):
                vername, osname, status, thedate, urls = tpl
                t = time.strptime(thedate, '%Y%m%d-%H%M%S')
                epoch = int(time.mktime(t))
                timelist.append(
                    (epoch, urls, osname, status, thedate, vername))
            if len(timelist) == 0:
                errmes = 'Error: Unable to analyze root.toml.'
                print(errmes, file=sys.stderr)
                exit(1)
            timelist.append((10000, 'example.com', 'Example OS'))
            timelist.sort(key=lambda x: x[0], reverse=True)
            rettpl: tuple = timelist[0][1:]
            return rettpl
        matched: bool = False
        for tpl in mainfunc.iter_rootdic(rootdic):
            vername, osname, status, thedate, urls = tpl
            if vername == vernamekey:
                matched = True
                break  # End of loop
        if matched == False:
            return ('', '', '', '', [])
        return tpl  # (Matched URL, osname)

    @staticmethod
    def iter_rootdic(rootdic: dict):
        vername: str
        s: str
        osname: str
        status: str
        thedate: str
        urls: list = list()
        errmes: str
        chklist: list
        vname: str
        for vername, d in rootdic.items():
            if vername in ('baseurls', 'message'):
                continue
            if d.get('status') != 'release':
                continue  # Not 'release' status.
            if d.get('url') != None:
                s = d.get('url')
                if isinstance(s, str) != True:
                    errmes = 'Error: url value on root.toml is NOT string.'
                    print(errmes, file=sys.stderr)
                    exit(1)
                urls.append(s)
            osname = d.get('osname')
            status = d.get('status')
            thedate = d.get('thedate')
            if isinstance(d.get('urls'), list):
                urls.extend(d.get('urls'))
            chklist = [('osname', osname), ('status', status),
                       ('thedate', thedate)]
            for vname, v in chklist:
                if isinstance(v, str) != True:
                    errmes = 'Error: {0} on root.toml is NOT string.'.format(
                        vname)
                    print(errmes, file=sys.stderr)
                    exit(1)
            if isinstance(urls, list) != True:
                errmes = 'Error: urls on root.toml is NOT list type.'
                print(errmes, file=sys.stderr)
                exit(1)
            yield (vername, osname, status, thedate, urls)
        return

    @staticmethod
    def loadbytes_url(urlpath: str, exception: bool = True) -> bytes:
        if exception:
            try:
                with urllib.request.urlopen(urlpath) as response:
                    html_content: bytes = response.read()
            except urllib.error.URLError as e:
                errmes = 'Error: URL Error. {0}, URL: {1}'.format(e, urlpath)
                print(errmes, file=sys.stderr)
                exit(1)
            except urllib.error.HTTPError as e:
                errmes = 'Error: HTTP Error. {0}, URL: {1}'.format(e, urlpath)
                print(errmes, file=sys.stderr)
                exit(1)
            except Exception as e:
                errmes = 'Error: Runtime Error. {0}, URL: {1}'.format(
                    e, urlpath)
                print(errmes, file=sys.stderr)
                exit(1)
            b: bytes = html_content
            return b
        else:
            html_content: bytes = b''
            try:
                with urllib.request.urlopen(urlpath) as response:
                    html_content: bytes = response.read()
            except:
                pass
            return html_content

    @staticmethod
    def loadstring_url(urlpath: str) -> str:
        try:
            with urllib.request.urlopen(urlpath) as response:
                html_content = response.read().decode("utf-8")
        except urllib.error.URLError as e:
            errmes = 'Error: URL Error. {0}, URL: {1}'.format(e, urlpath)
            print(errmes, file=sys.stderr)
            exit(1)
        except urllib.error.HTTPError as e:
            errmes = 'Error: HTTP Error. {0}, URL: {1}'.format(e, urlpath)
            print(errmes, file=sys.stderr)
            exit(1)
        except Exception as e:
            errmes = 'Error: Runtime Error. {0}, URL: {1}'.format(e, urlpath)
            print(errmes, file=sys.stderr)
            exit(1)
        s = html_content
        return s

    @staticmethod
    def normurl(url: str) -> str:
        if '://' not in url:
            errmes = 'Error: Not url. [{0}]'.format(url)
            print(errmes, file=sys.stderr)
            exit(1)
        splitted = url.split('://', 1)
        ptn = r'/+'
        tail = re.sub(ptn, '/', splitted[1])
        retstr = splitted[0] + '://' + tail
        return retstr
