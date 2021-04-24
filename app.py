from flask import Flask,request,render_template
from datetime import datetime
from flask_apscheduler import APScheduler
from flask_mongoengine import MongoEngine


app=Flask(__name__)
app.config['MONGODB_SETTINGS'] ={ 'db' : 'git_log'}

db=MongoEngine()
db.init_app(app)

scheduler = APScheduler()

#id_no=0


@app.route('/')
def log_route():
	database=Github_action.objects.all()
	return render_template('github_log.html',github_log=database)





class Github_action(db.Document):
	#s_no=db.IntField(unique=True)
	user=db.StringField()
	req_id=db.StringField()
	user_action=db.StringField()
	from_branch=db.StringField()
	to_branch=db.StringField()
	timestamp=db.StringField()



@app.route('/git_hook',methods=['POST'])
def webhook():
	github_data=request.json
	#global id_no

	if "pusher" in github_data:
		user_name=github_data["repository"]["owner"]["name"]

		request_id=github_data["commits"][0]["id"]

		action="push"

		temp_brach=github_data["ref"]
		
		list_temp_branch=list(temp_brach.split('/'))
		f_branch=list_temp_branch[-1]
		t_branch=""
		
		timestamp=github_data["commits"][0]["timestamp"]

		date,time=time_conversion(timestamp)
		datetime=date+time

		Github_action(user=user_name, req_id=request_id, user_action=action,from_branch=f_branch,to_branch=t_branch
			,timestamp=datetime).save()
		


	elif "pull_request" in github_data:

		user_name=github_data["pull_request"]["user"]["login"]

		request_id=str(github_data["pull_request"]["id"])

		action="pull"
		
		t_branch=github_data["pull_request"]["head"]["ref"]
		
		f_branch=github_data["pull_request"]["base"]["ref"]
		
		timestamp=github_data["pull_request"]["created_at"]
		
		date,time=time_conversion(timestamp)
		datetime=date+time

		Github_action(user=user_name, req_id=request_id, user_action=action,from_branch=f_branch,to_branch=t_branch
			,timestamp=datetime).save()
		

	return "success"

def time_conversion(received_timedate):

	months={1:"January",2:"February",3:"March",4:"April",5:"May",6:"June",
	7:"July",8:"August",9:"September",10:"October",11:"November",12:"December"}

	date_suffix={1:"st",2:"nd",3:"rd"}

	date,time=received_timedate.split('T')
		
	time=time[:5]
	temp_date=datetime.strptime(time,"%H:%M")
	accurate_time=temp_date.strftime("%I:%M %p")

	date_split=date.split('-')

	accurate_date=date_split[2]

	if date_split[2] in date_suffix:
		accurate_date+=date_split[int(date_split[2])]+" "
	else:
		accurate_date+='th '


	accurate_date+=months[int(date_split[1])]+" "+date_split[0]

	return accurate_date,accurate_time






if __name__=='__main__':
	scheduler.add_job(id = 'Scheduled Task', func=log_route, trigger="interval", seconds=15)
	scheduler.start()
	app.run(debuh=True)