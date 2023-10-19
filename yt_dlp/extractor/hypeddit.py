from .common import InfoExtractor
from ..networking import HEADRequest, Request

from ..utils import (
    error_to_compat_str,
    ExtractorError,
    float_or_none,
    int_or_none,
    KNOWN_EXTENSIONS,
    mimetype2ext,
    parse_qs,
    str_or_none,
    try_get,
    unified_timestamp,
    update_url_query,
    url_or_none,
    urlhandle_detect_ext,
)

class HypedditIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?hypeddit\.com/(?P<id>[A-z0-9]+)'
    _TESTS = [{
        'url': 'https://hypeddit.com/gjm094',
        'md5': '57cb297e6b2e551740d5a0b8084c3a79',
        'info_dict': {
            'id': 'gjm094',
            'ext': 'wav',
            'artist': 'Rocco Arizona',
            'title': 'Look What You Made Me Do',
            'thumbnail': 'https://hypeddit-gates-prod.s3.amazonaws.com/gjm094_coverartmanual',
        }
    }]

    _BASE_URL = 'https://hypeddit-gates-prod.s3.amazonaws.com/'

    def _real_extract(self, url):
        video_id = self._match_id(url)
        webpage = self._download_webpage(url,video_id)
        
        title = self._html_search_regex(r'<h2[^>]*>(.*?)<\/h2>', webpage, 'title')
        artist = self._html_search_regex(r'<h1[^>]*>(.*?)<\/h1>', webpage, 'artist')
        
        filename = artist + ' ' + title + '.wav'

        video_id = self._hidden_inputs(webpage)['current_download_file_listner']

        track_url = self._BASE_URL + video_id + '_main'
        thumbnail_url = self._BASE_URL + video_id + '_coverartmanual'

        urlh = self._request_webpage(
            HEADRequest(track_url), video_id, fatal=False, note='Determining source extension')
        ext = urlh and urlhandle_detect_ext(urlh)
        
        return {
            'id': video_id,
            'title': title,
            'artist': artist,
            'url': track_url,
            'thumbnail': thumbnail_url,
            'filepath': filename,
            'ext': ext
        }