""" itu_appendix42
Copyright (C) 2024 Martin J Levy - W6LHI/G8LHI - @mahtin - https://github.com/mahtin
"""

# Table of International Call Sign Series (Appendix 42 to the RR)

# Based on this page ...
#     https://www.itu.int/en/ITU-R/terrestrial/fmd/Pages/glad.aspx
# Visit the following page ...
#     https://www.itu.int/en/ITU-R/terrestrial/fmd/Pages/call_sign_series.aspx
# Download via the .xlsx button and produce a file like this ...
#     CallSignSeriesRanges-998049b7-c007-4e71-bac6-d2393eaa83ef.xlsx
#     CallSignSeriesRanges-c3ce6efb-d36c-4e44-8fff-083b4aab1c09.xlsx
# The following code looks for the newest file of that name pattern in your Download's directory.
# Under windows that's C:\Users\YourUsername\Downloads\, under Linux or MacOS it's ~/Downloads
#
# See README

import sys
import re
from os import makedirs
from os.path import join, expanduser, getmtime, isdir, exists
import json

from string import ascii_uppercase, digits

from itu_appendix42.iso3661_mapping import iso3661_mapping
from itu_appendix42.iso3661_mapping_from_itu import iso3661_mapping_from_itu
from itu_appendix42.worksheet import ItuAppendix42Worksheet, ItuAppendix42WorksheetError
from itu_appendix42.log import ItuAppendix42Logger

class ItuAppendix42Error(Exception):
    """ raise this any ItuAppendix42 error """

