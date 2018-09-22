#!/bin/bash

##########################################
# Send an error email for any exception  #
##########################################
report_error(){
	error_message=$1
	email_id=$2
	echo "-- Sending error email to $email_id --"
	echo "An error has occured while automatically renewing your SSL certificate.
	
Please see below for error details.

Error Message : 
$error_message" | mailx -s "ERROR : Automatic SSL Renewal" $email_id
}

###########################################
# Send an email for successful completion #
###########################################
success_email(){
	message=$1
	email_id=$2
	echo "-- Sending email for successful completion to $email_id --"
	echo "Your SSL certificate for the domain example.com has been renewed successfully.

Please find the logs below.

	$message" | mailx -s "SUCCESS : Automatic SSL Renewal" $email_id
}

###########################################
# Main Program 							  #
###########################################
main(){
	attempt=$1
	echo " "
	echo "--------------------------------"
	echo "-- Attempt Number : $attempt --"
	echo "--------------------------------"
	echo " "
	cd "/path/to/certbot/"
	dir=`pwd`
	if [ $dir == "/path/to/certbot/" ]
	then
		echo "-- Removing all files in certbot directory --"
		rm -f -r *
		echo "-- Executing certbot --"
		certbot certonly --config-dir ~/path/to/certbot --logs-dir ~/path/to/certbot --work-dir ~/path/to/certbot --webroot -w /home/username/www -d example.com -d www.example.com --register-unsafely-without-email --agree-tos
		check_cert=`ls /path/to/certbot/live/example.com/cert.pem`
		check_key=`ls /path/to/certbot/live/example.com/privkey.pem`
		if [ "X$check_cert" == "X" ]
		then
			echo "[X]- Error in checking certificate. Sending Mail -[X]"
			report_error "Attempt Number : $attempt.
			New certificate file is not generated. Probably some error in CERTBOT command" "mail@example.com"
		elif [ "X$check_key" == "X" ]
		then
			echo "[X]- Error in checking Key. Sending Mail -[X]"
			report_error "Attempt Number : $attempt.
			New Key file is not generated. Probably some error in CERTBOT command" "mail@example.com"
		else
			echo "-- Certificate generated successfully --"
			echo "-- Loading Certificate --"
			cert=`cat /path/to/certbot/live/example.com/cert.pem`
			key=`cat /path/to/certbot/live/example.com/privkey.pem`

			echo "-- Executing Certificate Installation Script. Please Wait ... --"
			logs=`python /path/to/python_script/install_ssl_cpanel.py "$cert" "$key"`
			echo "$logs"
			confirm=`echo "$logs" | tail -n1 | cut -d '|' -f 2`
			if [ "X$confirm" == "XSUCCESS" ]
			then
				echo "[OK]- Certificate Installation was Successful -[OK]"
				echo "---------------------------------------------------"
				success_email "Attempt Number : $attempt.
				$logs" "mail@example.com"
			else
				echo "[X]- Certificate Installation Failed -[X]"
				echo "---------------------------------------------------"
				report_error "Attempt Number : $attempt.
				$logs" "mail@example.com"
			fi
		fi
	else
		echo "[X]- Error while starting certbot script -[X]"
		report_error "Attempt Number : $attempt.
		Directory location is not as expected" "mail@example.com"
	fi

	check_webdriver1=`pgrep phantomjs`
	kill -9 $check_webdriver1
	check_webdriver2=`pgrep phantomjs`
	kill -9 $check_webdriver2
}

count=1
main $count
if [ "X$confirm" != "XSUCCESS" ]
then
	count=2
	main $count
	if [ "X$confirm" != "XSUCCESS" ]
	then
		count=3
		main $count
	fi
fi