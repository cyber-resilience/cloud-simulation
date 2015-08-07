import subprocess
i=0
while i<10:
	subprocess.Popen(["python","cputest.py"])
	i=i+1
