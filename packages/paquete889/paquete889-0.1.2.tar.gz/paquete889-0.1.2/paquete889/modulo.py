class Course:

	def __init__(self, name, duration, link):
		self.name = name
		self.duration = duration
		self.link = link

	def __repr__(self):
		return f"{self.name}, {self.duration}, {self.link}"	

courses = [
	Course("introduccion a linux", 15, "hack4u.io/linux"),
	Course("perzonalizacion en linux", 3, "hack4u.io/per"),
	Course("hacking", 53, "hack4u.io/hacking")

]

def list_courses():	

	for course in courses:
		print(course)
	
def search_courses_by_name(name):
	for course in courses:
		if course.name == name:
			return course
	return None	

if __name__ == '__main__':
	list_courses()
