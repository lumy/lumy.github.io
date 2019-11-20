
for i in `ls pelican-themes`; do
		echo "Testing $i"
		sed -i "s/THEME=.*/THEME='pelican-themes\/$i'/g" pelicanconf.py 2> /dev/null
		make clean
		make html || exit
		read
done
