from django.shortcuts import render
from .models import Robot

# Create your views here.
def print_robot_infos(request) :
	robot_infos = Robot.objects.all()[:100] # 100개의 데이터만 추출

	return render(
		request,
		'robot/robot_info_template.html',
		{
			'robot_infos' : robot_infos
		},
	)
