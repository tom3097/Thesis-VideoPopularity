#!/bin/sh

printf "montage " > __create_collage.sh 
cat $1 | while read i ;
do
printf "$i " >> __create_collage.sh
done
printf " -geometry 256x256+0+0 -tile 10x10 collage.png" >> __create_collage.sh

chmod +x __create_collage.sh

./__create_collage.sh

rm __create_collage.sh
