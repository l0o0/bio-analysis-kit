for i in $(ls  $1/${2}*/*gz)
do
    filename=$(basename $i)
    dirname=$(basename ${i%/*}) 
    #echo $filename $dirname
    ln -s $i $3/${dirname}_${filename}
done
