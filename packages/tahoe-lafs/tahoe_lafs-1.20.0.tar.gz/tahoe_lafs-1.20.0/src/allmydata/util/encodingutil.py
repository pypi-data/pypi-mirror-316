"""
Functions used to convert inputs from whatever encoding used in the system to
unicode and back.

Ported to Python 3.

Once Python 2 support is dropped, most of this module will obsolete, since
Unicode is the default everywhere in Python 3.
"""

from six import ensure_str

import sys, os, re
import unicodedata
import warnings

from allmydata.util.assertutil import precondition, _assert
from twisted.python import usage
from twisted.python.filepath import FilePath
from allmydata.util import log
from allmydata.util.fileutil import abspath_expanduser_unicode

NoneType = type(None)


def canonical_encoding(encoding):
    if encoding is None:
        log.msg("Warning: falling back to UTF-8 encoding.", level=log.WEIRD)
        encoding = 'utf-8'
    encoding = encoding.lower()
    if encoding == "cp65001":
        encoding = 'utf-8'
    elif encoding == "us-ascii" or encoding == "646" or encoding == "ansi_x3.4-1968":
        encoding = 'ascii'

    return encoding

def check_encoding(encoding):
    # sometimes Python returns an encoding name that it doesn't support for conversion
    # fail early if this happens
    try:
        u"test".encode(encoding)
    except (LookupError, AttributeError):
        raise AssertionError(
            "The character encoding '%s' is not supported for conversion." % (encoding,),
        )

# On Windows we install UTF-8 stream wrappers for sys.stdout and
# sys.stderr, and reencode the arguments as UTF-8 (see scripts/runner.py).
#
# On POSIX, we are moving towards a UTF-8-everything and ignore the locale.
io_encoding = "utf-8"

filesystem_encoding = None

def _reload():
    global filesystem_encoding
    filesystem_encoding = canonical_encoding(sys.getfilesystemencoding())
    check_encoding(filesystem_encoding)

_reload()


def get_filesystem_encoding():
    """
    Returns expected encoding for local filenames.
    """
    return filesystem_encoding

def get_io_encoding():
    """
    Returns expected encoding for writing to stdout or stderr, and for arguments in sys.argv.
    """
    return io_encoding

def argv_to_unicode(s):
    """
    Decode given argv element to unicode. If this fails, raise a UsageError.

    This is the inverse of ``unicode_to_argv``.
    """
    if isinstance(s, str):
        return s

    precondition(isinstance(s, bytes), s)

    try:
        return str(s, io_encoding)
    except UnicodeDecodeError:
        raise usage.UsageError("Argument %s cannot be decoded as %s." %
                               (quote_output(s), io_encoding))

def argv_to_abspath(s, **kwargs):
    """
    Convenience function to decode an argv element to an absolute path, with ~ expanded.
    If this fails, raise a UsageError.
    """
    decoded = argv_to_unicode(s)
    if decoded.startswith(u'-'):
        raise usage.UsageError("Path argument %s cannot start with '-'.\nUse %s if you intended to refer to a file."
                               % (quote_output(s), quote_output(os.path.join('.', s))))
    return abspath_expanduser_unicode(decoded, **kwargs)


def unicode_to_argv(s):
    """
    Make the given unicode string suitable for use in an argv list.

    On Python 2 on POSIX, this encodes using UTF-8.  On Python 3 and on
    Windows, this returns the input unmodified.
    """
    precondition(isinstance(s, str), s)
    warnings.warn("This is unnecessary.", DeprecationWarning)
    if sys.platform == "win32":
        return s
    return ensure_str(s)


# According to unicode_to_argv above, the expected type for
# cli args depends on the platform, so capture that expectation.
argv_type = (str,)
"""
The expected type for args to a subprocess
"""


def unicode_to_url(s):
    """
    Encode an unicode object used in an URL to bytes.
    """
    # According to RFC 2718, non-ascii characters in URLs must be UTF-8 encoded.

    # FIXME
    return to_bytes(s)
    #precondition(isinstance(s, unicode), s)
    #return s.encode('utf-8')

def to_bytes(s):
    """Convert unicode to bytes.

    None and bytes are passed through unchanged.
    """
    if s is None or isinstance(s, bytes):
        return s
    return s.encode('utf-8')

