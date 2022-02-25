# DO

1. Install Adafruit_DHT dan RPi.GPIO
2. Klik tombol start it open 2 tab -> total 3 window with the first 1
3. Test your code

# Create environment variables

1. Create `.env` file in root directory
2. Input variables in `.env`
   - `export FLASK_APP=setup.py`
   - `export FLASK_ENV=<your-environment>`

# Create environment

1. `python -m venv env`
2. `pip install -r requirements.txt`

# Run a Server

1. Activate your environment
   - Linux `. env/bin/activate`
   - Windows `env\Scripts\activate`
2. Create table on database (sqlite) `flask create-table`
3. Insert data on table Tools `flask insert`
4. Runnin a server`flask run`
