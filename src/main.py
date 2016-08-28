import os
import os.path
import pickle

class command():
	def __init__(self):
		self.main = ''
		self.options = {}

class contact(object):
	"""docstring for contact"""
	def __init__(self, name = "", number = "", nickName = "", email = "", photo = "", numbers = {}, emails = {}, socialNetworks = {}, notes = ""):
		super(contact, self).__init__()
		self.name = name
		self.firstName = ""
		self.lastName = ""
		self.nickName = nickName
		self.number = number
		self.email = email
		self.photo = photo
		self.numbers = numbers
		self.emails = emails
		self.socialNetworks = socialNetworks
		self.notes = notes

	def refresh():
		# ---- first last name feature
		tmp = self.name.split()
		if len(tmp) >= 2:
			self.firstName = tmp[0]
			self.lastName = " ".join(tmp[1:])
		# ----
		if not self.number[0] == "+":
			self.number = "+212" + self.number[1:]
		# ---- check the existence of the file
		if not os.path.isfile(self.photo):
			self.photo = "!not found!"
		# ----
		self.numbers['main'] = self.number
		self.emails['main'] = self.email


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

		formatDico = {"$social-": self.socialNetworks, "$num-": self.numbers, "$mail-" : self.emails}
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


# initializing variables
contacts = []

commands = ['exit', 'add', 'update', 'remove', 'show', 'help']
dicoFields = {'social': "socialNetworks", "num" : "numbers", "mail": "emails"}
exitCode = 0

HELP_EXIT = "exit the app saving current changes\n\n"
HELP_ADD = "Add a contact to the database\n\n"+ \
			"Usage:\nadd [field]=[value]\n" + \
			"Field might be: firstName, lastName, name, number," + \
			" nickName, email, photo(path), notes, social-[name], num-[name], mail-[name]\n"+ \
			"Or simply:\n"+ \
			"add -s [name] [number]\n\n"+ \
			"Error:\nphoto not found or the values don't match their intended fields\n\n"

HELP_UPDATE = "Update a contact from the database\n\n" + \
			"Usage:\nupdate [contactId] [field]=[value]\n" + \
			"contactId is the id of the contact in databasem if u don't know it, try to figure it out by show command\n"+ \
			"Field might be: firstName, lastName, name, number," + \
			" nickName, email, photo(path), notes, social-[name], num-[name], mail-[name]\n\n"+ \
			"Error:\nid doesn't exist, photo not found or the values don't match their intended fields\n\n"

HELP_REMOVE = "Remove a contact from the database\n\n" + \
			"Usage:\nremove [contactId]\n" + \
			"contactId is the id of the contact in databasem if u don't know it, try to figure it out by show command\n\n"+ \
			"Error:\nid doesn't exist, photo not found or the values don't match their intended fields\n\n"

HELP_SHOW = "Show a contact from the databasem eventually with conditionsm or show all contacts\n\n" + \
			"Usage:\nshow [contactId]\n" + \
			"contactId is the id of the contact in database, if u don't know it, try to figure it out by show command\n\n"+ \
			"Error:\nid doesn't exist\n\n"+ \
			"Usage:\nshow -c [field]=[value]\n" + \
			"Field might be: firstName, lastName, name, number(without indicatif)," + \
			" nickName, email, photo(path), notes, social-[name], num-[name], mail-[name]\n"+ \
			"Usage:\nshow -all\n"

HELP_HELP = "Show help for a specific command\n\n" + \
			"Usage:\nhelp [cmd]\n" + \
			"cmd is a command, 'help' to view all commands\n\n"+ \
			"Error:\ncommand doesn't exist\n\n"
HELP_ALL = "add: add a contact\n"+ \
			"update: update a specific contact\n"+ \
			"remove: remove a specific a contact\n"+ \
			"show: show a specific a contact\n"+ \
			"help [cmd]: show help for a specific command\n"+ \
			"exit: exit phonebookm and save changes\n"


def parse(cmd):
	c = command()
	c.main = cmd.pop(0)
	tmp = 'main'
	c.options['main'] = []
	for i in cmd:
		if i[0] == '-':
			c.options[i] = []
			tmp = i
			continue
		if tmp != '':
			c.options[tmp] += [i]
	return c

def save():
	f = open("data/database.dat", 'wb')
	pickle.dump(contacts, f)
	f.close()

def load():
	global contacts
	if os.path.isfile("data/database.dat"):
		f = open("data/database.dat", 'rb')
		contacts = pickle.load(f)
		f.close()	

def exc(cmd):
	cmd = cmd.split()
	cmd = parse(cmd)
	if(cmd.main == "exit"):
		cmd_exit()
	elif(cmd.main == 'add'):
		cmd_add(cmd)
	elif(cmd.main == 'update'):
		pass
	elif(cmd.main == 'remove'):
		pass
	elif(cmd.main == 'show'):
		pass
	elif(cmd.main == 'help'):
		cmd_help(cmd)

	else:
		err("{} is not recognized".format(cmd.main))
		cmd_help(parse(['help']))
# commands ------------
def cmd_exit():
	global exitCode
	exitCode = 1

def cmd_add(cmd):
	global contacts
	if "-s" in cmd.options:
		if len(cmd.options["-s"]) < 2 or len(cmd.options["-s"]) > 2:
			err("'add -s' parameters are invalid, it accept exectly 2 params [name] [number]")
			return
		c = contact(name = cmd.options["-s"][0].replace("_", " "), number = cmd.options["-s"][1])
	else:
		c = contact()
		for field in cmd.options["main"]:
			field = field.split("=")
			if "-" in field[0]:
				field[0] = field[0].split("-")
				if field[0][0] not in dicoFields:
					err("%s is not a proper field, type 'help add' for more infos" % field[0][0])
					return
				exec("c.%s['%s'] = '%s'" % (dicoFields[field[0][0]], field[0][1], field[1]))
				continue
			if field[0] not in dir(c) or field[0] in ["socialNetworks" , "emails", "numbers"]:
				err("%s is not a proper field, type 'help add' for more infos" % field[0])
				return
			exec("c.%s = '%s'" % (field[0], field[1]))
		contacts += [c]

def cmd_help(cmd):
	if '-all' in cmd.options:
		echo(eval('HELP_ALL'))
		return
	if len(cmd.options['main']) == 0:
		echo(eval('HELP_ALL'))
	elif len(cmd.options['main']) == 1:
		if cmd.options['main'][0] in commands:
			echo(eval('HELP_' + cmd.options['main'][0].upper()))
		else:
			err("{} is not recognized".format(cmd.options['main'][0]))
# --------------------

def initCmd():
	print("\n", "master", ": ", end='', sep="")
	exc(input())

def echo(string):
	print(string, end='')

def err(strErr):
	echo('[!] ')
	echo(strErr + "\n\n")


if not os.path.isdir('data'):
	os.mkdir('data')
if not os.path.isdir('data/images'):
	os.mkdir('data/images')


load()


while(exitCode == 0):
	initCmd()
	save()