def from_utf8_or_none(s):
    precondition(isinstance(s, bytes) or s is None, s)
    if s is None:
        return s
    return s.decode('utf-8')

PRINTABLE_ASCII = re.compile(br'^[\n\r\x20-\x7E]*$',          re.DOTALL)
PRINTABLE_8BIT  = re.compile(br'^[\n\r\x20-\x7E\x80-\xFF]*$', re.DOTALL)

def is_printable_ascii(s):
    return PRINTABLE_ASCII.search(s) is not None

def unicode_to_output(s):
    """
    Encode an unicode object for representation on stdout or stderr.

    On Python 3 just returns the unicode string unchanged, since encoding is
    the responsibility of stdout/stderr, they expect Unicode by default.
    """
    precondition(isinstance(s, str), s)
    warnings.warn("This is unnecessary.", DeprecationWarning)
    return s

def _unicode_escape(m, quote_newlines):
    u = m.group(0)
    if u == u'"' or u == u'$' or u == u'`' or u == u'\\':
        return u'\\' + u
    elif u == u'\n' and not quote_newlines:
        return u
    if len(u) == 2:
        codepoint = (ord(u[0])-0xD800)*0x400 + ord(u[1])-0xDC00 + 0x10000
    else:
        codepoint = ord(u)
    if codepoint > 0xFFFF:
        return u'\\U%08x' % (codepoint,)
    elif codepoint > 0xFF:
        return u'\\u%04x' % (codepoint,)
    else:
        return u'\\x%02x' % (codepoint,)

def _bytes_escape(m, quote_newlines):
    """
    Takes a re match on bytes, the result is escaped bytes of group(0).
    """
    c = m.group(0)
    if c == b'"' or c == b'$' or c == b'`' or c == b'\\':
        return b'\\' + c
    elif c == b'\n' and not quote_newlines:
        return c
    else:
        return b'\\x%02x' % (ord(c),)

MUST_DOUBLE_QUOTE_NL = re.compile(u'[^\\x20-\\x26\\x28-\\x7E\u00A0-\uD7FF\uE000-\uFDCF\uFDF0-\uFFFC]', re.DOTALL)
MUST_DOUBLE_QUOTE    = re.compile(u'[^\\n\\x20-\\x26\\x28-\\x7E\u00A0-\uD7FF\uE000-\uFDCF\uFDF0-\uFFFC]', re.DOTALL)

# if we must double-quote, then we have to escape ", $ and `, but need not escape '
ESCAPABLE_UNICODE = re.compile(u'([\uD800-\uDBFF][\uDC00-\uDFFF])|'  # valid surrogate pairs
                               u'[^ !#\\x25-\\x5B\\x5D-\\x5F\\x61-\\x7E\u00A0-\uD7FF\uE000-\uFDCF\uFDF0-\uFFFC]',
                               re.DOTALL)

ESCAPABLE_8BIT    = re.compile( br'[^ !#\x25-\x5B\x5D-\x5F\x61-\x7E]', re.DOTALL)

def quote_output_u(*args, **kwargs):
    """
    Like ``quote_output`` but always return ``unicode``.
    """
    result = quote_output(*args, **kwargs)
    if isinstance(result, str):
        return result
    # Since we're quoting, the assumption is this will be read by a human, and
    # therefore printed, so stdout's encoding is the plausible one. io_encoding
    # is now always utf-8.
    return result.decode(kwargs.get("encoding", None) or
                         getattr(sys.stdout, "encoding") or io_encoding)


