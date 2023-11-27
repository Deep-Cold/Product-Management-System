import pymysql
def ConnectTodb(Host,User,Passwd,Database):
	try:
		global __db
		__db = pymysql.connect(host=Host,user=User,password=Passwd,database=Database)
		if __db == None:
			return False
		global __Cursor
		__Cursor = __db.cursor()
		__Cursor.execute("show tables like 'prod'")
		if __Cursor.fetchone() == None:
			__Cursor.execute("create table prod(id int,name text,price float,profit float,quantities int,supplier text)")
			__db.commit()
		__Cursor.execute("show tables like 'sales'")
		if __Cursor.fetchone() == None:
			__Cursor.execute("create table sales(id int,name text,quantities int,client text,date text)")
			__db.commit()
	except:
		return False
	return True
def AddNewProd(ilst):
	try:
		ilst[0]=int(ilst[0])
		ilst[1]='"'+str(ilst[1])+'"'
		ilst[2]=float(ilst[2])
		ilst[3]=float(ilst[3])
		ilst[4]=int(ilst[4])
		ilst[5]='"'+str(ilst[5])+'"'
		__Cursor.execute("select * from prod where name = %s" % (ilst[1]))
		if __Cursor.fetchone() != None:
			return False
		__Cursor.execute("select * from prod where id = %s" % (ilst[0]))
		if __Cursor.fetchone() != None:
			return False
		__Cursor.execute("insert into prod(id,name,price,profit,quantities,supplier) values(%s,%s,%s,%s,%s,%s)" % (ilst[0],ilst[1],ilst[2],ilst[3],ilst[4],ilst[5]))
		__db.commit()
	except ValueError:
		return False
	return True
def DeleteProd(id):
	__Cursor.execute("select * from prod where id = %s" % (id))
	__Name ='"'+str(__Cursor.fetchone()[1])+'"'
	__Cursor.execute("delete from sales where name = %s" % (__Name))
	__Cursor.execute("delete from prod where id = %s" % (id))
	__db.commit()
def ShowSearchProd(column,value):
	__Cursor.execute("select * from prod where %s = %s" % (column,value))
	TmpList = list(__Cursor.fetchall())
	ReturnList = []
	for i in range(len(TmpList)):
		ReturnList.append(list(TmpList[i]))
	return ReturnList
def UpdateProd(ilist):
	try:
		ilist[0]=int(ilist[0])
		ilist[1]='"'+str(ilist[1])+'"'
		ilist[2]=float(ilist[2])
		ilist[3]=float(ilist[3])
		ilist[4]=int(ilist[4])
		ilist[5]='"'+ilist[5]+'"'
		__Cursor.execute("select * from prod where name = %s" % (ilist[1]))
		if __Cursor.fetchone() == None:
			return False
		__Cursor.execute("select * from prod where id = %s" % (int(ilist[0])))
		tmp = __Cursor.fetchone()
		if  tmp != None and '"'+tmp[1]+'"' != ilist[1]:
			return False
		__Cursor.execute("update prod set id = %s,price = %s,profit = %s,quantities = %s,supplier = %s where name = %s" % (int(ilist[0]),float(ilist[2]),float(ilist[3]),int(ilist[4]),ilist[5],ilist[1]))
	except ValueError:
		return False
	__db.commit()
	return True
def AddSaleInfo(ilist):
	try:
		ilist[0]=int(ilist[0])
		ilist[1]='"'+str(ilist[1])+'"'
		ilist[2]=int(ilist[2])
		ilist[3]='"'+str(ilist[3])+'"'
		ilist[4]='"'+str(ilist[4])+'"'
		__Cursor.execute("select * from sales where id = %s" % (ilist[0]))
		if __Cursor.fetchone() != None:
			return False
		__Cursor.execute("select * from prod where name = %s" % (ilist[1]))
		if __Cursor.fetchone() == None:
			return False
		__Cursor.execute("select * from prod where name = %s" % (ilist[1]))
		TmpList = list(__Cursor.fetchall())
		__Cursor.execute("update prod set quantities = %s where name = %s" % (int(TmpList[0][4]) - ilist[2],ilist[1]))
		__Cursor.execute("insert into sales(id,name,quantities,client,date) values(%s,%s,%s,%s,%s)" % (ilist[0],ilist[1],ilist[2],ilist[3],ilist[4]))
		__db.commit()
	except ValueError:
		return False
	return True
def DelSaleInfo(ilist):
	try:
		ilist[0]=int(ilist[0])
		ilist[1]='"'+str(ilist[1])+'"'
		ilist[2]=int(ilist[2])
		ilist[3]='"'+str(ilist[3])+'"'
		ilist[4]='"'+str(ilist[4])+'"'
		__Cursor.execute("select * from prod where name = %s" % (ilist[1]))
		if __Cursor.fetchone() == None:
			return
		__Cursor.execute("select * from prod where name = %s" % (ilist[1]))
		TmpList = list(__Cursor.fetchall())
		__Cursor.execute("update prod set quantities = %s where name = %s" % (int(TmpList[0][4]) + ilist[2],ilist[1]))
		__Cursor.execute("delete from sales where id = %s" % (int(ilist[0])))
		__db.commit()
	except ValueError:
		return
def ShowSearchSale(column,value):
	__Cursor.execute("select * from sales where %s = %s" % (column,value))
	TmpList = list(__Cursor.fetchall())
	ReturnList = []
	for i in range(len(TmpList)):
		ReturnList.append(list(TmpList[i]))
	return ReturnList
def ShowAllSale():
	__Cursor.execute("select * from sales")
	TmpList = list(__Cursor.fetchall())
	ReturnList = []
	for i in range(len(TmpList)):
		ReturnList.append(list(TmpList[i]))
	return ReturnList
def ShowAllProd():
	__Cursor.execute("select * from prod")
	TmpList = list(__Cursor.fetchall())
	ReturnList = []
	for i in range(len(TmpList)):
		ReturnList.append(list(TmpList[i]))
	return ReturnList
'''
ConnectTodb('localhost','root','123456','TESTDB')
AddNewProd([1,"'Apple'",1,1,1,"'Apple Inc.'"])
AddSaleInfo([1,"'Apple'",1,"'Huawei Inc.'"])
print(ShowAllProd())
print(ShowAllSale())
'''