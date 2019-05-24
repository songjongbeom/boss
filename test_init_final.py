# -*- coding: utf-8 -*- 

import os
import sys
import asyncio
import discord
import datetime
import random
from discord.ext import commands
from gtts import gTTS
from github import Github
import base64

if not discord.opus.is_loaded():
	discord.opus.load_opus('opus')

basicSetting = []
bossData = []

bossNum = 0
chkvoicechannel = 0
chkrelogin = 0
chflg = 0
LoadChk = 0

bossTime = []
tmp_bossTime = []

bossTimeString = []
bossDateString = []
tmp_bossTimeString = []
tmp_bossDateString = []

bossFlag = []
bossFlag0 = []
bossMungFlag = []
bossMungCnt = []

channel_info = []
channel_name = []
channel_id = []
channel_voice_name = []
channel_voice_id = []
channel_type = []


client = discord.Client()

access_token = os.environ["BOT_TOKEN"]			
git_access_token = os.environ["GIT_TOKEN"]			
git_access_repo = os.environ["GIT_REPO"]			
git_access_repo_restart = os.environ["GIT_REPO_RESTART"]			

g = Github(git_access_token)
repo = g.get_repo(git_access_repo)
repo_restart = g.get_repo(git_access_repo_restart)

def init():
	global basicSetting
	global bossData

	global bossNum
	global chkvoicechannel
	global chkrelogin

	global bossTime
	global tmp_bossTime

	global bossTimeString
	global bossDateString
	global tmp_bossTimeString
	global tmp_bossDateString

	global bossFlag
	global bossFlag0
	global bossMungFlag
	global bossMungCnt
	
	global player
	global voice_client1
	
	global task1
	
	global channel_info
	global channel_name
	global channel_voice_name
	global channel_voice_id
	global channel_id
	global channel_type
	
	tmp_bossData = []
	f = []
	#print("test")
	
	inidata = repo.get_contents("test_setting.ini")
	file_data1 = base64.b64decode(inidata.content)
	file_data1 = file_data1.decode('utf-8')
	inputData = file_data1.split('\n')

	for i in range(inputData.count('\r')):
		inputData.remove('\r')

	basicSetting.append(inputData[0][11:])   #timezone
	basicSetting.append(inputData[4][15:])   #before_alert
	basicSetting.append(inputData[6][10:])   #mungChk
	basicSetting.append(inputData[5][16:])   #before_alert1
	basicSetting.append(inputData[1][14:16]) #restarttime 시
	basicSetting.append(inputData[1][17:])   #restarttime 분
	basicSetting.append(inputData[2][15:])   #voice채널 ID
	basicSetting.append(inputData[3][14:])   #text채널 ID


	for i in range(len(basicSetting)):
		basicSetting[i] = basicSetting[i].strip()
	
	#print (inputData, len(inputData))
	
	bossNum = int((len(inputData)-7)/5)
	
	#print (bossNum)
	
	for i in range(bossNum):
		tmp_bossData.append(inputData[i*5+7:i*5+12])
		
	#print (tmp_bossData)
		
	for j in range(bossNum):
		for i in range(len(tmp_bossData[j])):
			tmp_bossData[j][i] = tmp_bossData[j][i].strip()
	
	for j in range(bossNum):
		tmp_len = tmp_bossData[j][1].find(':')
		f.append(tmp_bossData[j][0][11:])         #0 : 보스명
		f.append(tmp_bossData[j][1][10:tmp_len])  #1 : 시
		f.append(tmp_bossData[j][2][13:])         #2 : 멍/미입력
		f.append(tmp_bossData[j][3][20:])         #3 : 분전 알림멘트
		f.append(tmp_bossData[j][4][13:])         #4 : 젠 알림멘트
		f.append(tmp_bossData[j][1][tmp_len+1:])  #5 : 분
		bossData.append(f)
		f = []

	print ('보탐봇 재시작 시간 : ', basicSetting[4], '시 ', basicSetting[5], '분')
	print ('보스젠알림시간1 : ', basicSetting[1])
	print ('보스젠알림시간2 : ', basicSetting[3])
	print ('보스멍확인시간 : ', basicSetting[2])
	
	for i in range(bossNum):
		bossTime.append(datetime.datetime.now()+datetime.timedelta(days=365, hours = int(basicSetting[0])))
		tmp_bossTime.append(datetime.datetime.now()+datetime.timedelta(days=365, hours = int(basicSetting[0])))
		bossTimeString.append('99:99:99')
		bossDateString.append('9999-99-99')
		tmp_bossTimeString.append('')
		tmp_bossDateString.append('')
		bossFlag.append(False)
		bossFlag0.append(False)
		bossMungFlag.append(False)
		bossMungCnt.append(0)
		
	#inidata.close()

init()

endTime = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
endTime = endTime.replace(hour=int(basicSetting[4]), minute=int(basicSetting[5]), second = int(0))
tmp_endTime = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
if endTime < tmp_endTime:
	endTime = endTime + datetime.timedelta(days = 1)

channel = ''

