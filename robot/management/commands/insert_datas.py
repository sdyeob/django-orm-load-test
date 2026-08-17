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

def test_by_batch_size(robot_objects:list[Robot], bulk_size: int, batch_size: int)->int :
	Robot.objects.all().delete() # Robot 테이블에 존재하는 모든 Record 삭제

	loaded_cnt = 0
	for i in range(0, bulk_size, batch_size) :
		loaded_cnt += len(Robot.objects.bulk_create(robot_objects[i:i+batch_size]))

	return loaded_cnt

def time_check(robot_objects:list[Robot], bulk_size: int, batch_size: int):
	avg_time = 0
	iter_cnt = 3
	for _ in range(iter_cnt) :
		start = time.perf_counter() # 시간 측정 시작

		# 소요 시간 : 1.64초, 1.66초, 1.62초 => 평균 : 1.64초
		loaded_cnt = test_by_batch_size(robot_objects, bulk_size, batch_size)

		end = time.perf_counter() # 시간 측정 끝
		avg_time += end - start

	return (loaded_cnt, (avg_time / iter_cnt))


class Command(BaseCommand):
	help = '로봇 데이터 적재를 시작합니다.'

	def handle(self, *args, **options):
		'''
		데이터 리스트 세팅 및 데이터 적재
		'''

		bulk_size = 100_000

		robot_objects = create_objects(bulk_size=bulk_size)
		loaded_cnt, avg_time = time_check(robot_objects, bulk_size, 100000)

		self.stdout.write(
			self.style.SUCCESS(f'성공적으로 {loaded_cnt}명의 로봇 데이터를 적재했습니다.')
		)
		self.stdout.write(
			self.style.SUCCESS(f"소요시간: {avg_time:.2f}초")
		)
