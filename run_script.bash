subject='OS'
index='7'
numFiles=$(ls -l *.mp4 | wc -l)

echo "Subject is: ${subject}"
echo "Video number: ${index}"
echo "Number of sub-videos: $numFiles"


if [ $numFiles  -eq  '8' ]
then
		echo "tests"
	fi


	if [ $numFiles  -eq  '12' ]
	then
		MP4Box -cat ${subject}__${index}_part1.mp4 -cat ${subject}__${index}_part2.mp4 -cat ${subject}__${index}_part3.mp4 -cat ${subject}__${index}_part4.mp4 -cat ${subject}__${index}_part5.mp4 -cat ${subject}__${index}_part6.mp4 -cat ${subject}__${index}_part7.mp4 -cat ${subject}__${index}_part8.mp4 -cat ${subject}__${index}_part9.mp4 -cat ${subject}__${index}_part10.mp4 -cat ${subject}__${index}_part11.mp4 -cat ${subject}__${index}_part12.mp4 -cat ${subject}__${index}_part13.mp4 -new ${subject}__${index}.mp4
	fi

	if [ $numFiles  -eq  '11' ]
	then
		MP4Box -cat ${subject}__${index}_part1.mp4 -cat ${subject}__${index}_part2.mp4 -cat ${subject}__${index}_part3.mp4 -cat ${subject}__${index}_part4.mp4 -cat ${subject}__${index}_part5.mp4 -cat ${subject}__${index}_part6.mp4 -cat ${subject}__${index}_part7.mp4 -cat ${subject}__${index}_part8.mp4 -cat ${subject}__${index}_part9.mp4 -cat ${subject}__${index}_part10.mp4 -cat ${subject}__${index}_part11.mp4 -cat ${subject}__${index}_part12.mp4 -new ${subject}__${index}.mp4
	fi

	if [ $numFiles  -eq  '10' ]
	then
		MP4Box -cat ${subject}__${index}_part1.mp4 -cat ${subject}__${index}_part2.mp4 -cat ${subject}__${index}_part3.mp4 -cat ${subject}__${index}_part4.mp4 -cat ${subject}__${index}_part5.mp4 -cat ${subject}__${index}_part6.mp4 -cat ${subject}__${index}_part7.mp4 -cat ${subject}__${index}_part8.mp4 -cat ${subject}__${index}_part9.mp4 -cat ${subject}__${index}_part10.mp4 -cat ${subject}__${index}_part11.mp4 -new ${subject}__${index}.mp4
	fi

	if [ $numFiles  -eq  '9' ]
	then
		MP4Box -cat ${subject}__${index}_part1.mp4 -cat ${subject}__${index}_part2.mp4 -cat ${subject}__${index}_part3.mp4 -cat ${subject}__${index}_part4.mp4 -cat ${subject}__${index}_part5.mp4 -cat ${subject}__${index}_part6.mp4 -cat ${subject}__${index}_part7.mp4 -cat ${subject}__${index}_part8.mp4 -cat ${subject}__${index}_part9.mp4 -cat ${subject}__${index}_part10.mp4 -new ${subject}__${index}.mp4
	fi

	if [ $numFiles  -eq  '9' ]
	then
		MP4Box -cat ${subject}__${index}_part1.mp4 -cat ${subject}__${index}_part2.mp4 -cat ${subject}__${index}_part3.mp4 -cat ${subject}__${index}_part4.mp4 -cat ${subject}__${index}_part5.mp4 -cat ${subject}__${index}_part6.mp4 -cat ${subject}__${index}_part7.mp4 -cat ${subject}__${index}_part8.mp4 -cat ${subject}__${index}_part9.mp4 -new ${subject}__${index}.mp4
	fi

	if [ $numFiles  -eq  '8' ]
	then
		MP4Box -cat ${subject}__${index}_part1.mp4 -cat ${subject}__${index}_part2.mp4 -cat ${subject}__${index}_part3.mp4 -cat ${subject}__${index}_part4.mp4 -cat ${subject}__${index}_part5.mp4 -cat ${subject}__${index}_part6.mp4 -cat ${subject}__${index}_part7.mp4 -cat ${subject}__${index}_part8.mp4 -new ${subject}__${index}.mp4
	fi

	if [ $numFiles  -eq  '7' ]
	then
		MP4Box -cat ${subject}__${index}_part1.mp4 -cat ${subject}__${index}_part2.mp4 -cat ${subject}__${index}_part3.mp4 -cat ${subject}__${index}_part4.mp4 -cat ${subject}__${index}_part5.mp4 -cat ${subject}__${index}_part6.mp4 -cat ${subject}__${index}_part7.mp4 -new ${subject}__${index}.mp4
	fi

	if [ $numFiles  -eq  '6' ]
	then
		MP4Box -cat ${subject}__${index}_part1.mp4 -cat ${subject}__${index}_part2.mp4 -cat ${subject}__${index}_part3.mp4 -cat ${subject}__${index}_part4.mp4 -cat ${subject}__${index}_part5.mp4 -cat ${subject}__${index}_part6.mp4 -new ${subject}__${index}.mp4
	fi

	if [ $numFiles  -eq  '5' ]
	then
		MP4Box -cat ${subject}__${index}_part1.mp4 -cat ${subject}__${index}_part2.mp4 -cat ${subject}__${index}_part3.mp4 -cat ${subject}__${index}_part4.mp4 -cat ${subject}__${index}_part5.mp4 -new ${subject}__${index}.mp4
	fi

	if [ $numFiles  -eq  '4' ]
	then
		MP4Box -cat ${subject}__${index}_part1.mp4 -cat ${subject}__${index}_part2.mp4 -cat ${subject}__${index}_part3.mp4 -cat ${subject}__${index}_part4.mp4 -new ${subject}__${index}.mp4
	fi

	if [ $numFiles  -eq  '3' ]
	then
		MP4Box -cat ${subject}__${index}_part1.mp4 -cat ${subject}__${index}_part2.mp4 -cat ${subject}__${index}_part3.mp4 -new ${subject}__${index}.mp4
	fi

	if [ $numFiles  -eq  '2' ]
	then
		MP4Box -cat ${subject}__${index}_part1.mp4 -cat ${subject}__${index}_part2.mp4 -new ${subject}__${index}.mp4
	fi

