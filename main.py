import	time
import	json

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
		print('3. 종료')

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
	def	judge(self, score_a, score_b, label_a='A', label_b='B'):
		if abs(score_a - score_b) < self.EPSILON:
			return 'UNDECIDED'
		elif score_a > score_b:
			return label_a
		else:
			return label_b

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
	#	NpuSimulator json data 로드 메서드
	#===========================================
	def	load_json(self):
		try:
			with open('data_v2.json') as f:
				data = json.load(f)
				return data
		except	FileNotFoundError:
			print('data.json 파일을 찾을 수 없습니다.')
			return None
		except json.JSONDecodeError:
			print('data.json 파일 형식이 올바르지 않습니다.')
			return None

	#===========================================
	#	NpuSimulator 실행 메서드
	#===========================================
	def	run(self):
		while True:
			# 메뉴 선택
			self.showmenu()
			raw_input = input('선택 : ').strip()
			# 입력값 검증 처리
			if self.is_empty_space(raw_input) == True or self.is_str(raw_input) == True:
				print('공백 또는 숫자가 아닌 값이 입력되었습니다.')
				continue
			if raw_input not in ('1', '2', '3'):
				print('1 또는 2를 입력하세요. (종료 : 3)')
				continue
			user_input = int(raw_input)
			# 메뉴얼 모드
			if user_input == 1:
				self.manual_mode()
			# json 모드
			elif user_input == 2:
				self.json_mode()
			# 종료
			elif user_input == 3:
				break

	#===========================================
	#	NpuSimulator 메뉴얼 모드 메서드
	#===========================================
	def	manual_mode(self):
		# 필터 입력
		print('--------------------')
		print('[1] 필터 입력')
		print('--------------------')
		print('필터 A (3줄 입력, 공백 구분)')
		filter_a = self.input_matrix()
		print('✓ 필터 A 저장 완료') 
		print('필터 B (3줄 입력, 공백 구분)') 
		filter_b = self.input_matrix()
		print('✓ 필터 B 저장 완료')
		# 패턴 입력
		print('--------------------')
		print('[2] 패턴 입력')
		print('--------------------')
		print('패턴 (3줄 입력, 공백 구분)')
		pattern = self.input_matrix()
		# MAC 연산 (Multiply Accumulate)
		r1 = self.cal_mac(pattern, filter_a)
		r2 = self.cal_mac(pattern, filter_b)
		# 판정 처리
		jud_result = self.judge(r1, r2)
		# 시간 체크
		avg_result = self.profile_performance(pattern, filter_a)
		# 결과 판정
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
		total = 0
		passed = 0
		failed = 0
		fail_list = []

		# 데이터 로드
		data = self.load_json()
		# 데이터 로드 실패 시, json 모드 종료
		if data is None:
			return

		# 추출 데이터 값 가져오기
		extracted_filters = data['filters']
		extracted_patterns = data['patterns']
		print('--------------------')
		print('[1] 필터 로드')
		print('--------------------')
		for key in extracted_filters:
			filter_types = list(extracted_filters[key].keys())  # ["cross", "x"]
			print(f'✓ {key} 필터 로드 완료 ({filter_types})')

		print('--------------------')
		print('[2] 패턴 분석 (라벨 정규화 적용)')
		print('--------------------')
		for key in extracted_patterns:
			try:
				# 키 값에서 패턴의 크기 추출
				raw_size_data = str(key)
				tmp_list = raw_size_data.split('_')
				parttern_size = int(tmp_list[1])
				# 패턴 키 저장 ('size_n')
				load_key = f'size_{parttern_size}'
				# 필터에서 패턴값의 크기에 맞는 데이터 가져오기 
				filter_cross = extracted_filters[load_key]['cross']
				filter_x = extracted_filters[load_key]['x']
				# 패턴에서 비교할 데이터 가져오기
				pattern = extracted_patterns[key]['input']
				# 크기 검증
				if len(pattern) != len(filter_cross) or len(pattern) != len(filter_x):
					print(f'{key}: FAIL (크기 불일치)')
					total += 1
					failed += 1
					fail_list.append((key, '크기 불일치'))
					continue
				# MAC 연산
				score_cross = self.cal_mac(pattern, filter_cross)
				score_x = self.cal_mac(pattern, filter_x)
				# 판정 처리
				jud_result = self.judge(score_cross, score_x, 'Cross', 'X')

				# expected 정규화
				expected_raw = extracted_patterns[key]['expected']  # "+" 또는 "x"
				if expected_raw == '+' or expected_raw == 'cross':
					expected = 'Cross'
				else:
					expected = 'X'

				total += 1
				# PASS/FAIL 비교
				if jud_result == expected:
					pass_fail = 'PASS'
					passed += 1
				else:
					pass_fail = 'FAIL'
					failed += 1
					if jud_result == 'UNDECIDED':
						fail_list.append((key, '동점(UNDECIDED) 처리 규칙에 따라 FAIL'))
					else:
						fail_list.append((key, f'판정 {jud_result} != expected {expected}'))

				# 결과 출력
				print(f'--- {key} ---')
				print(f'Cross 점수: {score_cross}')
				print(f'X 점수: {score_x}')
				print(f'판정: {jud_result} | expected: {expected} | {pass_fail}')
			except Exception as s:
				continue

		print('--------------------')
		print('[3] 성능 분석 (평균/10회)')
		print('--------------------')
		print('크기       평균 시간(ms)    연산 횟수')
		print('-' * 40)
		sizes = [3, 5, 13, 25]
		for n in sizes:
			if n == 3:
				test_data = []
				for _ in range(3):
					row = [1, 1, 1]
					test_data.append(row)
			else:
				size_key = 'size_' + str(n)
				test_data = extracted_filters[size_key]['cross']
			avg_ms = self.profile_performance(test_data, test_data)
			ops = n * n
			print(str(n) + '×' + str(n) + '    ' + str(round(avg_ms, 3)) + 'ms    ' + str(ops))

		print('--------------------')
		print('[4] 결과 요약')
		print('--------------------')
		print(f'총 테스트: {total}개')
		print(f'통과: {passed}개')
		print(f'실패: {failed}개')
		if fail_list:
			print(f'\n실패 케이스:')
			for name, reason in fail_list:
				print(f'- {name}: {reason}')

#===========================================
#	NpuSimulator 실행 코드
#===========================================
simulator = NpuSimulator()
simulator.run()