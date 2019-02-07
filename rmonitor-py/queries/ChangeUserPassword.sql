UPDATE Login
SET Password = %(password)s,
Salt = %(salt)s
WHERE Username = %(username)s