async def my_background_task():
	await client.wait_until_ready()

	global channel
	global endTime
		
	global basicSetting
	global bossData

	global bossNum
	global chkvoicechannel
	global chkrelogin

	global bossTime
	global tmp_bossTime

	global bossTimeString
	global bossDateString
	global tmp_bossTimeString
	global tmp_bossDateString

	global bossFlag
	global bossFlag0
	global bossMungFlag
	global bossMungCnt
	
	global player
	global voice_client1
	
	global task1
	
	global channel_info
	global channel_name
	global channel_id
	global channel_voice_name
	global channel_voice_id
	global channel_type

	while not client.is_closed:
		now = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
		priv0 = now+datetime.timedelta(minutes=int(basicSetting[3]))
		priv = now+datetime.timedelta(minutes=int(basicSetting[1]))
		aftr = now+datetime.timedelta(minutes=int(0-int(basicSetting[2])))
		
		nowTimeString = now.strftime('%H:%M:%S')
		nowDateString = now.strftime('%Y-%m-%d')
		endTimeString = endTime.strftime('%H:%M:%S')
		endDateString = endTime.strftime('%Y-%m-%d')
		

		if channel != '':			
			#await client.send_message(client.get_channel(channel), 'now : ' + nowDateString + '   ' + nowTimeString + '  end : ' + endDateString + '   ' + endTimeString, tts=False)
			if endTimeString == nowTimeString and endDateString == nowDateString:
				await client.send_message(client.get_channel(channel), '<갑자기 인사해도 놀라지마세요!>', tts=False)
				
				inidata_restart = repo_restart.get_contents("restart.txt")
				file_data_restart = base64.b64decode(inidata_restart.content)
				file_data_restart = file_data_restart.decode('utf-8')
				inputData_restart = file_data_restart.split('\n')
				
				if len(inputData_restart) < 3:	
					contents12 = repo_restart.get_contents("restart.txt")
					repo_restart.update_file(contents12.path, "restart_0", "restart\nrestart\nrestrat\n", contents12.sha)
				else:
					contents12 = repo_restart.get_contents("restart.txt")
					repo_restart.update_file(contents12.path, "restart_1", "", contents12.sha)
					
				endTime = endTime + datetime.timedelta(days = 1)

			for i in range(bossNum):
				#print (bossData[i][0], bossTime[i])
				if bossTime[i] <= priv0 and bossTime[i] > priv:
					if basicSetting[3] != '0':
						if bossFlag0[i] == False:
							bossFlag0[i] = True
							await client.send_message(client.get_channel(channel), bossData[i][0] + ' ' + basicSetting[3] + '분 전 ' + bossData[i][3], tts=False)
							await PlaySound(voice_client1, './sound/' + bossData[i][0] + '알림1.mp3')
				
				if bossTime[i] <= priv and bossTime[i] > now:
					if basicSetting[1] != '0' :
						if bossFlag[i] == False:
							bossFlag[i] = True
							await client.send_message(client.get_channel(channel), bossData[i][0] + ' ' + basicSetting[1] + '분 전 ' + bossData[i][3], tts=False)
							await PlaySound(voice_client1, './sound/' + bossData[i][0] + '알림.mp3')
						
				if bossTime[i] <= now :
					#print ('if ', bossTime[i])
					bossMungFlag[i] = True
					tmp_bossTime[i] = bossTime[i]
					bossTimeString[i] = '99:99:99'
					bossDateString[i] = '9999-99-99'
					bossTime[i] = now+datetime.timedelta(days=365)
					embed = discord.Embed(
							description= bossData[i][0] + '탐 ' + bossData[i][4],
							color=0x00ff00
							)
					await client.send_message(client.get_channel(channel), embed=embed, tts=False)
					await PlaySound(voice_client1, './sound/' + bossData[i][0] + '젠.mp3')
				
				if bossMungFlag[i] == True:
					if (bossTime[i]+datetime.timedelta(days=-365)) <= aftr:
						if basicSetting[2] != '0':
							if bossData[i][2] == '0':
								await client.send_message(client.get_channel(channel), bossData[i][0] + ' 미입력 됐습니다.', tts=False)
								await PlaySound(voice_client1, './sound/' + bossData[i][0] + '미입력.mp3')
								bossFlag[i] = False
								bossFlag0[i] = False
								bossMungFlag[i] = False
								bossMungCnt[i] = bossMungCnt[i] + 1
								tmp_bossTime[i] = bossTime[i] = nextTime = now+datetime.timedelta(hours=int(bossData[i][1]), minutes=int(0-int(basicSetting[2])+int(bossData[i][5])))
								tmp_bossTimeString[i] = bossTimeString[i] = nextTime.strftime('%H:%M:%S')
								tmp_bossDateString[i] = bossDateString[i] = nextTime.strftime('%Y-%m-%d')
								embed = discord.Embed(
									description= '다음 ' + bossData[i][0] + ' ' + bossTimeString[i] + '입니다.',
									color=0xff0000
									)
								await client.send_message(client.get_channel(channel), embed=embed, tts=False)
								await dbSave()
							else :
								await client.send_message(client.get_channel(channel), bossData[i][0] + ' 멍 입니다.')
								await PlaySound(voice_client1, './sound/' + bossData[i][0] + '멍.mp3')
								bossFlag[i] = False
								bossFlag0[i] = False
								bossMungFlag[i] = False
								bossMungCnt[i] = bossMungCnt[i] + 1
								tmp_bossTime[i] = bossTime[i] = nextTime = now+datetime.timedelta(hours=int(bossData[i][1]), minutes=int(0-int(basicSetting[2])+int(bossData[i][5])))
								tmp_bossTimeString[i] = bossTimeString[i] = nextTime.strftime('%H:%M:%S')
								tmp_bossDateString[i] = bossDateString[i] = nextTime.strftime('%Y-%m-%d')
								embed = discord.Embed(
									description= '다음 ' + bossData[i][0] + ' ' + bossTimeString[i] + '입니다.',
									color=0xff0000
									)
								await client.send_message(client.get_channel(channel), embed=embed, tts=False)
								await dbSave()
											
		await asyncio.sleep(1) # task runs every 60 seconds
		
async def MakeSound(saveSTR, filename):
	tts = gTTS(saveSTR, lang = 'ko')
	tts.save('./' + filename + '.mp3')
	
