class NpuSimulator:
	#===========================================
	#	NpuSimulator 이니셜라이저
	#===========================================
	def	__init__(self):
		pass

	#===========================================
	#	NpuSimulator 메뉴 출력 메서드
	#===========================================
	def	showmenu(self):
		print('===Mini NPU Simulator===\n')
		print('[모드 선택]\n')
		print('1. 사용자 입력 (3x3)')
		print('2. data.json 분석')

	#===========================================
	#	NpuSimulator 실행 메서드
	#===========================================
	def	run(self):
		#메뉴 선택
		self.showmenu()
		raw_input = input('선택 : ').strip()
		#입력에 대한 검증 처리


		user_input = int(raw_input)
		#메뉴얼 모드
		if user_input == 1:
			self.manual_mode()
		#json 모드
		elif user_input == 2:
			self.json_mode()

	#===========================================
	#	NpuSimulator 메뉴얼 모드 메서드
	#===========================================
	def	manual_mode(self):
		print('--------------------')
		print('[1] 필터 입력')
		print('--------------------')
		#필터 입력
		print('필터 A (3줄 입력, 공백 구분)')
		filter_a = []
		row_a_1 = input().split()
		row_a_2 = input().split()
		row_a_3 = input().split()
		filter_a.append(row_a_1)
		filter_a.append(row_a_2)
		filter_a.append(row_a_3)
		print(filter_a)
		print('필터 B (3줄 입력, 공백 구분)')
		filter_b = []
		row_b_1 = input().split()
		row_b_2 = input().split()
		row_b_3 = input().split()
		filter_b.append(row_b_1)
		filter_b.append(row_b_2)
		filter_b.append(row_b_3)
		print(filter_b)

		print('--------------------')
		print('[2] 패턴 입력')
		print('--------------------')
		#패턴 입력
		print('패턴 (3줄 입력, 공백 구분)')
		pattern = []
		row_pattern_1 = input().split()
		row_pattern_2 = input().split()
		row_pattern_3 = input().split()
		pattern.append(row_pattern_1)
		pattern.append(row_pattern_2)
		pattern.append(row_pattern_3)
		print(pattern)

	#===========================================
	#	NpuSimulator json 모드 메서드
	#===========================================
	def	json_mode(self):
		print('json mode')

#===========================================
#	NpuSimulator 실행 코드
#===========================================
simulator = NpuSimulator()
simulator.run()