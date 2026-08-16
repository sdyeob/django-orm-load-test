from django.core.management.base import BaseCommand
from robot.models import Robot

class Command(BaseCommand) :
	help='Robot 테이블의 모든 record를 삭제'

	def handle(self, *args, **options) :
		data_counts = Robot.objects.count()
		all_datas = Robot.objects.all()
		all_datas.delete()

		self.stdout.write(
			self.style.SUCCESS(f'성공적으로 {data_counts}개의 데이터를 삭제했습니다.')
		)