async def PlaySound(voiceclient, filename):
	player = voiceclient.create_ffmpeg_player(filename)
	player.start()
	while not player.is_done():
		await asyncio.sleep(1)
	# disconnect after the player has finished
	player.stop()

async def dbSave():
	global bossData
	global bossNum
	global bossTime
	global bossTimeString
	global bossDateString
	global bossMungCnt

	for i in range(bossNum):
		for j in range(bossNum):
			if bossTimeString[i] and bossTimeString[j] != '99:99:99':
				if bossTimeString[i] == bossTimeString[j] and i != j:
					tmp_time1 = bossTimeString[j][:6]
					tmp_time2 = (int(bossTimeString[j][6:]) + 1)%100
					if tmp_time2 < 10 :
						tmp_time22 = '0' + str(tmp_time2)
					elif tmp_time2 == 60 :
						tmp_time22 = '00'
					else :
						tmp_time22 = str(tmp_time2)
					bossTimeString[j] = tmp_time1 + tmp_time22
					
	datelist1 = bossTime
	
	datelist = list(set(datelist1))

	information1 = '----- 보스탐 정보 -----\n'
	for timestring in sorted(datelist):
		for i in range(bossNum):
			if timestring == bossTime[i]:
				if bossTimeString[i] != '99:99:99' :
					if bossData[i][2] == '0' :
						information1 += ' - ' + bossData[i][0] + '(' + bossData[i][1] + '.' + bossData[i][5] + ') : ' + bossTimeString[i] + ' @ ' + bossDateString[i] + ' (미입력 ' + str(bossMungCnt[i]) + '회)' + '\n'
					else : 
						information1 += ' - ' + bossData[i][0] + '(' + bossData[i][1] + '.' + bossData[i][5] + ') : ' + bossTimeString[i] + ' @ ' + bossDateString[i] + ' (멍 ' + str(bossMungCnt[i]) + '회)' + '\n'
	
	contents = repo.get_contents("my_bot.db")
	repo.update_file(contents.path, "bossDB", information1, contents.sha)


async def dbLoad():
	global LoadChk
	
	contents1 = repo.get_contents("my_bot.db")
	file_data = base64.b64decode(contents1.content)
	file_data = file_data.decode('utf-8')
	#print (file_data)
	beforeBossData = file_data.split('\n')
	
	if len(beforeBossData) > 1:	
		for i in range(len(beforeBossData)-1):
			for j in range(bossNum):
				if beforeBossData[i+1].find(bossData[j][0]) != -1 :
					#bossMungCnt[j] = 0
					#print (str(i) + '   '  + beforeBossData[i+1] + '     ' + bossData[j][0])
					tmp_len = beforeBossData[i+1].find(':')
					tmp_datelen = beforeBossData[i+1].find('@')

					
					years1 = beforeBossData[i+1][tmp_datelen+2:tmp_datelen+6]
					months1 = beforeBossData[i+1][tmp_datelen+7:tmp_datelen+9]
					days1 = beforeBossData[i+1][tmp_datelen+10:tmp_datelen+12]
					
					hours1 = beforeBossData[i+1][tmp_len+2:tmp_len+4]
					minutes1 = beforeBossData[i+1][tmp_len+5:tmp_len+7]
					seconds1 = beforeBossData[i+1][tmp_len+8:tmp_len+10]
					
					now2 = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))

					tmp_now = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
					tmp_now = tmp_now.replace(year = int(years1), month = int(months1), day = int(days1), hour=int(hours1), minute=int(minutes1), second = int(seconds1))

					if tmp_now < now2 : 
						deltaTime = datetime.timedelta(hours = int(bossData[j][1]), minutes = int(bossData[j][5]))
						while now2 > tmp_now :
							tmp_now = tmp_now + deltaTime
					
					now2 = tmp_now

					tmp_bossTime[j] = bossTime[j] = now2
					bossTimeString[j] = bossTime[j].strftime('%H:%M:%S')
					bossDateString[j] = bossTime[j].strftime('%Y-%m-%d')
					
					#print (bossData[j][0] + '  ' + bossTimeString[j] + '  ' + bossDateString[j])

					#print (beforeBossData[i+1])
					#print (len(beforeBossData[i+1]))
					#print (beforeBossData[i+1][len(beforeBossData[i+1])-3:len(beforeBossData[i+1])-2])
					if beforeBossData[i+1][len(beforeBossData[i+1])-3:len(beforeBossData[i+1])-2] != 0 :
						bossMungCnt[j] = int(beforeBossData[i+1][len(beforeBossData[i+1])-3:len(beforeBossData[i+1])-2])
						#print (bossMungCnt)
					else:
						bossMungCnt[j] = 0
		LoadChk = 0
		print ("<불러오기 완료>")
	else:
		#await client.send_message(client.get_channel(channel), '<보스타임 정보가 없습니다.>', tts=False)
		LoadChk = 1
		print ("보스타임 정보가 없습니다.")

async def JointheVC(VCchannel, TXchannel):
	global chkvoicechannel
	global voice_client1
	global task1

	
	if VCchannel is not None:
		#print (task1)
		if chkvoicechannel == 0:
			voice_client1 = await client.join_voice_channel(VCchannel)
			chkvoicechannel = 1
			await PlaySound(voice_client1, './sound/hello.mp3')
		else :
			await voice_client1.disconnect()
			voice_client1 = await client.join_voice_channel(VCchannel)
			await PlaySound(voice_client1, './sound/hello.mp3')
		task1 = client.loop.create_task(my_background_task())
	else:
		await client.send_message(client.get_channel(TXchannel), '음성채널에 먼저 들어가주세요.', tts=False)