def quote_output(s, quotemarks=True, quote_newlines=None, encoding=None):
    """
    Encode either a Unicode string or a UTF-8-encoded bytestring for representation
    on stdout or stderr, tolerating errors. If 'quotemarks' is True, the string is
    always quoted; otherwise, it is quoted only if necessary to avoid ambiguity or
    control bytes in the output. (Newlines are counted as control bytes iff
    quote_newlines is True.)

    Quoting may use either single or double quotes. Within single quotes, all
    characters stand for themselves, and ' will not appear. Within double quotes,
    Python-compatible backslash escaping is used.

    If not explicitly given, quote_newlines is True when quotemarks is True.

    On Python 3, returns Unicode strings.
    """
    precondition(isinstance(s, (bytes, str)), s)
    # Since we're quoting, the assumption is this will be read by a human, and
    # therefore printed, so stdout's encoding is the plausible one. io_encoding
    # is now always utf-8.
    encoding = encoding or getattr(sys.stdout, "encoding") or io_encoding

    if quote_newlines is None:
        quote_newlines = quotemarks

    def _encode(s):
        if isinstance(s, bytes):
            try:
                s = s.decode("utf-8")
            except UnicodeDecodeError:
                return b'b"%s"' % (ESCAPABLE_8BIT.sub(lambda m: _bytes_escape(m, quote_newlines), s),)

        must_double_quote = quote_newlines and MUST_DOUBLE_QUOTE_NL or MUST_DOUBLE_QUOTE
        if must_double_quote.search(s) is None:
            try:
                out = s.encode(encoding)
                if quotemarks or out.startswith(b'"'):
                    return b"'%s'" % (out,)
                else:
                    return out
            except (UnicodeDecodeError, UnicodeEncodeError):
                pass

        escaped = ESCAPABLE_UNICODE.sub(lambda m: _unicode_escape(m, quote_newlines), s)
        return b'"%s"' % (escaped.encode(encoding, 'backslashreplace'),)

    result = _encode(s)
    result = result.decode(encoding)
    return result


def quote_path(path, quotemarks=True):
    return quote_output(b"/".join(map(to_bytes, path)), quotemarks=quotemarks, quote_newlines=True)

def quote_local_unicode_path(path, quotemarks=True):
    precondition(isinstance(path, str), path)

    if sys.platform == "win32" and path.startswith(u"\\\\?\\"):
        path = path[4 :]
        if path.startswith(u"UNC\\"):
            path = u"\\\\" + path[4 :]

    return quote_output(path, quotemarks=quotemarks, quote_newlines=True)

def quote_filepath(path, quotemarks=True):
    return quote_local_unicode_path(unicode_from_filepath(path), quotemarks=quotemarks)

def extend_filepath(fp, segments):
    # We cannot use FilePath.preauthChild, because
    # * it has the security flaw described in <https://twistedmatrix.com/trac/ticket/6527>;
    # * it may return a FilePath in the wrong mode.

    for segment in segments:
        fp = fp.child(segment)

    return fp

def to_filepath(path):
    precondition(isinstance(path, str), path=path)

    if sys.platform == "win32":
        _assert(isinstance(path, str), path=path)
        if path.startswith(u"\\\\?\\") and len(path) > 4:
            # FilePath normally strips trailing path separators, but not in this case.
            path = path.rstrip(u"\\")

    return FilePath(path)

def _decode(s):
    precondition(isinstance(s, (bytes, str)), s=s)

    if isinstance(s, bytes):
        return s.decode(filesystem_encoding)
    else:
        return s

def unicode_from_filepath(fp):
    precondition(isinstance(fp, FilePath), fp=fp)
    return _decode(fp.path)

def unicode_segments_from(base_fp, ancestor_fp):
    precondition(isinstance(base_fp, FilePath), base_fp=base_fp)
    precondition(isinstance(ancestor_fp, FilePath), ancestor_fp=ancestor_fp)

    return base_fp.asTextMode().segmentsFrom(ancestor_fp.asTextMode())

def unicode_platform():
    """
    Does the current platform handle Unicode filenames natively?
    """
    return True

class FilenameEncodingError(Exception):
    """
    Filename cannot be encoded using the current encoding of your filesystem
    (%s). Please configure your locale correctly or rename this file.
    """
    pass

def listdir_unicode(path):
    """
    Wrapper around listdir() which provides safe access to the convenient
    Unicode API even under platforms that don't provide one natively.
    """
    precondition(isinstance(path, str), path)
    return os.listdir(path)

def listdir_filepath(fp):
    return listdir_unicode(unicode_from_filepath(fp))


# 'x' at the end of a variable name indicates that it holds a Unicode string that may not
# be NFC-normalized.
def normalize(namex):
    return unicodedata.normalize('NFC', namex)
