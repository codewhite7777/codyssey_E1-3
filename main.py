import	time

class NpuSimulator:
	#===========================================
	#	NpuSimulator 상수
	#===========================================
	EPSILON = 1e-9    # 0.000000001

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
	#	NpuSimulator 입력 값 검증 메서드 - 공백
	#===========================================
	def	is_empty_space(self, value):
		if value == '':
			return True
		return False

	#===========================================
	#	NpuSimulator 입력 값 검증 메서드 - 문자열
	#===========================================
	def	is_str(self, value):
		try:
			num = float(value)
			return False
		except ValueError:
			return True

	#===========================================
	#	NpuSimulator 메트릭스 입력 처리 메서드
	#===========================================
	def input_matrix(self):
		matrix = []
		while len(matrix) < 3:
			tmp = input().split()
			if len(tmp) != 3:
				print('입력 형식 오류: 3개의 값만 입력 가능합니다.')
				continue
			valid = True
			for j in range(3):
				try:
					tmp[j] = float(tmp[j])
				except ValueError:
					print('입력 형식 오류: 숫자만 입력 가능합니다.')
					valid = False
					break
			if valid:
				matrix.append(tmp)
		return matrix

	#===========================================
	#	NpuSimulator MAC 계산 처리 메서드
	#===========================================
	def	cal_mac(self, pattern, filter_matrix):
		score = 0.0
		for i in range(len(pattern)):
			for j in range(len(pattern)):
				score += pattern[i][j] * filter_matrix[i][j]
		return score

	#===========================================
	#	NpuSimulator 결과 값 판정 처리 메서드
	#===========================================
	def	judge(self, score_a, score_b):
		if abs(score_a - score_b) < self.EPSILON:
			return '판정 불가'
		elif score_a > score_b:
			return 'A'
		else:
			return 'B'

	#===========================================
	#	NpuSimulator 실행 프로파일링 처리 메서드
	#===========================================
	def	profile_performance(self, pattern, filter_matrix, repeat = 10):
		times = []
		for _ in range(repeat):
			start = time.perf_counter()
			self.cal_mac(pattern, filter_matrix)
			end = time.perf_counter()
			times.append((end - start) * 1000)
		avg_ms = sum(times) / len(times)
		return avg_ms



	#===========================================
	#	NpuSimulator 실행 메서드
	#===========================================
	def	run(self):
		while True:
			#메뉴 선택
			self.showmenu()
			raw_input = input('선택 : ').strip()
			#입력값 검증 처리
			if self.is_empty_space(raw_input) == True or self.is_str(raw_input) == True:
				print('공백 또는 숫자가 아닌 값이 입력되었습니다.')
				continue
			if raw_input not in ('1', '2'):
				print('1 또는 2를 입력하세요.')
				continue
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
		#필터 입력
		print('--------------------')
		print('[1] 필터 입력')
		print('--------------------')
		print('필터 A (3줄 입력, 공백 구분)')
		filter_a = self.input_matrix()
		print('필터 B (3줄 입력, 공백 구분)')
		filter_b = self.input_matrix()
		#패턴 입력
		print('--------------------')
		print('[2] 패턴 입력')
		print('--------------------')
		print('패턴 (3줄 입력, 공백 구분)')
		pattern = self.input_matrix()
		#MAC 연산 (Multiply Accumulate)
		r1 = self.cal_mac(pattern, filter_a)
		r2 = self.cal_mac(pattern, filter_b)
		#판정 처리
		jud_result = self.judge(r1, r2)
		#시간 체크
		avg_result = self.profile_performance(pattern, filter_a)
		#결과 판정
		print('--------------------')
		print('[3] MAC 결과')
		print('--------------------')
		print('A 점수 : ', r1)
		print('B 점수 : ', r2)
		print(f'연산 시간(평균/10회) : {avg_result}ms')
		print('판정 : ',jud_result)
		# 성능 분석 표
		print('--------------------')
		print('[4] 성능 분석 (평균/10회)')
		print('--------------------')
		print(f'{"크기":<10} {"평균 시간(ms)":<15} {"연산 횟수"}')
		print('-' * 40)
		n = 3
		print(f'{n}×{n:<10} {avg_result:<20.7f} {n * n}')
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