# 봇이 구동되었을 때 동작되는 코드입니다.
@client.event
async def on_ready():
	global task1
	global channel
	
	global channel_info
	global channel_name
	global channel_id
	global channel_voice_name
	global channel_voice_id
	global channel_type
	
	global chkvoicechannel
	global chflg
			
	print("Logged in as ") #화면에 봇의 아이디, 닉네임이 출력됩니다.
	print(client.user.name)
	print(client.user.id)
	print("===========")

	
	#await joinVoiceChannel()
	all_channels = client.get_all_channels()
	
	for channel1 in all_channels:
		channel_type.append(str(channel1.type))
		channel_info.append(channel1)
	
	for i in range(len(channel_info)):
		if channel_type[i] == "text":
			channel_name.append(str(channel_info[i].name))
			channel_id.append(str(channel_info[i].id))
			
	for i in range(len(channel_info)):
		if channel_type[i] == "voice":
			channel_voice_name.append(str(channel_info[i].name))
			channel_voice_id.append(str(channel_info[i].id))

	await dbLoad()
	
	if basicSetting[6] != "" and basicSetting[7] != "" :
		#print ('join channel')
		await JointheVC(client.get_channel(basicSetting[6]), client.get_channel(basicSetting[7]))
		await client.send_message(client.get_channel(basicSetting[7]), '< 텍스트채널 [' + client.get_channel(basicSetting[7]).name + '] 접속완료>', tts=False)
		await client.send_message(client.get_channel(basicSetting[7]), '< 음성채널 [' + client.get_channel(basicSetting[6]).name + '] 접속완료>', tts=False)
		await client.send_message(client.get_channel(basicSetting[7]), '< 보탐봇 재시작 설정시간 ' + basicSetting[4] + '시 ' + basicSetting[5] + '분입니다. >', tts=False)
		channel = basicSetting[7]
		chflg = 1

	#task = client.loop.create_task(my_background_task())
	
	# 디스코드에는 현재 본인이 어떤 게임을 플레이하는지 보여주는 기능이 있습니다.
	# 이 기능을 사용하여 봇의 상태를 간단하게 출력해줄 수 있습니다.
	await client.change_presence(game=discord.Game(name="반갑습니다 :D", type=1))

	
