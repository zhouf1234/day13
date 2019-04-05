from functools import wraps

def wrapper(func):
    @wraps(func)
    def inner(*args,**kwargs):
        print('前方执行')
        func()
        print('后方执行')
    return inner

@wrapper
def f():
    '''
    这是用来测试装饰器修复的函数
    :return:
    '''
    print('ok')

if __name__=='__main__':
    print(f.__name__)
    print(f.__doc__)
    print(f.__dict__)