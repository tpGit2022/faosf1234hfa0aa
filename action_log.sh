#! /bin/sh
currentTimeStamp=`date "+%Y_%m_%d_%H_%M_%S"`
#rm -rf email_content.txt
echo $currentTimeStamp:Run Github Action, Runtime Env IP: >> email_content.txt
curl ip.sb >> email_content.txt
echo The File List After Checkout And Compile
ls -RF >> email_content.txt