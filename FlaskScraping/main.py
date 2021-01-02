from save import save_to_file
from so import get_jobs as get_so_jobs
from indeed import get_jobs as get_indeed_jobs
from flask import Flask, render_template, request, redirect, send_file
# render_template -> Flask에서 html을 렌더링 할 수 있게 해주는 용어
# request -> 필요한 단어를 뽑아내는 역할


# app 이름을 설정해준다
app = Flask("SuperScraper")

db = {}

# @: decorator
# decorator는 "바로 아래에 있는 함수"를 찾아 꾸며주는 역할을 함
@app.route("/")
def home():
	return render_template("index.html")
    

# Dynamic URL username을 DB에서 찾아서 결과 값을 보여준다
@app.route("/report")
def report():
	word = request.args.get('word')
	if word:	# 검색 결과를 통일시켜주자
		word = word.lower()
		existingJobs = db.get(word)
		if existingJobs:
			jobs = existingJobs
		else:
			jobs = get_indeed_jobs(word)
			jobs += get_so_jobs(word)
			db[word] = jobs
	else:		# None을 반환하지 않도록 해주자
		return redirect("/")
	return render_template(
		"report.html", searchingBy=word, results_number=len(jobs), jobs=jobs
	)

# 만든 홈페이지를 csv파일로 내보내기 위함
@app.route("/export")
def export():
	try:
		word = request.args.get('word')
		if not word:
			# try block 내에서 Exception이 raise되면 except문 안의 내용이 실행되게 만듬
			raise Exception()
		word = word.lower()
		jobs = db.get(word)
		if not jobs:
			raise Exception()
		save_to_file(jobs)
		return send_file("jobs.csv")
	except:
		return redirect("/")
	
		


# repl.it에서 사용하기 위해 host를 따로 설정해준 것
app.run(host="0.0.0.0")
