# Keysearch Scraper
A demo scraper for https://www.keysearch.co/ including reCaptcha bypass.


## How to run 

### Pre-requisites
You need Chrome installed in the default location of your system: https://www.google.de/chrome/.
Furthermore you need a .env file with the 2Captcha-python key and the credentials for keysearcher. If you do not have these, send me an email: zrx938@alumni.ku.dk.

### Setup enviorment and project
1. Connect to your server and navigate in the desired directory.

2. Install [miniconda](https://docs.conda.io/projects/continuumio-conda/en/latest/user-guide/install/index.html).
```
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash Miniconda3-latest-Linux-x86_64.sh
```

  
3. Create a virtual enviroment and activate it.
```
conda create --name venvKeysearch python
conda activate venvKeysearch
```

4. Clone repo and install requirements.
```
#clone repo
git clone https://github.com/benjaminkohler96/keysearch-scraper

#move to directory
cd keysearch-scraper

#install requirements
pip install -r requirements.txt
```  

5. Run the script.
```
python keysearch_scrape.py
```

## Contact
If you have any questions or encounter any issues, please contact me: zrx938@alumni.ku.dk
  
