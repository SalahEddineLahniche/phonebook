import os
import os.path
import pickle


class contact(object):
	"""docstring for contact"""
	def __init__(self, name = "", number = "", email = "", photo = "", numbers = {}, emails = {}, socialNetworks = {}, notes = ""):
		super(contact, self).__init__()
		self.name = name
		self.firstName = ""
		self.lastName = ""

		# ----
		tmp = name.split()
		if len(tmp) == 2:
			self.firstName = tmp[0]
			self.lastName = tmp[1]
		# ----
		self.nickName = ""
		self.number = number
		self.email = email
		self.photo = photo
		self.numbers = numbers + {'main': number}
		self.emails = emails + {'main': email}
		self.socialNetworks = socialNetworks
		self.notes = notes


	def __str__(self):
		return self.name

	def __format__(self, strFormat = ""):
		strFormat = strFormat.replace("$name", self.name)
		strFormat = strFormat.replace("$firstName", self.firstName)
		strFormat = strFormat.replace("$lastName", self.lastName)
		strFormat = strFormat.replace("$nickName", self.nickName)
		strFormat = strFormat.replace("$number", self.number)
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