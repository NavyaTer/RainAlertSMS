# RainAlertSMS


1. The Cronjob from the CloudWatch service triggers the lambda once every hour, 24/7.
2. The lambda then makes a call to the OpenWeatherAPI endpoint using an API key with an HTTP GET request. 
3. I parse the JSON from the response and check if the weather is bad. I also check to the see the previous hour's weather report using the DynamoDB table. Since I am just comparing the current hour's weather code to the previous hours weather code, a simple K-V item in the database was sufficient. 
4. Once the lambda determines it isappropriate to send the message it places it on the SNS topic. I was using the SNS sandbox which allows upto 10 numbersto easily subscribe. Since the requirement was just for less than 5 people this setup was sufficient.
5. To send the SMS, SNS needs an originator number. I used AWS Pinpoint for that.
6. Most of the services are free or nearly free. Below is the system design diagram showing the flow
