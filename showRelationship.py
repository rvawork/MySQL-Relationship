#!/bin/python
# -*- coding: utf-8 -*-

import MySQLdb, sys


host = raw_input('Введите имя/адрес сервера БД: ')
user = raw_input('Введите имя пользователя для доступа к базе: ')
passwd = raw_input('Введите пароль: ')
db = raw_input('Введите имя БД: ')

"""#1#
Извлекаем имена таблиц и информацию по полям в них
[u'virtual_fs_preferences', (u'virtual_fs_id', u'bigint(20)', u'NO', u'MUL', None, u''), 
(u'preferences_key', u'varchar(150)', u'NO', u'MUL', None, u''), 
(u'preferences_value', u'text', u'YES', u'', None, u'')]
"""
r1 = []
try:
	con = MySQLdb.connect(host, user, passwd, db)

	cur_I = con_I.cursor()
	cur_I.execute("SHOW TABLES")
	result_0 = cur_I.fetchall()
	
	for R in result_0:
		cur_I.execute("SHOW COLUMNS FROM %s" % str(R[0]))
		r1 += [['%s'%R[0]] + list(cur_I.fetchall())]

	con_I.close()
except MySQLdb.Error:
	print(db.error())


"""#2#
Ищем связи с искомой таблицей в полях всех таблиц!
На выходе имеем список, где значения элементов(списки):
[0] '<имя таблицы>.<имя ключевого поля>'
[1] список полей в формате '<имя таблицы>.<имя поля>'

EXAMPLE:
[[['tbl_1.id'],['tbl_1.column1', ... , 'tbl_1.columnN']],
 ...,
 [['tbl_X.id'],['tbl_X.column1', ... , 'tbl_X.columnN']]]
"""

P = raw_input('Введите имя таблицы, связи с которой нужно найти: ')


###
#Предполагаем что ссылка на исходную таблицу формируется по принципу
#<имя таблицы>_id
P_id = P +'_id'
r2 = []

for T in r1:
	Flag = 0
	if T[0] == P:
		T1 = []
		for T0 in T[1:]:
			if T0[0] == 'id':
				T2 = [str(T[0]) + '.' + str(T0[0])]
				T1 += [str(T0[0])]
			else:
				T1 += [str(T0[0])]
		r2 += [[T2] + [T1]]

	else:
		T1 = []
		for T0 in T[1:]:
			if T0[0] == P_id:
				Flag = 1
				T2 = [str(T[0]) + '.' + str(T0[0])]
			else:
				T1 += [str(T0[0])]
		if Flag == 1:
			r2 += [[T2] + [T1]]

"""
Генерируем SELECT для просмотра всех полей сJOINных по ключевому полю
искомой таблицы
"""
ID = raw_input('Введите номер заявки: ')

Columns = ''
Join = ''
Where = """WHERE %s.id = '%s'""" % (P, ID)

i = 0
L = len(r2)

while i != L:
	for T in r2[i][0]:
		if i == 0:
			Join += """%s AS T0""" % (T.split(',')[0])
			T0_id = T
	else:
		Join += """ JOIN %s ON %s = %s""" % (T.split(',')[0], T0_id, T)

	for T in r2[i][1]:
		Columns += """ T%s.%s,""" % (i, T)
	i += 1
	



S = """'SELECT %s FROM %s %s;'""" % (Columns[:-1], Join, Where)
print(S)

