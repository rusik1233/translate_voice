try:
    import sounddevice as sd
    import numpy as np
    import scipy.io.wavfile as wav
    import speech_recognition as sr
    from googletrans import Translator
    import os
    from generate_word import generate_word, timer
    print('success')
except Exception as e:
    print(e,'не устоновлены библиотеки')


current_round = 1
bal = 0
rounds = 0
recorded_audio = None
sample_rate = 44100
recognized_text = ""

def choice():
    global time, rounds, dificult
    print("""
    ╔═══════════════════════════════╗
    ║          ИГРА СЛОВ            ║
    ╚═══════════════════════════════╝
    """)
    print('-'*90)
    rounds = int(input('напиши число желаемых раундов: ')) 
    print('-'*90)
    dificult = input('выберите сложность: лёгкая , средняя, сложная: ')
    print('-'*90)
    if dificult == 'лёгкая':
        time = 5
    elif dificult == 'средняя':
        time = 3
    elif dificult == 'сложная':
        time = 1

def start():
    global lang, word, word_tr, current_round
    print('-'*90)
    lang = input("Введите код языка для перевода (например, 'en' — английский, 'es' — испанский): ")
    word = generate_word()
    print('-'*90)
    print(f'Ваше слово:')
    print(word)
    print(f'перевести надо на {lang}')
    word_tr = translate(lang,word)
    print(f'у вас есть {time} секунд на подумать')
    print('-'*90)
    timer(time)
    recording() 
    save_file(lang)
    check_word()
    delete_file()
def translate(lang,word):
    translator = Translator()
    translated_text = translator.translate(word, dest=lang)
    return translated_text.text
def recording():
    global recorded_audio
    print("Говори... 🎙️")
    recorded_audio = sd.rec(
        int(int(time) * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype="int16"
    )
    sd.wait()
def save_file(lang):
    global recorded_audio, recognized_text
    if recorded_audio is not None:
        wav.write("output.wav", sample_rate, recorded_audio)
        print("Запись завершена, теперь распознаём... 🤖")

        recognizer = sr.Recognizer()
        with sr.AudioFile("output.wav") as source:
            audio = recognizer.record(source)

        try:
            recognized_text = recognizer.recognize_google(audio, language=lang)
            print("Ты сказал: 😃", recognized_text)
        except sr.UnknownValueError:
            print("Не удалось распознать речь. 🙁")
        except sr.RequestError as e:
            print("Ошибка сервиса: 😞", e)
    else:
        print("Нет записанных данных для сохранения.")
def check_word():
    global current_round, bal
    if recognized_text.lower() == word_tr.lower():
        print('молодец ты прав ✌')
        print(f"Текущий раунд: {current_round}")
        current_round += 1
        print('Баллы + 1')
        bal += 1
    else: 
        print(f'Ты ошибся слово: {word_tr} 😞')
        current_round += 1
def delete_file():
    file_path = "output.wav"
    try:
        os.remove(file_path)
    except FileNotFoundError:
        print(f"Ошибка: Файл '{file_path}' не найден.😞")
    except Exception as e:
        print(f"Произошла ошибка при удалении файла: 😞{e}😞")
def main():
    global current_round, rounds, bal
    choice()
    while current_round <= rounds:
        print(f"\n=== Раунд {current_round} из {rounds} ===")
        start()
    print(f"\nИгра завершена! Ваш счет: {bal} из {rounds}")
    if bal > rounds * 0.5:  
        print('поздравляем, вы выиграли! 🎉')
    else:
        print('ты проиграл. Попробуй еще раз! 💪')
if __name__ == "__main__":
    main()