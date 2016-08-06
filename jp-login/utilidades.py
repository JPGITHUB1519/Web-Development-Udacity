import sqlite3
import time
import re

class Utilidades :

	def __init__(self) :

		self.con = sqlite3.connect("basedatos.db")
		self.c = self.con.cursor()
		self.user_check = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
		self.password_check = re.compile(r"^.{3,20}$")

	def ejecuta(self, string) :
		self.c.execute(string)
		data = self.c.fetchall()
		self.con.commit()
		self.c.close()
		return data

	def validate_user(nombre) :

		return self.user_check.match(nombre)

	def validate_password(password) :

		return self.password_check.match(password)

	def get_date(self) :

		return time.strftime("%x")

	def signup_user(self, nombre, password) :

		cond = False

		try:
			fecha_actual = self.get_date()
			cmd = "insert into usuarios values ('%(nombre)s', '%(password)s', '%(fecha_actual)s')" % {"nombre" : nombre, "password" : password, "fecha_actual" : fecha_actual}
			self.ejecuta(cmd)
			cond = True

		except Exception, e:
			
			raise

		return cond

	def delete_user(self, nombre) :

		cond = False

		if self.check_exits(nombre) == True : 
			try:
				# re open cursor
				self.c = self.con.cursor()
				cmd = "delete from usuarios where nombre = '%s'" % nombre
				self.ejecuta(cmd)
				cond = True

			except Exception, e:
				raise
		return cond

	def update_user(self, nombre, new_nombre, password) :

		cond = False

		if self.check_exits(nombre) :
			self.c = self.con.cursor()
			if self.check_exits(new_nombre) == False :
				try:
					self.c = self.con.cursor()
					cmd = "update usuarios set nombre = '%(new_nombre)s', password = '%(password)s' where nombre = '%(nombre)s' " % {"nombre" : nombre, "password" : password, "new_nombre" : new_nombre}
					self.ejecuta(cmd)
					cond = True

				except Exception, e:
					raise	

		return cond				


	def check_exits(self, nombre) :

		data = self.ejecuta("select * from usuarios where nombre = '%s' " % nombre)

		if len(data) > 0 :

			return True

		return False

	def get_all_users(self) :

		data = self.ejecuta("select * from usuarios")

		return data


# utilidades = Utilidades()

# print utilidades.update_user("a", "pedro", 3)


# fec = utilidades.get_date()
# utilidades.ejecuta("insert into usuarios values ('Juan2','0', '%s')" % fec)

# we have to put null for autoincrement
#utilidades.ejecuta("insert into usuarios values (NULL,'Juan','0')")
