import requests, re, time, sys
from bs4 import BeautifulSoup

#ur credentials here :)
usr = "xxxx"
pwd = "xxxx"

class BotPresensi():
	'''
	..............................
	. Bot Presensi - Skansaba.ID . @github  : soracyberteam
	.    By M. Khidhir Ibrahim   . @version : 2.0
	..............................
	'''
	target = "https://skansaba.id/"
	def __init__(self, username, password):
		self.username = username
		self.password = password

		self.s = requests.Session()
		self.getToken()
		print(self.__doc__)

		if self.doLogin():
			print("[*] Login Success")
			self.getEvents()
			for i in self.events:
				i_url   = i[0]
				i_time  = i[1]
				print("[*] Next to Present : " + i_url)
				while 1:
					if self.getUnixTime() == i_time:
						self.doLogin()
						if doPresensi(i_url):
							print("[*] Done : " + i_url)
							break
						else:
							print("[*] Check : " + i_url)
							key = input("Press any keys")
							break
					else:
						sys.stdout.write("\r[*] " + str(self.getUnixTime()) + " != " + str(i_time))


		else:
			print("Check ur credentials plz :)")

	def getUnixTime(self):
		return int(time.time())
	def doLogin(self):
		data 	= {
		'logintoken': self.logintoken,
		'username': self.username,
		'password': self.password,
		} 
		r 		= self.s.post(BotPresensi.target + "/login/index.php", data = data)
		if re.search("loginerrormessage", r.text):
			return False
		else:
			return True

	def getToken(self):
		r  = self.s.get(BotPresensi.target + "/login/index.php")
		bs = BeautifulSoup(r.text, "html.parser").find("input", attrs={'name': 'logintoken'}) 
		self.logintoken = bs.get("value")

	def getEvents(self):
		r 		= self.s.get(BotPresensi.target + "/calendar/view.php?view=day")
		bs 		= BeautifulSoup(r.text, "html.parser").find_all('div', attrs={'data-type': 'event'})
		self.events = []
		for i in bs:
			#ata.append(str(i))
			if re.search("attendance", str(i)):
				bs2 = BeautifulSoup(str(i), "html.parser")
				#get time
				time 	= bs2.find('div', attrs={'class': 'description card-body'}).find('a').get('href').replace(BotPresensi.target+"calendar/view.php?view=day&time=", '')

				mapel 	= bs2.find('div', attrs={'class': 'card-footer text-right bg-transparent'}).find('a').get('href')
				
				self.events.append([mapel, time])


	def doPresensi(self, target):
		r 	= self.s.get(target)
		bs 	= BeautifulSoup(r.text, "html.parser").find("a")

		for i in bs:
			if re.search("attendance.php", str(i)):
				r2 = self.s.get(str(i.get("href")))
				if re.search("fdescription required", r2.text):
						#get sess
						bs2 = BeautifulSoup(r2.text, "html.parser")
						self.sessid 	= bs2.find("input", attrs={'name': 'sessid'}).get('value')
						self.sesskey 	= bs2.find("input", attrs={'name': 'sesskey'}).get('value')
						self.status 	= bs2.find("input", attrs={'type': 'radio', 'name': 'status'}).get('value')

						#submit to present
						data = {
						'sessid': self.sessid,
						'sesskey': self.sesskey,
						'_qf__mod_attendance_student_attendance_form': 1,
						'mform_isexpanded_id_session': 1,
						'status': self.status,
						'submitbutton': 'Simpan+perubahan',
						}

						r3 	= self.s.post(BotPresensi.target + "/mod/attendance/attendance.php", data = data, headers = {'Referer': str(i.get('href'))})
				return True
			else:
				return False





if __name__ == '__main__':
	app = BotPresensi(usr, pwd)