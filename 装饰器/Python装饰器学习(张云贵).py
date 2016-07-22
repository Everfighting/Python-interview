# -*- coding:gbk -*-
'''��һ������򵥵ĺ�����׼�����Ӷ��⹦��'''
'''ʾ��1����򵥵ĺ�������ʾ����������'''

def myfunc():
	print ("myfunc() called.")

myfunc()
myfunc()



'''�ڶ�����ʹ��װ�κ����ں���ִ��ǰ��ִ�к�ֱ𸽼Ӷ��⹦��'''
'''ʾ��2: �滻����(װ��)
װ�κ����Ĳ����Ǳ�װ�εĺ������󣬷���ԭ��������
װ�ε�ʵ�����: myfunc = deco(myfunc)'''

def deco(func):
	print("before myfunc() called.")
	func()
	print("  after myfunc() called.")
	return func

def myfunc():
	print(" myfunc() called.")

myfunc = deco(myfunc)

myfunc()
myfunc()



'''��������ʹ���﷨��@��װ�κ���'''
'''ʾ��3: �൱�ڡ�myfunc = deco(myfunc)��
�������º���ֻ�ڵ�һ�α����ã���ԭ�����������һ��'''

def deco(func):
	print("before myfunc() called.")
	func()
	print("  after myfunc() called.")
	return func

@deco
def myfunc():
	print(" myfunc() called.")

myfunc()
myfunc()



'''���Ĳ���ʹ����Ƕ��װ������ȷ��ÿ���º�����������'''
'''ʾ��4: ʹ����Ƕ��װ������ȷ��ÿ���º����������ã�
��Ƕ��װ�������βκͷ���ֵ��ԭ������ͬ��װ�κ���������Ƕ��װ��������'''

def deco(func):
	def _deco():
		print("before myfunc() called.")
		func()
		print("  after myfunc() called.")

	# ����Ҫ����func��ʵ����Ӧ����ԭ�����ķ���ֵ
	return _deco

@deco
def myfunc():
	print(" myfunc() called.")
	return 'ok'

myfunc()
myfunc()



'''���岽���Դ������ĺ�������װ��'''
'''ʾ��5: �Դ������ĺ�������װ�Σ�
��Ƕ��װ�������βκͷ���ֵ��ԭ������ͬ��װ�κ���������Ƕ��װ��������'''

def deco(func):
	def _deco(a, b):
		print("before myfunc() called.")
		ret = func(a, b)
		print("after myfunc() called. result: %s" % ret)
		return ret
	return _deco

@deco
def myfunc(a, b):
	print(" myfunc(%s,%s) called." % (a, b))
	return a + b

myfunc(1, 2)
myfunc(3, 4)



'''���������Բ���������ȷ���ĺ�������װ��'''
'''ʾ��6: �Բ���������ȷ���ĺ�������װ�Σ�
������(*args, **kwargs)���Զ���Ӧ��κ���������'''

def deco(func):
	def _deco(*args, **kwargs):
		print("before %s called." % func.__name__)
		ret = func(*args, **kwargs)
		print("  after %s called. result: %s" % (func.__name__, ret))
		return ret
	return _deco

@deco
def myfunc(a, b):
	print(" myfunc(%s,%s) called." % (a, b))
	return a + b

@deco
def myfunc2(a, b, c):
	print(" myfunc2(%s,%s,%s) called." % (a, b, c))
	return a + b + c

myfunc(1, 2)
myfunc(3, 4)
myfunc2(1, 2, 3)
myfunc2(3, 4, 5)



'''���߲�����װ����������'''
'''ʾ��7: ��ʾ��4�Ļ����ϣ���װ������������
����һʾ�������������һ���װ��
װ�κ�����ʵ����Ӧ��������Щ'''

def deco(arg):
	def _deco(func):
		def __deco():
			print("before %s called [%s]." % (func.__name__, arg))
			func()
			print("after %s called [%s]." % (func.__name__, arg))
		return __deco
	return _deco

@deco("mymodule")
def myfunc():
	print("myfunc() called.")

@deco("module2")
def myfunc2():
	print("myfunc2() called.")

myfunc()
myfunc2()



'''�ڰ˲�����װ�����������'''
'''ʾ��8: װ�����������'''
class locker:
	def __init__(self):
		print("locker.__init__() should be not called.")

	@staticmethod
	def acquire():
		print("locker.acquire() called.�����Ǿ�̬������")

	@staticmethod
	def release():
		print("  locker.release() called.������Ҫ����ʵ����")

def deco(cls):
	'''cls ����ʵ��acquire��release��̬����'''

	def _deco(func):
		def __deco():
			print("before %s called [%s]." % (func.__name__, cls))
			cls.acquire() #������ķ���
			try:
				return func()
			finally:
				cls.release()
		return __deco
	return _deco

@deco(locker)
def myfunc():
	print(" myfunc() called.")

myfunc()
myfunc()



'''�ھŲ���װ����������������ֲ𹫹��ൽ����py�ļ��У�ͬʱ��ʾ�˶�һ������Ӧ�ö��װ����'''
'''mylocker.py: ������ for ʾ��9.py'''

class mylocker:
	def __init__(self):
		print("mylocker.__init__() called.")

	@staticmethod
	def acquire():
		print("mylocker.acquire() called.")

	@staticmethod
	def unlock():
		print("mylocker.unlock() called.")

class lockerex(mylocker):
	@staticmethod
	def acquire():
		print("lockerex.acquire() called.")

	@staticmethod
	def unlock():
		print("  lockerex.unlock() called.")

def lockhelper(cls):
	'''cls ����ʵ��acquire��release��̬����'''
	def _deco(func):
		def __deco(*args, **kwargs):
			print("before %s called." % func.__name__)
			cls.acquire()
			try:
				return func(*args, **kwargs)
			finally:
				cls.unlock()
		return __deco
	return _deco


'''ʾ��9: װ����������������ֲ𹫹��ൽ����py�ļ���
ͬʱ��ʾ�˶�һ������Ӧ�ö��װ����'''

from mylocker import *

class example:
	@lockhelper(mylocker)
	def myfunc(self):
		print(" myfunc() called.")

	@lockhelper(mylocker)
	@lockhelper(lockerex)
	def myfunc2(self, a, b):
		print(" myfunc2() called.")
		return a + b

if __name__ == "__main__":
	a = example()
	a.myfunc()
	print(a.myfunc())
	print(a.myfunc2(1, 2))
	print(a.myfunc2(3, 4))