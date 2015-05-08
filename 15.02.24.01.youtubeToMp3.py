# -*- coding: utf-8-*-
import urllib2
from bs4 import BeautifulSoup
import os
import datetime, time
import sys
import string
from selenium import webdriver
import datetime, time
from os.path import expanduser
import shutil

def init():
	# 허윤희
	# url = 'http://stage.m.music.daum.net/onair/radio/detail?channelId=821&programId=298'

	# # 배철수
	url = 'http://stage.m.music.daum.net/onair/radio/detail?channelId=831&programId=254'

	# # 노래의 날개 위에
	# url = 'http://stage.m.music.daum.net/onair/radio/detail?channelId=824&programId=10'
	html = urllib2.urlopen( url )
	soup = BeautifulSoup( html, 'lxml' )

	global songs
	songs = []
	for strong in soup.find_all( 'strong', class_ = 'tit_song' ):
		data = strong
		str = data.text

		str = string.replace( str, '\t', '' )
		str = string.replace( str, '\n', '' '' )
		str = string.replace( str, '    ', '' )
		str = str[2:]
		songs.append( str )

	global artists
	artists = []
	for strong in soup.find_all( 'span', class_ = 'txt_info ' ):
		data = strong
		str = data.text

		str = string.replace( str, '\t', '' )
		str = string.replace( str, '\n', '' '' )
		str = string.replace( str, '    ', '' )
		str = str[4:]
		artists.append( str )

	global keywords
	keywords = []
	for i in range( 0, len( songs ) ):
		# print artists[i], songs[i]
		keywords.append( artists[i] + songs[i] )
		i += 1

	global songFilesDirName
	now = time.localtime()

	songFilesDirName = './radio'

	if os.path.isdir( songFilesDirName ) == False :
		os.mkdir( songFilesDirName )

def youtubeProcessBySelenium( queryKeyword, idx ):
	queryKeyword = string.replace( queryKeyword, ' ', '+' )
	print queryKeyword
	url = 'https://www.youtube.com/results?search_query=' + queryKeyword

	driver = webdriver.Chrome()
	driver.set_window_size( 0, 0 )
	driver.get( url )
	links = driver.find_elements_by_class_name( 'yt-uix-tile-link' )

	youtubeLink = ''
	for link in links:
		youtubeLink =  link.get_attribute( 'href' )
		if string.count( youtubeLink, '/watch?v=' ) != 0:
			break

	print 'YouTube Link : ', youtubeLink
	driver.get( 'http://www.video2mp3.net/loading.php?url=' + youtubeLink )
	# loading.php에서 /view/ 화면으로 이동위한 sleep
	time.sleep( 15 )
	video2mp3Link = driver.current_url
	print 'video2mp3 접근 Link 1 : ', video2mp3Link
	driver.get( video2mp3Link )

	print 'video2mp3 접근 Link 2 : ', driver.current_url
	mp3Link = string.replace( video2mp3Link, 'view', 'load' )
	driver.get( mp3Link )

	time.sleep( 60 )

	homeDir = expanduser( '~' ) + '\Downloads'
	sourceFiles = os.listdir( homeDir )
	# destination = 'E:\\60.dev\99.python.project\youtube_to_mp3\\'
	destination = './' + songFilesDirName + '/'

	print '파일 처리전'
	for sourceFile in sourceFiles :
		if sourceFile.endswith( '.mp3' ) :
			shutil.move( homeDir + '\\' + sourceFile, destination + artists[idx].lstrip() + ' - ' + songs[idx].lstrip() + '.mp3' )
			print '이동위치 : ', destination + artists[idx].lstrip() + ' - ' + songs[idx].lstrip() + '.mp3'

	driver.close()
	print '파일 처리후 : ' + artists[idx].lstrip() + ' - ' + songs[idx].lstrip() + '.mp3'


# 한글처리를 위한 구문임.
reload(sys)
sys.setdefaultencoding('utf-8')

globalsongs = []
artists = []
keywords = []
songFilesDir = ''

init()

idx = 0
for keyword in keywords:
	# if idx == 0:
	youtubeProcessBySelenium( keyword, idx )
	idx += 1