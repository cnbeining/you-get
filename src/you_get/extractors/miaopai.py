#!/usr/bin/env python

__all__ = ['miaopai_download']

from ..common import *
import urllib.error


def process_simple_m3u_to_file_list(url = ''):
    """str->list of str
    
    Hopefullt this could be merged in common later on
    if it works.
    """
    from urllib.parse import urlsplit
    base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(url))
    m3u = get_content(url)
    return [base_url + i for i in m3u.split() if not i.startswith('#')]

def miaopai_download_by_fid(fid, output_dir = '.', merge = False, info_only = False, **kwargs):
    '''Source: Android mobile'''
    fake_headers_mobile = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'UTF-8,*;q=0.5',
        'Accept-Encoding': 'gzip,deflate,sdch',
        'Accept-Language': 'en-US,en;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36'
    }
    page_url = 'http://video.weibo.com/show?fid=' + fid + '&type=mp4'

    mobile_page = get_content(page_url, headers=fake_headers_mobile)
    title = match1(mobile_page, r'<title>([^<]+)</title>')
    
    url = match1(mobile_page, r'<video id=.*?src=[\'"](.*?)[\'"]\W')

    if '.m3u8' in url:
        url_list = process_simple_m3u_to_file_list(url)
        size_total = 0
        for i in url_list:
            type_, ext, size = url_info(i)
            size_total += size
        print_info(site_info, title, 'mp4', size)

    else: 
        type_, ext, size = url_info(url)
        print_info(site_info, title, type_, size)
        url_list = [url]

    if not info_only:
        download_urls(url_list, title.replace('\n',''), 'mp4', total_size=None, output_dir=output_dir, merge=merge)

#----------------------------------------------------------------------
def miaopai_download(url, output_dir = '.', merge = False, info_only = False, **kwargs):
    fid = match1(url, r'\?fid=(\d{4}:\w{32})')
    if fid is not None:
        miaopai_download_by_fid(fid, output_dir, merge, info_only)
    elif '/p/230444' in url:
        fid = match1(url, r'/p/230444(\w+)')
        miaopai_download_by_fid('1034:'+fid, output_dir, merge, info_only)
    else:
        raise Exception('Unknown pattern')

site_info = "miaopai"
download = miaopai_download
download_playlist = playlist_not_supported('miaopai')
