set d=%date:~0,10%
set t=%time:~0,8%
git add .
git commit -m  "%d%_%t%"
git push origin master