# 봇이 새로운 메시지를 수신했을때 동작되는 코드입니다.
@client.event
async def on_message(msg):
	if msg.author.bot: #만약 메시지를 보낸사람이 봇일 경우에는
		return None #동작하지 않고 무시합니다.

	global channel
	
	global basicSetting
	global bossData

	global bossNum
	global chkvoicechannel
	global chkrelogin

	global bossTime
	global tmp_bossTime

	global bossTimeString
	global bossDateString
	global tmp_bossTimeString
	global tmp_bossDateString

	global bossFlag
	global bossFlag0
	global bossMungFlag
	global bossMungCnt
	
	global player
	global voice_client1
	
	global task1
	
	global channel_info
	global channel_name
	global channel_id
	global channel_voice_name
	global channel_voice_id
	global channel_type
	
	global chflg
	global LoadChk
	
	id = msg.author.id #id라는 변수에는 메시지를 보낸사람의 ID를 담습니다.
	
	if chflg == 0 :
		channel = msg.channel.id #channel이라는 변수에는 메시지를 받은 채널의 ID를 담습니다
		if basicSetting[7] == "":
			inidata_textCH = repo.get_contents("test_setting.ini")
			file_data_textCH = base64.b64decode(inidata_textCH.content)
			file_data_textCH = file_data_textCH.decode('utf-8')
			inputData_textCH = file_data_textCH.split('\n')
			
			for i in range(len(inputData_textCH)):
				if inputData_textCH[i] == 'textchannel = \r':
					inputData_textCH[i] = 'textchannel = ' + channel + '\r'
					basicSetting[7] = channel
					#print ('======', inputData_text[i])
			
			result_textCH = '\n'.join(inputData_textCH)
			
			#print (result_textCH)
			
			contents = repo.get_contents("test_setting.ini")
			repo.update_file(contents.path, "test_setting", result_textCH, contents.sha)

		await client.send_message(client.get_channel(channel), '< 텍스트채널 [' + client.get_channel(channel).name + '] 접속완료>', tts=False)
			
		if basicSetting[6] != "":
			#print ('join channel')
			await JointheVC(client.get_channel(basicSetting[6]), channel)
			await client.send_message(client.get_channel(channel), '< 음성채널 [' + client.get_channel(basicSetting[6]).name + '] 접속완료>', tts=False)
		else:
			#print ('join no')
			task1 = client.loop.create_task(my_background_task())

		await client.send_message(client.get_channel(channel), '< 보탐봇 재시작 설정시간 ' + basicSetting[4] + '시 ' + basicSetting[5] + '분입니다. >', tts=False)
		chflg = 1
		
	if client.get_channel(channel) != msg.channel :
		return None
	else :
		message = await client.get_message(client.get_channel(channel), msg.id)
		
		##################################

		if message.content.startswith('!채널확인'):
			ch_information = ''
			for i in range(len(channel_name)):
				ch_information += channel_name[i] + '\n'
			print (ch_information)
			embed = discord.Embed(
				title = "----- 채널 정보 -----",
				description= ch_information,
				color=0xff00ff
				)
			await client.send_message(client.get_channel(channel), embed=embed, tts=False)

		##################################

		if message.content.startswith('!채널이동'):
			tmp_sayMessage1 = message.content
			
			for i in range(len(channel_name)):
				if  channel_name[i] == str(tmp_sayMessage1[6:]):
					channel = channel_id[i]
				
			await client.send_message(client.get_channel(channel), '< ' + client.get_channel(channel).name + ' 이동완료>', tts=False)
		
		hello = message.content
		#print (hello, len(hello))

		##################################

		for i in range(bossNum):
			if message.content.startswith(bossData[i][0] +'컷'):
				tmp_msg = bossData[i][0] +'컷'
				if len(hello) > len(tmp_msg) + 3 :
					if hello.find(':') != -1 :
						chkpos = hello.find(':')
						hours1 = hello[chkpos-2:chkpos]
						minutes1 = hello[chkpos+1:chkpos+3]
						now2 = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
						tmp_now = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
						tmp_now = tmp_now.replace(hour=int(hours1), minute=int(minutes1))
					else:
						chkpos = len(hello)-2
						hours1 = hello[chkpos-2:chkpos]
						minutes1 = hello[chkpos:chkpos+2]
						now2 = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
						tmp_now = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
						tmp_now = tmp_now.replace(hour=int(hours1), minute=int(minutes1))
				else:
					now2 = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
					tmp_now = now2
					
				#await client.send_message(client.get_channel(channel), now2, tts=False)
				#await client.send_message(client.get_channel(channel), tmp_now, tts=False)
					
				bossFlag[i] = False
				bossFlag0[i] = False
				bossMungFlag[i] = False
				bossMungCnt[i] = 0

				if tmp_now > now2 :
					tmp_now = tmp_now + datetime.timedelta(days=int(-1))
					
				if tmp_now < now2 : 
					deltaTime = datetime.timedelta(hours = int(bossData[i][1]), minutes = int(bossData[i][5]))
					while now2 > tmp_now :
						tmp_now = tmp_now + deltaTime
						bossMungCnt[i] = bossMungCnt[i] + 1
					now2 = tmp_now
					bossMungCnt[i] = bossMungCnt[i] - 1
				else :
					now2 = now2 + datetime.timedelta(hours = int(bossData[i][1]), minutes = int(bossData[i][5]))
							
				tmp_bossTime[i] = bossTime[i] = nextTime = now2
				tmp_bossTimeString[i] = bossTimeString[i] = nextTime.strftime('%H:%M:%S')
				#print (tmp_bossTimeString[i])
				tmp_bossDateString[i] = bossDateString[i] = nextTime.strftime('%Y-%m-%d')
				#print (tmp_bossDateString[i])
				#await client.send_message(channel, '다음 '+ bossData[i][0] + ' ' + bossTimeString[i] + '입니다.', tts=False)
				embed = discord.Embed(
						description= '다음 ' + bossData[i][0] + ' ' + bossTimeString[i] + '입니다.',
						color=0xff0000
						)
				await client.send_message(client.get_channel(channel), embed=embed, tts=False)
				await dbSave()

		##################################

			if message.content.startswith(bossData[i][0] +'멍'):
				tmp_msg = bossData[i][0] +'멍'
				tmp_now = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
				temptime = tmp_bossTime[i]
				if len(hello) > len(tmp_msg) + 3 :
					if hello.find(':') != -1 :
						chkpos = hello.find(':')
						hours1 = hello[chkpos-2:chkpos]
						minutes1 = hello[chkpos+1:chkpos+3]					
						tmp_now = tmp_now.replace(hour=int(hours1), minute=int(minutes1))
						nextTime = tmp_now + datetime.timedelta(hours = int(bossData[i][1]), minutes = int(bossData[i][5]))
					else:
						chkpos = len(hello)-2
						hours1 = hello[chkpos-2:chkpos]
						minutes1 = hello[chkpos:chkpos+2]					
						tmp_now = tmp_now.replace(hour=int(hours1), minute=int(minutes1))
						nextTime = tmp_now + datetime.timedelta(hours = int(bossData[i][1]), minutes = int(bossData[i][5]))			
				else:
					temptime = temptime.replace(year=int(tmp_now.year), day=int(tmp_now.day))
					nextTime = temptime + datetime.timedelta(hours = int(bossData[i][1]), minutes = int(bossData[i][5]))
				
				bossFlag[i] = False
				bossFlag0[i] = False
				bossMungFlag[i] = False
				bossMungCnt[i] = bossMungCnt[i] + 1

				if nextTime < tmp_now : 
					nextTime = nextTime + datetime.timedelta(days=int(1))
				else :
					nextTime = nextTime

				
				bossTime[i] = nextTime				

				tmp_bossTimeString[i] = bossTimeString[i] = nextTime.strftime('%H:%M:%S')
				tmp_bossDateString[i] = bossDateString[i] = nextTime.strftime('%Y-%m-%d')
				embed = discord.Embed(
						description= '다음 ' + bossData[i][0] + ' ' + bossTimeString[i] + '입니다.',
						color=0xff0000
						)
				await client.send_message(client.get_channel(channel), embed=embed, tts=False)
				await dbSave()
				
		##################################

		for i in range(bossNum):
			if message.content.startswith(bossData[i][0] +'예상'):
				tmp_msg = bossData[i][0] +'예상'
				if len(hello) > len(tmp_msg) + 3 :
					if hello.find(':') != -1 :
						chkpos = hello.find(':')
						hours1 = hello[chkpos-2:chkpos]
						minutes1 = hello[chkpos+1:chkpos+3]
						now2 = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
						tmp_now = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
						tmp_now = tmp_now.replace(hour=int(hours1), minute=int(minutes1))
					else:
						chkpos = len(hello)-2
						hours1 = hello[chkpos-2:chkpos]
						minutes1 = hello[chkpos:chkpos+2]
						now2 = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
						tmp_now = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
						tmp_now = tmp_now.replace(hour=int(hours1), minute=int(minutes1))
					
					bossFlag[i] = False
					bossFlag0[i] = False
					bossMungFlag[i] = False
					bossMungCnt[i] = 0

					if tmp_now < now2 :
						tmp_now = tmp_now + datetime.timedelta(days=int(1))

					tmp_bossTime[i] = bossTime[i] = nextTime = tmp_now
					tmp_bossTimeString[i] = bossTimeString[i] = nextTime.strftime('%H:%M:%S')
					#print (tmp_bossTimeString[i])
					tmp_bossDateString[i] = bossDateString[i] = nextTime.strftime('%Y-%m-%d')
					#print (tmp_bossDateString[i])
					#await client.send_message(channel, '다음 '+ bossData[i][0] + ' ' + bossTimeString[i] + '입니다.', tts=False)
					embed = discord.Embed(
							description= '다음 ' + bossData[i][0] + ' ' + bossTimeString[i] + '입니다.',
							color=0xff0000
							)
					await client.send_message(client.get_channel(channel), embed=embed, tts=False)
					await dbSave()
				else:
					await client.send_message(client.get_channel(channel), bossData[i][0] +' 예상 시간을 입력해주세요.', tts=False)
					
		##################################
				
			if message.content.startswith(bossData[i][0] +'삭제'):
				bossTime[i] = datetime.datetime.now()+datetime.timedelta(days=365, hours = int(basicSetting[0]))
				tmp_bossTime[i] =  datetime.datetime.now()+datetime.timedelta(days=365, hours = int(basicSetting[0]))
				bossTimeString[i] = '99:99:99'
				bossDateString[i] = '9999-99-99'
				tmp_bossTimeString[i] = ''
				tmp_bossDateString[i] = ''
				bossFlag[i] = (False)
				bossFlag0[i] = (False)
				bossMungFlag[i] = (False)
				bossMungCnt[i] = 0
				await client.send_message(client.get_channel(channel), '<' + bossData[i][0] + ' 삭제완료>', tts=False)
				await dbSave()
				print ('<' + bossData[i][0] + ' 삭제완료>')
			
		if message.content.startswith('!오빠'):
			#await client.send_message(channel, '오빠달려려어어어어어어 ', tts=False)
			await PlaySound(voice_client1, './sound/오빠.mp3')
		if message.content.startswith('!언니'):
			#await client.send_message(channel, '오빠달려려어어어어어어 ', tts=False)
			await PlaySound(voice_client1, './sound/언니.mp3')
		if message.content.startswith('!형'):
			#await client.send_message(channel, '오빠달려려어어어어어어 ', tts=False)
			await PlaySound(voice_client1, './sound/형.mp3')

		##################################

		if message.content.startswith('!분배'):
			separate_money = []
			separate_money = message.content[4:].split(" ")
			num_sep = int(separate_money[0])
			cal_tax1 = int(float(separate_money[1])*0.05)
			real_money = int(int(separate_money[1]) - cal_tax1)
			cal_tax2 = int(real_money/num_sep) - int(float(int(real_money/num_sep))*0.95)
			if num_sep == 0 :
				await client.send_message(client.get_channel(channel), '분배 인원이 0입니다. 재입력 해주세요.', tts=False)
			else :
				await client.send_message(client.get_channel(channel), '1차세금 : ' + str(cal_tax1) + '\n1차 수령액 : ' + str(real_money) + '\n분배자 거래소등록금액 : ' + str(int(real_money/num_sep)) + '\n2차세금 : ' + str(cal_tax2) + '\n인당 실수령액 : ' + str(int(float(int(real_money/num_sep))*0.95)), tts=False)

		##################################

		if message.content.startswith('!사다리'):
			ladder = []
			ladder = message.content[5:].split(" ")
			num_cong = int(ladder[0])
			del(ladder[0])
			if num_cong < len(ladder):
				result_ladder = random.sample(ladder, num_cong)
				print (result_ladder)
				await client.send_message(client.get_channel(channel), '----- 당첨! -----\n' + str(result_ladder), tts=False)
			else:
				await client.send_message(client.get_channel(channel), '추첨인원이 총 인원과 같거나 많습니다. 재입력 해주세요', tts=False)
			
		if message.content.startswith('!메뉴'):
			embed = discord.Embed(
					title = "----- 메뉴 -----",
					description= '!채널확인\n!채널이동 [채널명]\n!소환\n!불러오기\n!초기화\n!명치\n!미예약\n!분배 [인원] [금액]\n!사다리 [뽑을인원수] [아이디1] [아이디2] ...\n!보스일괄 00:00 또는 !보스일괄 0000\n!ㅂ,ㅃ,q\n\n[보스명]컷\n[보스명]컷 00:00 또는 [보스명]컷 0000\n[보스명]멍\n[보스명]멍 00:00 또는 [보스명]멍 0000\n[보스명]삭제\n보스탐',
					color=0xff00ff
					)
			await client.send_message(client.get_channel(channel), embed=embed, tts=False)

		##################################

		if message.content.startswith('!미예약'):
			temp_bossTime2 = []
			for i in range(bossNum):
				if bossTimeString[i] == '99:99:99' :
					temp_bossTime2.append(bossData[i][0])
					
			embed = discord.Embed(
					title = "----- 미예약보스 -----",
					description= str(temp_bossTime2),
					color=0x0000ff
					)
			await client.send_message(client.get_channel(channel), embed=embed, tts=False)

		##################################		
			
		if message.content.startswith('!v') or message.content.startswith('!ㅍ'):
			tmp_sayMessage = message.content
			sayMessage = tmp_sayMessage[3:]
			await MakeSound(message.author.display_name +'님이' + sayMessage, './sound/say')
			await client.send_message(client.get_channel(channel), "<@" +id+ ">님이 \"" + sayMessage + "\"", tts=False)
			await PlaySound(voice_client1, './sound/say.mp3')

		##################################

		if message.content.startswith('!명치'):
			if chkvoicechannel == 1:
				chkvoicechannel = 0
				await voice_client1.disconnect()
			
			basicSetting = []
			bossData = []
			bossTime = []
			tmp_bossTime = []
			bossTimeString = []
			bossDateString = []
			tmp_bossTimeString = []
			tmp_bossDateString = []
			bossFlag = []
			bossFlag0 = []
			bossMungFlag = []
			bossMungCnt = []

			init()
			
			if task1.cancelled != False:
				task1.cancel()
				print ('task cancle')
			
			await client.send_message(client.get_channel(channel), '<재접속 성공>', tts=False)
			print ("<재접속 성공>")

			await dbLoad()

			if LoadChk == 0:
				await client.send_message(client.get_channel(channel), '<불러오기 완료>', tts=False)
			else:
				await client.send_message(client.get_channel(channel), '<보스타임 정보가 없습니다.>', tts=False)
			
			await dbSave()

			voice_channel = message.author.voice.voice_channel

			await JointheVC(voice_channel, channel)
			
		#############################

		if message.content.startswith('!소환'):
			voice_channel = message.author.voice.voice_channel
			
			if basicSetting[6] == "":
				inidata_voiceCH = repo.get_contents("test_setting.ini")
				file_data_voiceCH = base64.b64decode(inidata_voiceCH.content)
				file_data_voiceCH = file_data_voiceCH.decode('utf-8')
				inputData_voiceCH = file_data_voiceCH.split('\n')
				
				for i in range(len(inputData_voiceCH)):
					if inputData_voiceCH[i] == 'voicechannel = \r':
						inputData_voiceCH[i] = 'voicechannel = ' + voice_channel.id + '\r'
						basicSetting[6] = voice_channel.id
						#print ('======', inputData_text[i])
				
				result_voiceCH = '\n'.join(inputData_voiceCH)
				
				#print (result_voiceCH)
				
				contents = repo.get_contents("test_setting.ini")
				repo.update_file(contents.path, "test_setting", result_voiceCH, contents.sha)
				
			elif basicSetting[6] != voice_channel.id:
				inidata_voiceCH = repo.get_contents("test_setting.ini")
				file_data_voiceCH = base64.b64decode(inidata_voiceCH.content)
				file_data_voiceCH = file_data_voiceCH.decode('utf-8')
				inputData_voiceCH = file_data_voiceCH.split('\n')
				
				for i in range(len(inputData_voiceCH)):
					if inputData_voiceCH[i] == 'voicechannel = ' + basicSetting[6] + '\r':
						inputData_voiceCH[i] = 'voicechannel = ' + voice_channel.id + '\r'
						basicSetting[6] = voice_channel.id
						#print ('======', inputData_text[i])
				
				result_voiceCH = '\n'.join(inputData_voiceCH)
				
				#print (result_voiceCH)
				
				contents = repo.get_contents("test_setting.ini")
				repo.update_file(contents.path, "test_setting", result_voiceCH, contents.sha)

			if task1.cancelled != False:
				task1.cancel()
				print ('task cancle')

			await JointheVC(voice_channel, channel)
			await client.send_message(client.get_channel(channel), '< 음성채널 [' + client.get_channel(voice_channel.id).name + '] 접속완료>', tts=False)
		
		##################################
					
		if message.content.startswith('!초기화'):
			basicSetting = []
			bossData = []

			bossTime = []
			tmp_bossTime = []

			bossTimeString = []
			bossDateString = []
			tmp_bossTimeString = []
			tmp_bossDateString = []

			bossFlag = []
			bossFlag0 = []
			bossMungFlag = []
			bossMungCnt = []
			
			init()

			await dbSave()

			await client.send_message(client.get_channel(channel), '<초기화 완료>', tts=False)
			print ("<초기화 완료>")

		##################################
		
		if message.content.startswith('!보스일괄'):
			for i in range(bossNum):
				tmp_msg = '!보스일괄'
				if len(hello) > len(tmp_msg) + 3 :
					if hello.find(':') != -1 :
						chkpos = hello.find(':')
						hours1 = hello[chkpos-2:chkpos]
						minutes1 = hello[chkpos+1:chkpos+3]
						now2 = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
						tmp_now = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
						tmp_now = tmp_now.replace(hour=int(hours1), minute=int(minutes1))
					else:
						chkpos = len(hello)-2
						hours1 = hello[chkpos-2:chkpos]
						minutes1 = hello[chkpos:chkpos+2]
						now2 = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
						tmp_now = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
						tmp_now = tmp_now.replace(hour=int(hours1), minute=int(minutes1))
				else:
					now2 = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
					tmp_now = now2
					
				bossFlag[i] = False
				bossFlag0[i] = False
				bossMungFlag[i] = False
				bossMungCnt[i] = 1

				if tmp_now > now2 :
					tmp_now = tmp_now + datetime.timedelta(days=int(-1))
					
				if tmp_now < now2 : 
					deltaTime = datetime.timedelta(hours = int(bossData[i][1]), minutes = int(bossData[i][5]))
					while now2 > tmp_now :
						tmp_now = tmp_now + deltaTime
						bossMungCnt[i] = bossMungCnt[i] + 1
					now2 = tmp_now
					bossMungCnt[i] = bossMungCnt[i] - 1
				else :
					now2 = now2 + datetime.timedelta(hours = int(bossData[i][1]), minutes = int(bossData[i][5]))
							
				bossTime[i] = nextTime = now2
				tmp_bossTimeString[i] = bossTimeString[i] = nextTime.strftime('%H:%M:%S')
				tmp_bossDateString[i] = bossDateString[i] = nextTime.strftime('%Y-%m-%d')

			await dbSave()
			await dbLoad()
			await dbSave()
			
			await client.send_message(client.get_channel(channel), '<보스 일괄 입력 완료>', tts=False)
			print ("<보스 일괄 입력 완료>")

		##################################


		if message.content.startswith('!설정확인'):			
			setting_val = '보스젠알림시간1 : ' + basicSetting[1] + ' 분 전\n' + '보스젠알림시간2 : ' + basicSetting[3] + ' 분 전\n' + '보스멍확인시간 : ' + basicSetting[2] + ' 분 후\n'
			embed = discord.Embed(
					title = "----- 설정내용 -----",
					description= setting_val,
					color=0xff00ff
					)
			await client.send_message(client.get_channel(channel), embed=embed, tts=False)
			print ('보스젠알림시간1 : ', basicSetting[1])
			print ('보스젠알림시간2 : ', basicSetting[3])
			print ('보스멍확인시간 : ', basicSetting[2])

		##################################

		if message.content.startswith('!불러오기'):
			await dbLoad()

			if LoadChk == 0:
				await client.send_message(client.get_channel(channel), '<불러오기 완료>', tts=False)
			else:
				await client.send_message(client.get_channel(channel), '<보스타임 정보가 없습니다.>', tts=False)
		
		##################################
		
		if message.content.startswith('!ㅂ') or message.content.startswith('!q') or message.content.startswith('!ㅃ'):
			await dbLoad()

			datelist = bossTime
			
			sorted_datelist = sorted(datelist)
			
			#print (sorted_datelist)
			
			for i in range(bossNum):
				if sorted_datelist[0] == bossTime[i]:
					leftTime = bossTime[i] - datetime.datetime.now() - datetime.timedelta(hours = int(basicSetting[0]))
			
					#print (leftTime)
					#leftTimeStr = leftTime.strftime('%H:%M:%S')

					total_seconds = int(leftTime.total_seconds())
					hours, remainder = divmod(total_seconds,60*60)
					minutes, seconds = divmod(remainder,60)

					result_lefttime = bossData[i][0] + '탐 %02d:%02d:%02d 남았습니다.' % (hours,minutes,seconds)
					
					#print (result_lefttime)
					#print(bossData[i][0] + '탐 %02d:%02d:%02d 남았습니다.' % (hours,minutes,seconds))
					
					embed = discord.Embed(
						description= result_lefttime,
						color=0xff0000
						)
					await client.send_message(client.get_channel(channel), embed=embed, tts=False)

			#print (leftTimeStr)

		##################################

		if message.content.startswith('보스탐'):
			for i in range(bossNum):
				for j in range(bossNum):
					if bossTimeString[i] and bossTimeString[j] != '99:99:99':
						if bossTimeString[i] == bossTimeString[j] and i != j:
							tmp_time1 = bossTimeString[j][:6]
							tmp_time2 = (int(bossTimeString[j][6:]) + 1)%100
							if tmp_time2 < 10 :
								tmp_time22 = '0' + str(tmp_time2)
							elif tmp_time2 == 60 :
								tmp_time22 = '00'
							else :
								tmp_time22 = str(tmp_time2)
							bossTimeString[j] = tmp_time1 + tmp_time22
							
			datelist2 = bossTime
	
			datelist = list(set(datelist2))
			
			#print ('datelist', len(datelist))
			#print ('bosslist', len(bossTime))
			#print ('bossdata', len(bossData))

			temp_bossTime1 = []
			for i in range(bossNum):
				if bossTimeString[i] == '99:99:99' :
					temp_bossTime1.append(bossData[i][0])
						
			information = ''
			#information1 = '----- 보스탐 정보 -----\n'
			for timestring in sorted(datelist):
				for i in range(bossNum):
					if timestring == bossTime[i]:
						if bossTimeString[i] != '99:99:99' :
							if bossData[i][2] == '0' :
								if bossMungCnt[i] == 0 :
									information += ' - ' + bossData[i][0] + '(' + bossData[i][1] + '.' + bossData[i][5] + ') : ' + bossTimeString[i] + '\n'
								else :
									information += ' - ' + bossData[i][0] + '(' + bossData[i][1] + '.' + bossData[i][5] + ') : ' + bossTimeString[i] + ' (미입력 ' + str(bossMungCnt[i]) + '회)' + '\n'
							else : 
								if bossMungCnt[i] == 0 :
									information += ' - ' + bossData[i][0] + '(' + bossData[i][1] + '.' + bossData[i][5] + ') : ' + bossTimeString[i] + '\n'
								else :
									information += ' - ' + bossData[i][0] + '(' + bossData[i][1] + '.' + bossData[i][5] + ') : ' + bossTimeString[i] + ' (멍 ' + str(bossMungCnt[i]) + '회)' + '\n'

			embed = discord.Embed(
					title = "----- 보스탐 정보 -----",
					description= information,
					color=0x0000ff
					)
			embed.add_field(
					name="----- 미예약보스 -----",
					value=str(temp_bossTime1)
					)
			await client.send_message(client.get_channel(channel), embed=embed, tts=False)

			await dbSave()

		##################################

		if message.content.startswith('!현재시간'):
			now3 = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
			await client.send_message(client.get_channel(channel), now3.strftime('%Y-%m-%d') + '   ' + now3.strftime('%H:%M:%S'), tts=False)

client.run(access_token)
