This document describes how to set up box.net application.

- Sign in to your box.net account
- Go to URL https://www.box.com/developers/services/new_service_terms and create new application.
- Go to URL https://www.box.com/developers/services. You should see the newly created application. Click on "Edit Application".
- On the application's page, in section "Backend parameters" you will find the "Api Key" for that application.
- Copy the "Api Key" value and store it in settings.py file with key BOXNET_APIKEY (BOXNET_APIKEY='<your_api_key>')
- Go to URL https://www.box.net/api/1.0/rest?action=get_ticket&api_key=<your_api_key>. You should receive an XML response which contains a 'ticket' string. 
    An example of an XML response:

        <?xml version='1.0' encoding='UTF-8'?>
        <response>
            <status>get_ticket_ok</status>
        <ticket>bxquuv025arztljze2n438md9zef95e8</ticket>
        </response>

- Now go to URL https://www.box.net/api/1.0/auth/<ticket>, where <ticket> is the obtained ticket, and log in with your credentials.
- Go to URL https://www.box.net/api/1.0/rest?action=get_auth_token&api_key=<your_api_key>&ticket=<ticket>. You should get an XML response, which will look like:

        <?xml version='1.0' encoding='UTF-8'?>
            <response>
                <status>get_auth_token_ok</status>
                <auth_token>9byo5bg8d2o3otp0voji0ej0v49bqcmo</auth_token>
                <user>
                ......
                </user>
            </response>

- Store the <auth_token> value in settings.py with key BOXNET_AUTH_TOKEN (BOXNET_AUTH_TOKEN='<auth_token>')
- That's all. Now you can use the application in docrepo-backend project.

For more information about setting up boxnet application please visit http://developers.box.net/w/page/12923956/ApiOverview