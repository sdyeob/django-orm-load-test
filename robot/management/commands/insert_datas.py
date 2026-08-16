# Students/management/commands/insert_students.py
from django.core.management.base import BaseCommand
from robot.models import Robot
import numpy as np
import time
import sys

class Command(BaseCommand):
	help = '로봇 데이터 적재를 시작합니다.'

	def handle(self, *args, **options):
		'''
		데이터 리스트 세팅 및 데이터 적재
		'''

		max_w, max_h = 1000, 1000
		bulk_size = 100000
		robot_datas = []
		cnt = 0

		#self.stdout.write(
		#	self.style.SUCCESS(str(sys.getsizeof({
		#		'robot_id': 0, 'pos_x' : np.random.randint(0, max_w + 1),
		#		'pos_y' : np.random.randint(0, max_h + 1), 'battery' : np.random.randint(0, 101),
		#	}))))

		for i in range(1, bulk_size + 1) :
			robot_datas.append({
				'robot_id': i,
				'pos_x' : np.random.randint(0, max_w + 1),
				'pos_y' : np.random.randint(0, max_h + 1),
				'battery' : np.random.randint(0, 101),
			})

		robot_objects = [
			Robot(robot_id=data['robot_id'], pos_x=data['pos_x'], pos_y=data['pos_y'], battery=data['battery'])
			for data in robot_datas
		]

		start = time.perf_counter() # 시간 측정 시작

		# Test1
		# 한번에 하나의 데이터 적재
		# 소요시간 42.86초, 42.65초, 44.76초 => 평균 : 43.42초
		#for i in range(bulk_size) :
		#	created_robots = Robot.objects.create(
		#		robot_id=robot_objects[i].robot_id,
		#		pos_x=robot_objects[i].pos_x,
		#		pos_y=robot_objects[i].pos_y,
		#		battery=robot_objects[i].battery,
		#		)

		# Test2
		# 한번에 100,000 데이터 적재
		# 소요 시간 2.35초, 2.33초, 2.45초 => 평균 : 2.37초
		#Robot.objects.bulk_create(robot_objects)

		# Test3
		# 100개의 데이터씩 적재
		# 소요 시간 : 1.84초, 1.95초, 1.83초 => 평균 : 1.87초
		for i in range(0, bulk_size, 100) :
			cnt += len(Robot.objects.bulk_create(robot_objects[i:i+100]))

		# Test4
		# 1000개의 데이터씩 적재
		# 소요 시간 : 1.91초, 1.92초, 1.91초 => 평균 : 1.91초
		#for i in range(0, bulk_size, 1_000) :
		#	Robot.objects.bulk_create(robot_objects[i:i+1_000])

		# Test5
		# 10000개의 데이터씩 적재
		# 소요 시간 : 2.03초, 2.11초, 2.03초 => 평균 : 2.05초
		#for i in range(0, bulk_size, 10_000) :
		#	Robot.objects.bulk_create(robot_objects[i:i+10_000])

		end = time.perf_counter() # 시간 측정 끝

		self.stdout.write(
			self.style.SUCCESS(f'성공적으로 {cnt}명의 로봇 데이터를 적재했습니다.')
		)
		self.stdout.write(
			self.style.SUCCESS(f"소요시간: {end - start:.2f}초")
		)
