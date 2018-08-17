def h():
    print 'aaaaa'
    #yield aaa()
    print 'bbbb'
    yield aaa()
    yield 'a'

    
def aaa():
    print  '111'
    return 'jajja'
if __name__ == '__main__':
    h=h()
    h()
    m=h.next()
   # h.next()

    
    
