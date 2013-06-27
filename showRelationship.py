#!/bin/python
# -*- coding: utf-8 -*-

import MySQLdb, sys


"""#1#
Извлекаем имена таблиц и информацию по полям в них
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

P = raw_input('Введите имя таблицы, связи с которой нужно найти:')

L = len(r1)
###
#Предполагаем что ссылка на исходную таблицу формируется по принципу
#<имя таблицы>_id
P_id = P +'_id'
r2 = []

for T in r1:

	if T[0] == P:
		T1 = []
		for T0 in T[1:]:
			if T0[0] == 'id':
				T2 = [str(T[0]) + '.' + str(T0[0])]
				T1 += T2
			else:
				T1 += [str(T[0]) + '.' + str(T0[0])]
		r2 += [[T2] + [T1]]
#		r2 += [str(T[0] + '.' + T[1][0])]				#Пишем только имена ключевых полей
	else:
		T1 = []
		for T0 in T[1:]:
			if T0[0] == P_id:
				T2 = [str(T[0]) + '.' + str(T0[0])]
#				r2 += [str(T[0] + '.' + T0[0])]			#Пишем только имена ключевых полей
			else:
				T1 += [str(T[0]) + '.' + str(T0[0])]
		r2 += [[T2] + [T1]]

"""
Генерируем SELECT для просмотра всех полей сJOINных по ключевому полю
искомой таблицы
"""

for T in r2:
	print(T)

