"""
String Resourses for NalidaClassicSecond module
"""

# 메시지를 여러 개로 끊고 싶을 때는 이 함수를 사용하세요.
# 아래의 예시 참조.
def multi(*args):
    "use this function when you want to send multple messages"
    delimiter = '$$$'
    return delimiter.join(args)

# 처음에 등록하는 과정
REGISTER_COMPLETE = multi(
    '안녕하세요!',
    '헤헤, 반가워요. 저는 날리다의 마스코트이자 날리다 클래식 워크샵의 진행을 도울 날리냥이라고 해요.',
    '앞으로 한 달 동안 날리다와 함께 소중한 시간 보내시길 바라요.',
    )

ASK_NICKNAME = '우선 진행을 하기에 앞서 참가자님을 어떻게 부르면 좋을지 알고 싶어요. 오늘 워크샵에서 정하신 별칭이 뭐예요?'
CONFIRM_NICKNAME = '아래의 별칭이 맞나요? "네", "아니오"로 대답해주세요.\n[%s]'
RESPONSE_NICKNAME_YES = '네'
RESPONSE_NICKNAME_NO = '아니오'
WRONG_RESPONSE_FORMAT = '잘못된 형식의 답변입니다.'
NICKNAME_SUBMITTED = '이제부터 %s님이라고 부를게요!'
ASK_NICKNAME_AGAIN = '그럼 뭐예요?'
ASK_EXPLANATION_FOR_NICKNAME = '이런 별칭을 짓게 되신 계기는 무엇인가요? 2~3문장으로 답변해주세요.'
EXPLANATION_SUBMITTED = '좋은 설명 잘 들었어요!'
INSTRUCTIONS_FOR_EMOREC = '그리고 오늘부터 하루에 3번씩 랜덤한 시각에 지금 어떤 감정을 느끼고 있는지를 물어볼 거예요. 나의 감정을 파악하는 데 도움이 되는 활동이니까 성실하게 답변해주시기를 바라요. 지금 바로 한번 연습해 볼까요?.'

# 감정기록
ASK_EMOTION = '지금은 무슨 감정을 느끼고 있나요?\n메시지를 늦게 보았어도 현재의 상태를 기록해주세요.'
EMOREC_SHARING_MESSAGE = '지금 어떤 동료는 이런 감정을 느끼고 있대요: %s'
ASK_EMOTION_DETAIL = '오늘 하루는 무슨 일이 있었고, 어떤 감정을 느꼈나요? 자세히 설명해주세요.'
EMOREC_SHARING_DETAILED_MESSAGE = '감정 일기: %s'
EMOREC_RESPONSE_RECORDED_AND_SHARED = '응답이 기록되고 공유되었어요. 감사합니다!'
EMOREC_RESPONSE_RECORDED_BUT_NOT_SHARED = '응답이 기록되고 공유는 되지 않았어요. 감사합니다!'
COMMAND_NOT_TO_SHARE_EMOTION = '비공개' #노터치

# 기타
CAT_MEOWS = ['냥', '야옹', '냐옹', '야아옹', '냐아옹']

# Admin 방
REGISTERED_AS_BROADCASTING_ROOM = '이 곳이 %s님의 중계방으로 등록되었습니다. 감사합니다.'
# 이 밑으론 아마 건드릴 거 없을 듯.
ERROR_MAKE_SESSION_INVALID_CONTEXT = '잘못된 아이디가 포함되어 있습니다. 다시 확인해주세요.'
ERROR_MAKE_SESSION_NO_TARGET_CHAT = '%s님의 중계방이 등록되지 않았습니다. 다시 확인해주세요.'
ERROR_NOTICE_INVALID_CONTEXT = '잘못된 닉네임이 포함되어 있습니다. 다시 확인해주세요.'
COMMAND_PUBLISH_REGISTRATION_KEY = '등록키발급'
COMMAND_MAKE_SESSION = '세션등록'
COMMAND_NOTICE = '공지'
REPORT_NOTICE_COMPLETE = '공지를 완료했습니다!'
COMMAND_PREFIX_REGISTER_BROADCASTING_ROOM = 'REGBCROOM:' #절대노터치
COMMAND_FAKE_TIMER = '타이머'

# 모니터링
REPORT_NICKNAME = '사용자 %s가 닉네임을 등록했습니다: %s'
HELP_MESSAGE_BROADCASTING_ROOM_REGKEY = multi(
    '%s님의 중계방을 등록하려면 아래의 메세지를 직접 보내게 하세요',
    'REGBCROOM:%s'
    )
REPORT_EXPLANATION = '%s님의 별명 설명: %s'
REPORT_EMOREC_SHARING = '%s님의 감정: %s'
REPORT_EMOREC_DETAIL = '%s님의 감정설명: %s'

COMMAND_GET_EMOREC_TIME = '감정기록시간'
COMMAND_NEXT_EMOREC_TIME = '감정기록시간재설정'
