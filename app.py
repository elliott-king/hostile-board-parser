import json
import io
import sys
import urllib

from flask import Flask, request
from pyresparser import ResumeParser

app = Flask(__name__)

# Taken from pyresparser cli 
def extract_resume(url, skills_file=None, custom_regex=None):
  try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urllib.request.urlopen(req).read()
    _file = io.BytesIO(webpage)
    _file.name = 'test.pdf' # the name is only really needed to identify the extension
    resume_parser = ResumeParser(_file, skills_file, custom_regex)
    return [resume_parser.get_extracted_data()]
  except urllib.error.HTTPError:
    print('File not found. Please provide correct URL for resume file')
    sys.exit(1)

@app.route('/parse', methods=['POST'])
def parse():
  try:
    url = request.get_json()['url']
    print(url)
    e = extract_resume(url)
    print(e)
    return e[0]
  except Exception as e:
    print(e)
    raise e