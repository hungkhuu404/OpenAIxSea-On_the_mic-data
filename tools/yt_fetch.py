"""Fetch YouTube watch-page metadata + auto transcript (no video/audio download).
Usage: python -I -X utf8 yt_fetch.py <out_dir> id1 id2 ...
Writes <out_dir>/yt_<id>.json. Skips ids already present with transcript. Stops on IpBlocked.
"""
import sys, os, re, json, time
import site
sys.path.append(site.getusersitepackages())  # -I disables user site; packages come from pip --user
import requests
from youtube_transcript_api import YouTubeTranscriptApi

UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36')


def meta(vid, s):
    url = 'https://www.youtube.com/watch?v=' + vid + '&hl=vi'
    r = s.get(url, timeout=30)
    m = re.search(r'var ytInitialPlayerResponse = (\{.*?\});(?:var|</script>)', r.text, re.S)
    out = {'video_id': vid, 'url': 'https://www.youtube.com/watch?v=' + vid}
    if not m:
        out['meta_error'] = 'no player response, status %s' % r.status_code
        return out
    pr = json.loads(m.group(1))
    vd = pr.get('videoDetails', {})
    mf = pr.get('microformat', {}).get('playerMicroformatRenderer', {})
    out.update({
        'title': vd.get('title'), 'channel': vd.get('author'), 'channel_id': vd.get('channelId'),
        'description': vd.get('shortDescription'), 'length_s': vd.get('lengthSeconds'),
        'publish_date': mf.get('publishDate'), 'upload_date': mf.get('uploadDate'),
        'is_live_content': vd.get('isLiveContent'),
    })
    tracks = pr.get('captions', {}).get('playerCaptionsTracklistRenderer', {}).get('captionTracks', [])
    out['caption_tracks'] = [{'lang': t.get('languageCode'), 'kind': t.get('kind', 'manual'),
                              'name': (t.get('name') or {}).get('simpleText') or ''.join(x.get('text', '') for x in (t.get('name') or {}).get('runs', []))}
                             for t in tracks]
    return out


def main():
    outdir = sys.argv[1]
    ids = sys.argv[2:]
    os.makedirs(outdir, exist_ok=True)
    s = requests.Session()
    s.headers.update({'User-Agent': UA, 'Accept-Language': 'vi-VN,vi;q=0.9'})
    s.cookies.set('CONSENT', 'YES+cb', domain='.youtube.com')
    api = YouTubeTranscriptApi()
    for vid in ids:
        p = os.path.join(outdir, 'yt_' + vid + '.json')
        if os.path.exists(p):
            d = json.load(open(p, encoding='utf-8'))
            if d.get('transcript'):
                print('skip', vid)
                continue
        try:
            d = meta(vid, s)
        except Exception as e:
            d = {'video_id': vid, 'meta_error': repr(e)[:200]}
        time.sleep(1.5)
        try:
            ft = api.fetch(vid, languages=['vi'])
            d['transcript_kind'] = 'generated' if ft.is_generated else 'manual'
            d['transcript'] = [{'start': round(x.start, 2), 'dur': round(x.duration, 2), 'text': x.text} for x in ft.snippets]
        except Exception as e:
            name = type(e).__name__
            d['transcript'] = []
            d['transcript_error'] = name + ': ' + str(e)[:300]
            print('TRANSCRIPT ERR', vid, name)
            if 'IpBlocked' in name or 'RequestBlocked' in name:
                json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
                print('BLOCKED - stopping')
                break
        d['retrieved_at'] = time.strftime('%Y-%m-%d %H:%M:%S')
        json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print('OK', vid, d.get('channel'), (d.get('publish_date') or '')[:10], d.get('length_s'), len(d.get('transcript', [])), (d.get('title') or '')[:80])
        time.sleep(3)


if __name__ == '__main__':
    main()
