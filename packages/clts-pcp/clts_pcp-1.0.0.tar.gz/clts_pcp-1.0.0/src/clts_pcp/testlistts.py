import time
import clts

clts.setcontext('Testing lts v2')

tstart=clts.getts()
print (tstart)
time.sleep(2.2)

clts.elapt["step 1 (successful)."]=clts.deltat(tstart)
t1=clts.getts()

time.sleep(3.1)

clts.elapt["step 2 (successful)."]=clts.deltat(tstart)

clts.elapt["step 1-2 (successful)."]=clts.deltat(t1)



#lts.listtimes()

print (clts.listtimes())


exit(8)

# twine upload --repository-url https://lts.pypi.org/legacy/ dist/*

