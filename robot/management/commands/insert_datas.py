# Students/management/commands/insert_students.py
from django.core.management.base import BaseCommand
from robot.models import Robot
import time
import sys

import numpy as np
def create_objects(bulk_size) :
	robot_datas = []
	max_w, max_h = 1000, 1000

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

	return robot_objects

def test_by_batch_size(robot_objects, bulk_size, batch_size) :
	Robot.objects.all().delete() # Robot 테이블에 존재하는 모든 Record 삭제

	loaded_cnt = 0
	for i in range(0, bulk_size, batch_size) :
		loaded_cnt += len(Robot.objects.bulk_create(robot_objects[i:i+batch_size]))

	return loaded_cnt


class Command(BaseCommand):
	help = '로봇 데이터 적재를 시작합니다.'

	def handle(self, *args, **options):
		'''
		데이터 리스트 세팅 및 데이터 적재
		'''

		bulk_size = 100_000

		robot_objects = create_objects(bulk_size=bulk_size)
		start = time.perf_counter() # 시간 측정 시작

		# 소요시간 42.86초, 42.65초, 44.76초 => 평균 : 43.42초
		loaded_cnt = test_by_batch_size(robot_objects, bulk_size, 1)

		# 소요 시간 : 1.84초, 1.95초, 1.83초 => 평균 : 1.87초
		#loaded_cnt = test_by_batch_size(robot_objects, bulk_size, 100)

		# 소요 시간 : 1.91초, 1.92초, 1.91초 => 평균 : 1.91초
		#loaded_cnt = test_by_batch_size(robot_objects, bulk_size, 1_000)

		# 소요 시간 : 2.03초, 2.11초, 2.03초 => 평균 : 2.05초
		#loaded_cnt = test_by_batch_size(robot_objects, bulk_size, 10_000)

		# 소요 시간 2.35초, 2.33초, 2.45초 => 평균 : 2.37초
		#loaded_cnt = test_by_batch_size(robot_objects, bulk_size, 100_000) 

		end = time.perf_counter() # 시간 측정 끝

		self.stdout.write(
			self.style.SUCCESS(f'성공적으로 {loaded_cnt}명의 로봇 데이터를 적재했습니다.')
		)
		self.stdout.write(
			self.style.SUCCESS(f"소요시간: {end - start:.2f}초")
		)
