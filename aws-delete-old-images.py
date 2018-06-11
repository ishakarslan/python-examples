import simplejson as json
import os
import subprocess
import dateutil.parser
from datetime import *

ZERO = timedelta(0)

class UTC(tzinfo):
  def utcoffset(self, dt):
    return ZERO
  def tzname(self, dt):
    return "UTC"
  def dst(self, dt):
    return ZERO

def load_json_multiple(segments):
    chunk = ""
    for segment in segments:
        chunk += segment
        try:
            yield json.loads(chunk)
            chunk = ""
        except ValueError:
            pass

def open_and_read(komut):
    result = subprocess.check_output(komut, shell=True)
    return result

def delete_func(imaj):
    #os.system("ec2 delete {0}}".format(imaj))
    print("{0} imaj silme komutu calistirildi".format(imaj))

def parse_json(parse):
   utc = UTC()
   now = datetime.now(utc)
   for parsed_json in load_json_multiple(parse):
      tarih=parsed_json['CreationDate']
      imageno=parsed_json['ImageId']
      insertion_date = dateutil.parser.parse(tarih)
      time_between_insertion = now - insertion_date
      if  time_between_insertion.days>30:
          print "Date older than 30 days"
          print tarih, imageno
	  delete_func(imageno) ## attention

      else:
          print "Date newer than 30 days"
          print tarih, imageno

def main():
    parse_json(open_and_read("aws ec2 describe-images"))

if __name__ == "__main__":
    main()
