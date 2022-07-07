QUIZ BOT

FUNCTIONS

Savollar:
  1. Oddiy
  2. Multiple choice

1. Imtixon. (Vaqtli va Balli yoki Odatiy)
2. Battle
3. Leaderboard
4. Fanlar




User:
  first_name 
  last_name
  username
  telegram_id

Question:
  title
  content
  type = MULTIPLE SINGLE
  time

QuestionOptions
  title
  is_correct
  question (F)

Subject:
  title


Exam:
  title
  content
  subjects (M)
  questions (M editable False)
  questions_count
  start_datetime
  end_datetime
  duration

UserExam:
  exam (F)
  user  (F)
  score 
  start_datetime
  end_datetime

UserExamAnswer:
  option_ids
  user_exam (F)
  question (F)
  is_correct










