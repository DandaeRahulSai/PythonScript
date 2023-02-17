import requests 
import datetime
PATH = 'C:/Users/xxxxx/New folder/'
JWT = 'xxxxxxxxxxxxxxxxxxxx'
# Put your USER ID that you get from the API. 
USERID = 'xxxxxx@xxxxx.com'
urlarray = []
filearray = []

headers = {
		'Authorization': 
		'Bearer {}'.format(JWT),
		'content-type':
		'application/json',
	}

def main():
	for year in range(2022,2023):
		for month in range(1,13):
			next_month = month + 1
			next_year = year

			if month == 12:
				next_month = 1
				next_year = year + 1

			start_date = datetime.datetime(year,month,1)
			next_date = datetime.datetime(next_year,next_month,1)

			get_recording(start_date, next_date)
			downloaffromurl()


def get_recording(start_date, next_date):
	
	date_string = '%Y-%m-%d'
	url = 'https://api.zoom.us/v2/users/{}/recordings?page_size=300&from={}&to={}'.format(
				USERID,
				start_date.strftime(date_string),
				next_date.strftime(date_string)
			)

	#print(url)

	response = requests.get(
		url,
		headers=headers
	)

	data = response.json()
	# print('page_count: ', data['page_count'])
	# print('page_size: ', data['page_size'])
	# print(len(data['meetings']))
	# print(data['from'])
	# print(data['to'])

	for meeting in data['meetings']:
		for record in meeting['recording_files']:
			if record['file_type'] == "MP4" and record['recording_type'] == "shared_screen_with_speaker_view":
				download_access_url = '{}?access_token={}'.format(record['download_url'], JWT)
				#print(download_access_url)
				#response = requests.get(download_access_url, stream=True)
				local_filename = '{}{}.mp4'.format(PATH, record['recording_start'].replace(':','-'))
				urlarray.append(download_access_url)
				filearray.append(local_filename)
            
            


	            


def downloaffromurl():
    print('length:'+' '+str(len(urlarray)))
    for idx, i in enumerate(urlarray): 
        with requests.get(i, stream=True) as r:
            with open(filearray[idx], 'wb') as f:
                for chunk in r.iter_content(4096):
                     if chunk:
                            f.write(chunk)
	#print(urlarray)
	#print(filearray)

    
	   
if __name__ == '__main__':
	main()