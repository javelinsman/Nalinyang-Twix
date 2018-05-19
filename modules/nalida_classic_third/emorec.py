"Module for Emotion Recording"
import json

EMOTION_PLEASED = '[기쁨, 설렘, 상쾌함]'
EMOTION_PASSIONATE = '[신남, 즐거움, 열정적]'
EMOTION_SAD = '[슬픔, 후회, 우울]'
EMOTION_IRRITATED = '[짜증, 화남, 불쾌]'
EMOTION_COMPLEX = '[복합 감정]'
EMOTION_ETC = '[기타 감정]'
EMOTION_ORDINARY = '[평범하다]'
EMOTIONS = [EMOTION_PLEASED, EMOTION_PASSIONATE,
            EMOTION_SAD, EMOTION_IRRITATED, EMOTION_COMPLEX,
            EMOTION_ETC, EMOTION_ORDINARY]
REPLYS = [
    [
        '헤헤, 잘됐네요. 남은 하루도 기분 좋게 보내실 수 있길 바라요!',
        '앗 혹시 제가 말 걸어서 설레셨나요?! 헤헤 농담이에요! 기쁜 일이 있으시다니 날리냥도 기분이 들뜨네요!'
    ],
    [
        '냥! 저도 즐거운데요?',
        '날리냥도 오늘은 에너지가 넘치네요! 꾹꾹이를 하지 않고는 못 배기겠어요!',
        '활기찬 모습이 정말 멋지네요. 남은 하루도 같이 신나게 보내봐요 냥!'
    ],
    [
        '그렇군요 ㅠㅠ 슬퍼해도 괜찮아요! 날리냥이 꼭 안아드릴게요!',
        '날리냥도 너무 속상해지네요. 우울한 일은 늘 예기치 못하게 찾아와서 더 슬픈 것 같아요 ㅠㅠ',
        '슬픈 일이 있으셨나 보군요. 소중한 마음이 너무 많이 다치지는 않길 바라요. 날리냥이 응원할게요!'
    ],
    [
        '날리냥도 화가 나네요! 소중한 나를 위해 맛있는 거라도 먹어야겠어요!',
        '냥냥! 누가 그렇게 기분 나쁘게 만들었어요? 날리냥이 냥냥펀치를 날려줄 테다!',
    ],
    [
        '한 마디로 정의내리기 어려운 기분이 들 때가 종종 있죠! 어떤 감정일지 궁금하네요 헤헤',
        '기쁜데 불안할 때도 있고, 화나는데 웃길 때도 있고. 감정은 참 복잡한 것 같아요!',
    ],
    [
        '선택지가 너무 제한적이었나 보군요! 어떤 감정일지 궁금하네요 ;)',
    ],
    [
        '그럴 때가 많지요. 하루하루가 특별한 것도 좋지만, 때로는 반복되는 안정적 일상도 나쁘지 않은 것 같아요!',
        '헤헤, 사실 지금은 날리냥도 별로 특별한 기분이 안 들어요. 모든 순간이 격렬할 필요는 없잖아요?',
    ],
]


KEYBOARD_EMOTIONS = [
    [EMOTION_PLEASED],
    [EMOTION_PASSIONATE],
    [EMOTION_SAD],
    [EMOTION_IRRITATED],
    [EMOTION_COMPLEX, EMOTION_ETC, EMOTION_ORDINARY]
    ]

KEYBOARD = json.dumps({
    "keyboard" : KEYBOARD_EMOTIONS,
    "one_time_keyboard" : True,
    })

def is_emorec_response(message):
    "determines if message is emorec response"
    return message["data"]["text"] in EMOTIONS
