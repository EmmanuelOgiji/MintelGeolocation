# MintelGeolocation

##Overview 
This python3 project comprises of the following:
- the src directory houses an application which does the following:
    - Gets a list of ip addresses from the ip_addresses.txt file. These serve to represent the IP addresses from the users in the scenario given. The IP Addresses were sourced from [TOR's exit relay list](https://check.torproject.org/torbulkexitlist). There are 550 ip addresses included in the file. This satisfies the sample size requirement of greater than 500 but below 10000. Capability was added as well to allow another text file be used if needed.
    - For each of these ip addresses:
        - uses the [IP-API Geolocation API](https://ip-api.com/docs/api:json) to get details on the location/geolocation of this IP address. Note that this API has a limit of 45 requests/minute thus retry mechanism and exponential backoff are used.
        - uses the location details to get details on the weather in that location. This is done using the [OpenWeatherMapAPI](https://openweathermap.org/current)
        - creates a data frame holding all of this information
        - add said data frame to a csv file (called output.csv)
    - Then uses the output to produce and display groups, aggregations and visualizations. These include:
        - Grouping:
            - Grouping the data by city, country and region
            - Displaying Details on IPs from region:Quebec
            - Displaying Details on IPs from the country:USA
            - Displaying Details on IPs from the city:Seattle
        - Aggregation and Visualizations:
            - Aggregation: Average Temperature in Countries
            - Aggregation: Mean Max/Min Temperature in Countries
            - Figure 1: Bar chart comparing Average Temperature in Countries
            - Figure 2: Bar chart comparing Mean Max/Min Temperature in Countries
- the test directory contains unit tests that utilize mocking to just check the functionality of the application
- a Dockerfile used to build a Docker image with the application. This is used to satisfy the requirements for the deployment process to be **repeatable**, be run using **docker** and **via a single command**
- the .circleci directory contains a config.yml file which uses CircleCI to put in a CI/CD pipeline for the application. The pipeline:
    - runs the unit tests and produces xml reports based on that. This happens for any branch on the repository
    - builds and pushes the docker image to Dockerhub. The image can be found on Dockerhub [here](https://hub.docker.com/repository/docker/emmaogiji/mintelweather)
    - The pipeline project and all the builds are available [here](https://app.circleci.com/pipelines/github/EmmanuelOgiji/MintelGeolocation). Access to that can be requested if needed
- a requirements.txt file containing all the python dependencies of the project. These can be installed using **pip install -r requirements.txt** from the root of this repository


##Usage:
- Run locally:
    with dependencies installed, to run the application, from the root of the repository, run the following commands:
    - cd src
    - python main.py --ips ip_addresses.txt
    - Note: Running this application locally requires **LOCATION_API_KEY** and **WEATHER_API_KEY** to be set as environment variables with their values being an API key for the IP Geolocation API and the OpenWeathermap API respectfully.
 
- Run tests:
    with dependencies installed, to run the application, from the root of the repository, run the following commands:
    - python -m unittest discover -s test
    
- Run with docker (following the requirements)
  - docker run emmaogiji/mintelweather:latest

##Notes:
- Due to the limitation of the API used, the code does take a significant amount of time to run. The API was favoured over others due to the fact that most others had daily limits. This limitation is also the reason behinf the number of ip addresses (samples) used being near the floor of the range given.