import sys
import os
import pytest
from unittest.mock import patch, MagicMock
from langchain_yt_dlp.youtube_loader import YoutubeLoaderDL

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@patch('langchain_yt_dlp.youtube_loader._parse_video_id', return_value='SlPgsBqr4KI')
def test_extract_video_id(mock_parse_video_id):
    youtube_url = 'https://www.youtube.com/watch?v=SlPgsBqr4KI'
    video_id = YoutubeLoaderDL.extract_video_id(youtube_url)
    assert video_id == 'SlPgsBqr4KI'
    mock_parse_video_id.assert_called_once_with(youtube_url)

@patch('yt_dlp.YoutubeDL.extract_info')
def test_get_video_info(mock_extract_info):
    mock_extract_info.return_value = {
        'title': 'Test Title',
        'description': 'Test Description',
        'upload_date': '20230101',
        'view_count': 1000,
        'duration': 300,
        'uploader': 'Test Uploader',
        'channel_id': 'TestChannelID',
        'webpage_url': 'https://www.youtube.com/watch?v=SlPgsBqr4KI'
    }
    loader = YoutubeLoaderDL(video_id='SlPgsBqr4KI', add_video_info=True)
    video_info = loader._get_video_info()
    assert video_info['title'] == 'Test Title'
    assert video_info['description'] == 'Test Description'
    assert video_info['view_count'] == 1000
    assert video_info['length'] == 300
    assert video_info['author'] == 'Test Uploader'
    assert video_info['channel_id'] == 'TestChannelID'
    assert video_info['webpage_url'] == 'https://www.youtube.com/watch?v=SlPgsBqr4KI'

@patch('langchain_yt_dlp.youtube_loader.YoutubeLoaderDL._get_video_info')
def test_load_with_video_info(mock_get_video_info):
    mock_get_video_info.return_value = {
        'title': 'Test Title',
        'description': 'Test Description',
        'view_count': 1000,
        'publish_date': '2023-01-01',
        'length': 300,
        'author': 'Test Uploader',
        'channel_id': 'TestChannelID',
        'webpage_url': 'https://www.youtube.com/watch?v=SlPgsBqr4KI'
    }
    loader = YoutubeLoaderDL(video_id='SlPgsBqr4KI', add_video_info=True)
    documents = loader.load()
    assert len(documents) == 1
    assert documents[0].metadata['title'] == 'Test Title'
    assert documents[0].metadata['description'] == 'Test Description'
    assert documents[0].metadata['view_count'] == 1000
    assert documents[0].metadata['length'] == 300
    assert documents[0].metadata['author'] == 'Test Uploader'
    assert documents[0].metadata['channel_id'] == 'TestChannelID'
    assert documents[0].metadata['webpage_url'] == 'https://www.youtube.com/watch?v=SlPgsBqr4KI'

def test_load_without_video_info():
    loader = YoutubeLoaderDL(video_id='SlPgsBqr4KI', add_video_info=False)
    documents = loader.load()
    assert len(documents) == 1
    assert documents[0].metadata['source'] == 'SlPgsBqr4KI'
    assert 'title' not in documents[0].metadata