class ItuAppendix42():
    """ ItuAppendix42 """

    DOWNLOAD_FOLDER = 'Downloads'
    FILENAME_PATTERN = 'CallSignSeriesRanges-*-*-*-*.xlsx'
    PACKAGE_RESOURCES = 'itu_appendix42.resources'

    CACHE_FOLDER = '.cache'
    CACHE_SUBFOLDER = 'itu_appendix42'
    CACHE_FILENAME = 'itu_appendix42.regex'

    _forward = None
    _reverse = None
    __prefix_regex = None
    __prefix_regex_c = None
    _regex = None
    _regex_c = None

    _verbose = False
    _log = None

    def __init__(self, force=False, verbose=False):
        """ __init__ """

        self.__class__._verbose = verbose

        if not self.__class__._log:
            self.__class__._log = ItuAppendix42Logger(verbose).getLogger()

        if force:
            self.__class__._log.info('force rebuild')

        if not force:
            # grab cached regex, etc if we can
            try:
                a, b, c, regex_mtime = self.__class__._read_cache_files()
                self.__class__._regex = a
                self.__class__._prefix_regex = b
                self.__class__._forward = c
            except ItuAppendix42Error:
                pass

        if self.__class__._regex and self.__class__._prefix_regex and self.__class__._forward:
            # cached regex found - yippee!
            self.__class__._log.info('using cache values for regex')
            return

        # cached regex missing (no biggie) - read in the worksheet(s) and build it manually

        # read in a fresh version of the worksheet
        try:
            worksheet = ItuAppendix42Worksheet(self.__class__._log)
            values = worksheet.read_sheet()
        except ItuAppendix42WorksheetError as e:
            self.__class__._log.warning('no worksheet to read in - aborting: %s', e)
            raise ItuAppendix42Error from None

        # forward mapping build first
        self.__class__._forward = self.__class__._build_forward(values)

        # regex build time
        if not self.__class__._regex or not self.__class__._prefix_regex:
            self.__class__._build_regex_and_prefix_regex()

        # save a local version away in users cache for next run
        self.__class__._write_cache_files()

    def prefix_regex(self):
        """ prefix_regex """
        return self.__class__._prefix_regex

    def prefix_regex_c(self):
        """ prefix_regex_c """
        if not self.__class__._prefix_regex_c:
            # prefix_regex compile time
            self.__class__._prefix_regex_c = re.compile(self.__class__._prefix_regex, re.ASCII|re.IGNORECASE)

        return self.__class__._prefix_regex_c

    def regex(self):
        """ regex """
        return self.__class__._regex

    def regex_c(self):
        """ regex_c """
        if not self.__class__._regex_c:
            # regex compile time
            self.__class__._regex_c = re.compile(self.__class__._regex, re.ASCII|re.IGNORECASE)

        return self.__class__._regex_c

    def forward(self):
        """ forward """
        return self.__class__._forward

    def reverse(self):
        """ reverse """
        # we build a reverse maping as we need it
        if not self.__class__._reverse:
            self.__class__._reverse = self.__class__._build_reverse()
        return self.__class__._reverse

    def dump(self):
        """ dump """
        results = []
        for k in self.__class__._forward:
            callsign = k
            if callsign[-5:] == '[A-Z]':
                callsign = callsign[:-5]
            if callsign[-5:] == '[A-Z]':
                callsign = callsign[:-5]
            country = self.__class__._forward[k]
            results += ['%-10s %2s : %s' % (callsign, country['cc'], country['name'])]
        return '\n'.join(sorted(results))

    def rdump(self):
        """ rdump """
        # can only dump if we have worksheets - ignore force flag - TODO optimize this!
        # we build a reverse maping as we need it
        if not self.__class__._reverse:
            self.__class__._reverse = self.__class__._build_reverse()
        results = []
        for k in sorted(self.__class__._reverse):
            results += ['%-10s %-40s : %s' % (k, ' '.join(self.__class__._reverse[k]['prefix']), self.__class__._reverse[k]['name'])]
        return '\n'.join(sorted(results))

    def match(self, line):
        """ match """
        if not self.__class__._regex_c:
            # regex compile time
            self.__class__._regex_c = re.compile(self.__class__._regex, re.ASCII|re.IGNORECASE)
        return self.__class__._regex_c.match(line.upper())

    def fullmatch(self, line):
        """ fullmatch """
        if not self.__class__._regex_c:
            # regex compile time
            self.__class__._regex_c = re.compile(self.__class__._regex, re.ASCII|re.IGNORECASE)
        return self.__class__._regex_c.fullmatch(line.upper())

    def findall(self, line):
        """ findall """
        if not self.__class__._regex_c:
            # regex compile time
            self.__class__._regex_c = re.compile(self.__class__._regex, re.ASCII|re.IGNORECASE)
        return [''.join(v) for v in self.__class__._regex_c.findall(line.upper())]

    def prefix_match(self, line):
        """ prefix_match """
        if not self.__class__._prefix_regex_c:
            # prefix_regex compile time
            self.__class__._prefix_regex_c = re.compile(self.__class__._prefix_regex, re.ASCII|re.IGNORECASE)
        return self.__class__._prefix_regex_c.match(line.upper())

    def prefix_fullmatch(self, line):
        """ prefix_fullmatch """
        if not self.__class__._prefix_regex_c:
            # prefix_regex compile time
            self.__class__._prefix_regex_c = re.compile(self.__class__._prefix_regex, re.ASCII|re.IGNORECASE)
        return self.__class__._prefix_regex_c.fullmatch(line.upper())

    def prefix_findall(self, line):
        """ prefix_findall """
        if not self.__class__._prefix_regex_c:
            # prefix_regex compile time
            self.__class__._prefix_regex_c = re.compile(self.__class__._prefix_regex, re.ASCII|re.IGNORECASE)
        return [''.join(v) for v in self.__class__._prefix_regex_c.findall(line.upper())]

    @classmethod
    def _build_forward(cls, values):
        """ _build_forward """

        def _optimize_callsign(callsign_series):
            """ _optimize_callsign """
            # ['5XA - 5XZ']
            callsign_low, callsign_high = callsign_series.split(' - ')
            # each is three char's long

            if callsign_low[2] == 'A' and callsign_high[2] == 'Z':
                if callsign_low[0:2] == callsign_high[0:2]:
                    return callsign_low[0:2] + '[A-Z]'
                if callsign_low[1] == 'A' and callsign_high[1] == 'Z' and callsign_low[0:1] == callsign_high[0:1]:
                    return callsign_low[0:1] + '[A-Z][A-Z]'
                if callsign_low[1] == '0' and callsign_high[1] == '9' and callsign_low[0:1] == callsign_high[0:1]:
                    return callsign_low[0:1] + '[0-9][A-Z]'

            # For Egypt, Fiji, etc there could be an A-M & N-Z split on the third letter!
            if callsign_low[2] == 'A' and callsign_high[2] == 'M' and callsign_low[0:2] == callsign_high[0:2]:
                if callsign_low[0:2] == callsign_high[0:2]:
                    return callsign_low[0:2] + '[A-M]'

            if callsign_low[2] == 'N' and callsign_high[2] == 'Z' and callsign_low[0:2] == callsign_high[0:2]:
                if callsign_low[0:2] == callsign_high[0:2]:
                    return callsign_low[0:2] + '[N-Z]'

            # return callsign_series using its orginal values - no optimize available
            return callsign_low + ' - ' + callsign_high

        forward = {}
        for v in values:
            callsign = v[0]
            country = v[1]
            callsign = _optimize_callsign(callsign)
            if country in iso3661_mapping_from_itu:
                cc = iso3661_mapping_from_itu[country]['iso3661']
                country_name = iso3661_mapping_from_itu[country]['iso3661_name']
            else:
                cc = '??'
                country_name = country
            forward[callsign] = {'cc': cc, 'name': country}

        # Further processing reduces this data using regex definition methods
        return cls._optimize_duplicates(forward)

    @classmethod
    def _optimize_duplicates(cls, forward):
        """ _optimize_duplicates """

        def dedup(letter_1, letter_2_begin, letter_2_end, present_country):
            """ dedup """
            letter_2 = letter_2_begin
            while letter_2 <= letter_2_end:
                callsign = letter_1 + letter_2 + '[A-Z]'
                del forward[callsign]
                letter_2 = chr(ord(letter_2) + 1)
            if letter_2_begin == letter_2_end:
                letter_range = letter_2_begin
            else:
                letter_range = '[%s-%s]' % (letter_2_begin, letter_2_end)
            callsign = letter_1 + letter_range + '[A-Z]'
            forward[callsign] = present_country

        # now look for second letter sequences
        for letter_1 in sorted(set([v[0:1] for v in forward])):
            for seq in [digits, ascii_uppercase]:
                present_country = None
                letter_2_begin = None
                letter_2_end = None
                for letter_2 in seq:
                    callsign = letter_1 + letter_2 + '[A-Z]'
                    if callsign not in forward:
                        # quite common - this is a non allocated letter sequence
                        if present_country:
                            dedup(letter_1, letter_2_begin, letter_2_end, present_country)
                        present_country = None
                        letter_2_begin = None
                        letter_2_end = None
                        continue
                    if not present_country:
                        # first find of country
                        present_country = forward[callsign]
                        letter_2_begin = letter_2
                        letter_2_end = letter_2
                        continue
                    if present_country != forward[callsign]:
                        # changed country
                        dedup(letter_1, letter_2_begin, letter_2_end, present_country)
                        present_country = forward[callsign]
                        letter_2_begin = letter_2
                        letter_2_end = letter_2
                        continue
                    # continuing country
                    letter_2_end = letter_2

                if present_country:
                    dedup(letter_1, letter_2_begin, letter_2_end, present_country)
                    present_country = None
                    letter_2_begin = None
                    letter_2_end = None

        return forward

    @classmethod
    def _build_reverse(cls):
        """_build_reverse """
        reverse = {}
        for k in cls._forward:
            callsign = k
            if callsign[-5:] == '[A-Z]':
                callsign = callsign[:-5]
            if callsign[-5:] == '[A-Z]':
                callsign = callsign[:-5]
            country = cls._forward[k]
            cc = country['cc']
            if cc not in reverse:
                reverse[cc] = {'name': country['name'], 'prefix': []}
            reverse[cc]['prefix'].append(callsign)
        return reverse

    @classmethod
    def _build_regex_and_prefix_regex(cls):
        """ _build_regex_and_prefix_regex """

        def expand(s):
            """ expand """
            if len(s) != 3:
                return s
            begin = s[0]
            end = s[2]
            s = ''
            c = begin
            while c <= end:
                s += c
                c = chr(ord(c) + 1)
            return s

        one_letter_alpha = '[' + ''.join(sorted([v[0:1] for v in cls._forward if v[0].isalpha() and v[-10:] == '[A-Z][A-Z]'])) + ']'
        one_letter_numeric = '[' + ''.join(sorted([v[0:1] for v in cls._forward if v[0].isnumeric() and v[-10:] == '[A-Z][A-Z]'])) + ']'

        if len(one_letter_alpha) == 3:
            one_letter_alpha = one_letter_alpha[1]
        if len(one_letter_numeric) == 3:
            one_letter_numeric = one_letter_numeric[1]

        two_letters = []
        twos = sorted([v[0:2] for v in cls._forward if v[-10:] != '[A-Z][A-Z]' and v[-5:] in ['[A-Z]', '[A-M]', '[N-Z]']])
        for letter_1 in sorted(set([v[0:1] for v in twos])):
            step1 = sorted([v[1:-5] for v in cls._forward if v[0] == letter_1 and v[-5:] == '[A-Z]'])
            step2 = [v[0] for v in step1 if len(v) == 1]
            step3 = [expand(v[1:4]) for v in step1 if len(v) != 1]
            step4 = ''.join(sorted(step2 + step3))
            # The following is in a specific order
            # While this could (and should) be better code, there's only some very specific patterns in-use presently
            swaps = [
                ['ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'A-Z'],
                ['ABCDEFGHIJKLMNOPQRSTUVWXY', 'A-Y'],
                ['ABCDEFGHIJKLMNOPQRTUVWXYZ', 'A-RT-Z'],
                ['ABCDEFGHIJKLMOPQRSTUVWXYZ', 'A-MO-Z'],
                ['ABCEFGHIJKLMNOPQRSTUVWXYZ', 'A-CE-Z'],
                ['23456789', '2-9'],
                ['2345678', '2-8'],
                ['234567', '2-7'],
                ['2346789', '2-46-9'],
                ['2356789', '2-35-9'],
            ]
            for swap in swaps:
                step4 = step4.replace(swap[0], swap[1])
            two_letter = letter_1 + '[' + step4 + ']'
            two_letters.append(two_letter)

        # there's further optimization that can be done.

        two_letters_split = [(v[0], v[1:]) for v in two_letters]

        two_letters_sorted = {}
        for v in two_letters:
            a = v[0]
            b = v[1:]
            if b in two_letters_sorted:
                two_letters_sorted[b].append(a)
            else:
                two_letters_sorted[b] = [a]

        two_letters = []
        for k,v in two_letters_sorted.items():
            a = ''.join(v)
            if len(a) > 1:
                a = '[' + a + ']'
            two_letters.append(a + k)

        three_letters = sorted([v for v in cls._forward if v[-10:] != '[A-Z][A-Z]' and v[-5:] not in ['[A-Z]', '[A-M]', '[N-Z]']])

        # split these three patterns because we need to know the ones with numbers in the second position need a different pattern format

        two_letters_has_numeric = []
        two_letters_only_alpha = []
        for element in two_letters:
            a = element.split('[')
            if a[0] == '':
                del a[0]
            b = [v for v in a[1] if v.isnumeric()]
            if len(b) > 0:
                two_letters_has_numeric.append(element)
            else:
                two_letters_only_alpha.append(element)

        # Only found 56789 to optimize - but wrote more generic code anyway
        for ii in range(len(two_letters_has_numeric)):
            swaps = [
                ['56789', '5-9'],
            ]
            for swap in swaps:
                two_letters_has_numeric[ii] = two_letters_has_numeric[ii].replace(swap[0], swap[1])

        for ii in range(len(two_letters_only_alpha)):
            swaps = [
                ['56789', '5-9'],
            ]
            for swap in swaps:
                two_letters_only_alpha[ii] = two_letters_only_alpha[ii].replace(swap[0], swap[1])

        # we combine these three patterns. we add the missing letters. We take care of the numbers carefully

        prefix1_letters = [one_letter_numeric + '[A-Z]{1,2}'] + \
                          [one_letter_alpha + '[A-Z]{0,2}'] + \
                          [v + '[A-Z]{0,1}' for v in two_letters_only_alpha] + \
                          three_letters

        prefix2_letters = [v + '[A-Z]{0,1}' for v in two_letters_has_numeric]

        cls._regex = '(' + \
                        '(' + '|'.join(prefix1_letters) + ')(' + '[0-9][0-9A-Z]{0,3}[A-Z]' + ')' + \
                     '|' + \
                        '(' + '|'.join(prefix2_letters) + ')(' + '[0-9A-Z]{0,3}[A-Z]' + ')' + \
                     ')'

        cls._prefix_regex = '(' + '|'.join(prefix1_letters + prefix2_letters) + ')'

        cls._log.info('_regex: %s ...', cls._regex[:100])
        cls._log.info('_prefix_regex: %s ...', cls._prefix_regex[:100])

    @classmethod
    def _version(cls):
        """ _version """
        # this is a delayed runtime import to stop any recursion
        from . import __version__
        return str(__version__)

    @classmethod
    def _find_cache_file(cls):
        """ _find_cache_file """
        cache_file_folder = join(expanduser('~'), cls.CACHE_FOLDER , cls.CACHE_SUBFOLDER)
        if not isdir(cache_file_folder):
            cls._log.info('mkdir %s', cache_file_folder)
            try:
                makedirs(cache_file_folder)
            except OSError as e:
                cls._log.warning('%s: %s', cache_file_folder, e)
                raise ItuAppendix42Error from None
        cache_file = join(cache_file_folder, cls.CACHE_FILENAME)
        cls._log.info('cache file is %s', cache_file)
        return cache_file

    @classmethod
    def _write_cache_files(cls):
        """ _write_cache_files """

        cls._log.info('writing cache values')
        try:
            filename = cls._find_cache_file()
        except ItuAppendix42Error:
            return

        try:
            fd = open(filename, 'w', encoding='utf-8')
        except OSError as e:
            cls._log.warning('%s: %s', filename, e)
            return

        fd.write(cls._version())
        fd.write('\n')
        fd.write(cls._regex)
        fd.write('\n')
        fd.write(cls._prefix_regex)
        fd.write('\n')
        fd.write(json.dumps(cls._forward))
        fd.write('\n')

    @classmethod
    def _read_cache_files(cls):
        """ _read_cache_files """

        # Format:
        # release version number
        # regex
        # prefix_regex
        # forward (in json format)

        try:
            filename = cls._find_cache_file()
        except ItuAppendix42Error:
            raise ItuAppendix42Error from None

        try:
            file_mtime = getmtime(filename)
        except OSError as e:
            cls._log.warning('%s: %s', filename, e)
            # no file - so we create it later
            raise ItuAppendix42Error from None

        try:
            fd = open(filename, 'r', encoding='utf-8')
        except OSError as e:
            # no file - so we create it later
            cls._log.warning('%s: %s', filename, e)
            raise ItuAppendix42Error from None

        first_line = fd.readline().strip()
        if len(first_line) == 0:
            # zero length file - no idea why
            cls._log.warning('%s: first line zero length', filename)
            raise ItuAppendix42Error from None
        if first_line != cls._version():
            # old file from previous version - needs updating
            cls._log.warning('%s: version mismatch (old=%s new=%s) - new cache file will be created', filename, first_line, cls._version())
            raise ItuAppendix42Error from None

        regex = fd.readline().strip()
        prefix_regex = fd.readline().strip()
        if len(regex) == 0 or len(prefix_regex) == 0:
            cls._log.warning('%s: second and third line zero length', filename)
            raise ItuAppendix42Error from None

        forth_line = fd.readline().strip()
        if len(forth_line) == 0 or len(forth_line) == 0:
            cls._log.warning('%s: forth line zero length', filename)
            raise ItuAppendix42Error from None

        try:
            forward = json.loads(forth_line)
        except json.decoder.JSONDecodeError:
            cls._log.warning('%s: forth line json failure', filename)
            raise ItuAppendix42Error from None

        cls._log.debug('regex: %s ...', regex[:100])
        cls._log.debug('prefix_regex: %s ...', prefix_regex[:100])
        cls._log.debug('len(forward): %d', len(forward))

        return regex, prefix_regex, forward, file_mtime
