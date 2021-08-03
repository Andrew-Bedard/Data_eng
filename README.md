# Data_eng
THA: Data Engineer assignment

web_page.py contains the flask web app.

Web url can be accessed using url "<localhost>/campaigns/{campaign_id}"
  
Performance metrics were performed using locust, and can be run using locustfile.py, performance on my localhost easily exceeds 5000 requests/minute. Screen shots of performance as tested locally are available as 'stress_tests.png'

All banner logic functions are in banner_logic.py, this includes dat_check, which checks for duplicate csv files and changes the extension of the newest duplicate files to avoid capture by loading function, and saves this information in a log.txt file. load_frames will load appropriate csv into dataframes based on datetime. get_banners will select the appropriate banners for a given campaign based on the business rules, as well as the option to 'black list' banners that have just been shown to a specific individual.
  
There is currently no AWS implementation as the route that I had chosen provided too many issues, and I was unable to fix them in time.
