import os
import os.path
import pickle
import random


class contact(object):
	"""docstring for contact"""
	def __init__(self, name = "", number = "", email = "", photo = "", numbers = {}, emails = {}, socialNetworks = {}, notes = "", ind = '212'):
		super(contact, self).__init__()
		self.id = hex(random.randint(0, 0xffffffff))[2:]
		self.name = name
		self.firstName = ""
		self.lastName = ""

		# ---- first last name feature
		tmp = name.split()
		if len(tmp) == 2:
			self.firstName = tmp[0]
			self.lastName = tmp[1]
		# ----

		self.nickName = ""
		self.ind = ind
		self.number = number
		self.email = email
		self.photo = photo

		# ---- check the existence of the file
		if not os.path.isfile(photo):
			self.photo = "!not found!"
		# ---- 

		self.numbers = numbers + {'main': number}
		self.emails = emails + {'main': email}
		self.socialNetworks = socialNetworks
		self.notes = notes


	def __str__(self):
		return self.name

	def __format__(self, strFormat = ""):
		strFormat = strFormat.replace("$id", self.id)
		strFormat = strFormat.replace("$name", self.name)
		strFormat = strFormat.replace("$firstName", self.firstName)
		strFormat = strFormat.replace("$lastName", self.lastName)
		strFormat = strFormat.replace("$nickName", self.nickName)
		strFormat = strFormat.replace("$number", '+' + self.indicatif + self.number)
		strFormat = strFormat.replace("$email", self.email)
		strFormat = strFormat.replace("$photo", self.photo)
		strFormat = strFormat.replace("$notes", self.notes)

		formatDico = {"$social-": self.socialNetworks, "$nums-": self.numbers, "$mails-" : self.emails}
		for frm in formatDico:
			startingInedx = 0
			i = strFormat.find(frm)
			while i != -1:
				count = 0
				i += len(frm)
				while i < len(strFormat):
					if strFormat[i].isalnum():
						count += 1
						i += 1
					else:
						break
				s = strFormat[i - count:i]
				if s in formatDico[frm]:
					strFormat = strFormat.replace(frm + s, formatDico[frm][s])
					i = strFormat.find(frm)
				else:
					startingInedx = i - count - len(frm) + 1
					i = strFormat.find(frm, startingInedx)

		return strFormat



contacts = []