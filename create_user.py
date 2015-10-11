from models import *
import sys, sqlalchemy

try:
  if len(sys.argv) in [3,4] :
    User(name=sys.argv[1], password=sys.argv[2], role = sys.argv[3]).save()
  else:
    print 'Wrong parameters has been set'
    print '>>python create_user.py username password role'
except sqlalchemy.exc.IntegrityError:
  print "User has already exist"