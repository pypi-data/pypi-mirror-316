..
  Copyright 2024 Mike Turkey
  FreeBSD man documents were translated by MikeTurkey using Deep-Learning.
  contact: voice[ATmark]miketurkey.com
  license: GFDL1.3 License including a prohibition clause for AI training.
  
  Permission is granted to copy, distribute and/or modify this document
  under the terms of the GNU Free Documentation License, Version 1.3
  or any later version published by the Free Software Foundation;
  with no Invariant Sections, no Front-Cover Texts, and no Back-Cover Texts.
  A copy of the license is included in the section entitled "GNU
  Free Documentation License".
  See also
    GFDL1.3: https://www.gnu.org/licenses/fdl-1.3.txt
    Mike Turkey: https://miketurkey.com/
..

=================================
mman
=================================

  |  mman created by MikeTurkey
  |  Version 0.0.4, 21 Dec 2024
  |  2024, COPYRIGHT MikeTurkey, All Right Reserved.
  |  ABSOLUTELY NO WARRANTY.
  |  GPLv3 License including a prohibition clause for AI training.

Summary
---------------------------------

  | Multi-Language, Multi-Platform Man Pagers.
  | Choose your language.

Synopsis
--------------------------------

  | mman [ \--version | \--help ]
  | manXXYY [ \--version | \--help ]
  | manXXYY [ \--listos | \--listman]
  | manXXYY [MANNUM] [MANNAME] 
  |
  | note.

      | XX: Language, e.g. en(English), jp(Japanese)
      | YY: Platform, e.g. fb(FreeBSD), ob(OpenBSD)
      | e.g. manenfb, manenob ... 

Quick Start
--------------------------------

  Run on python pypi.

  .. code-block:: console

     $ python3.xx -m pip install mman
     $ python3.xx -m mman --help

       Select your language.
       e.g English, FreeBSD

     $ python3.xx -m manenfb test

How to use.
--------------------------------

  1) Select your language and platform.
   
     FreeBSD, English -> manenfb

  2) Run manpage command.

  .. code-block:: console
		   
     $ python3.xx -m manenfb test
     or
     $ manenfb test

  3) More Information.

  .. code-block:: console
		   
     $ python3.xx -m manenfb --help

  
Description
--------------------------------

  mman are Multi-Language, Multi-Platform pagers using Python3.
  The programs do not store man-data and download it with each request.
  Since they are Python scripts, they are expected to run on many Operating Systems in the future.
  We can read the mman on many Operating Systems.
  There is man-data that is not fully translated, but this is currently by design.
  Please note that I do not take full responsibility for the translation of the documents.

Languages
-------------------------------

English:

    | manenfb command: FreeBSD English man pager.
    | manenob command: OpenBSD English man pager.

Japanese:

    | manjpfb command: FreeBSD Japanese man pager.

Options(manXXYY)
-------------------------------

| \--version

  |   Show version and help page.

| \--listos

  |   Show the FreeBSD version name list of the manual.
  |   e.g. FreeBSD 13.2-Release

| \--listman

  |   Show the man list of the FreeBSD.
  |   e.g. ls, cp, rm, mv ... 

| \--listman1

  |   Show the man 1 list of the FreeBSD.
  |   man 1: General Commands Manual

| \--listman2

  |   Show the man 2 list of the FreeBSD.
  |   man 2: System Calls Manual

| \--listman3

  |   Show the man 3 list of the FreeBSD.
  |   man 3: Library Functions Manual

| \--listman4

  |   Show the man 4 list of the FreeBSD.
  |   man 4: Kernel Interfaces Manual

| \--listman5

  |   Show the man 5 list of the FreeBSD.
  |   man 5: File Formats Manual

| \--listman6

  |   Show the man 6 list of the FreeBSD.
  |   man 6: Games Manual

| \--listman7

  |   Show the man 7 list of the FreeBSD.
  |   man 7: Miscellaneous Information Manual

| \--listman8

  |   Show the man 8 list of the FreeBSD.
  |   man 8: System Manager's Manual

| \--listman9

  |   Show the man 9 list of the FreeBSD.
  |   man 9: Kernel Developer's Manual


Example
--------------------------------

.. code-block:: console
		
  $ manenfb ls
      print ls man.
  $ manenfb 1 head
      print head 1 section man.
  $ manenfb --version
      Show the message
  $ manenfb --listman
      Show man page list.
  $ manenfb --listos
      Show os name list of man.

要約
--------------------------------

  マルチ言語、マルチプラットフォーム マニュアルページャー


概要
---------------------------------

  mmanはpython3で動作するマルチ言語、マルチプラットフォームマニュアルページャーです。
  このプログラムはデータを保存せず、その都度ごとにダウンロードをします。
  pythonスクリプトで動作していることから、将来的には多くのOSで動作すれば良いと考えています。
  多くのオペレーティングシステムでこれらマニュアルを読めるようになります。
  マニュアルの中には完全に翻訳されていないものがありますが、現在のところ仕様です。
  ドキュメントの翻訳に全ての責任を負わないことに注意してください。
  
BUGS
------

  | Please report bugs to the issue tracker: https://github.com/MikeTurkey/mman/issues
  | or by e-mail: <voice[ATmark]miketurkey.com>
   
AUTHOR
------

  MikeTurkey <voice[ATmark]miketurkey.com>

LICENSE
----------

  GPLv3 License including a prohibition clause for AI training.

