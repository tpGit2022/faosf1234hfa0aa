#! /bin/sh
currentTimeStamp=`date "+%Y_%m_%d_%H_%M_%S"`
#rm -rf email_content.txt
echo $currentTimeStamp
echo $(TZ=UTC-8 date +%Y_%m_%d_%H_%M_%S)
echo $(TZ=UTC-8 date +%Y_%m_%d_%H_%M_%S) >> exec_result.html
