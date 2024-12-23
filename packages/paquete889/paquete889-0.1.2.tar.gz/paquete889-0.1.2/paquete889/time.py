from .modulo import courses

def total():

	return sum(course.duration for course in courses)
