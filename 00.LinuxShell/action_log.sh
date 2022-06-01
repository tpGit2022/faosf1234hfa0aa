#! /bin/sh
currentTimeStamp=`date "+%Y_%m_%d_%H_%M_%S"`
#rm -rf email_content.txt
echo 当前环境时间:$currentTimeStamp
echo 当前北京时间:$(TZ=UTC-8 date +%Y_%m_%d_%H_%M_%S)
echo $(TZ=UTC-8 date +%Y_%m_%d_%H_%M_%S) >> exec_result.html
