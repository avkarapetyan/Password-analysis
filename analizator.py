import pandas as pd
import string
import random
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression 
from tkinter import *  
from tkinter import messagebox
import sklearn.utils._typedefs
import sklearn.utils._heap
import sklearn.utils._sorting
import sklearn.utils._vector_sentinel

characters = list(string.ascii_letters + string.digits)

def generate_random_password(name):
    length1 = random.randrange(1,4)
    length2 = random.randrange(1,6)
    if len(name)==0:
         length1 = random.randrange(3,9)
         length2 = random.randrange(3,9)
    random.shuffle(characters)
    password = []
    
    for i in range(length1):
        password.append(random.choice(characters))
    for i in range(len(name)):
        password.append(name[i])
    for i in range(length2):
        password.append(random.choice(characters))

    return "".join(password)

def createTokens(f): #Cоздаем токенизатор
    tokens = []
    for i in f:
        tokens.append(i)
    return tokens

def gp(date):
    length1 = random.randrange(0,12)
    length2 = random.randrange(0,12)
    random.shuffle(characters)
    password = []
    
    for i in range(length1):
        password.append(random.choice(characters))
    for i in range(len(date)):
        password.append(date[i])
    for i in range(length2):
        password.append(random.choice(characters))

    return "".join(password)

df_names = pd.read_csv('passwords_names')
X_n = df_names['password']
y_n = df_names['target']
X_train_n, X_test_n, y_train_n, y_test_n = train_test_split(
      X_n, y_n, test_size=0.0000000001, random_state=42)
vectorizer_n = TfidfVectorizer(tokenizer=createTokens)
X_train_n_v = vectorizer_n.fit_transform(X_train_n)
X_test_n_v = vectorizer_n.transform(X_test_n)
clf_n = LogisticRegression(max_iter=1000).fit(X_train_n_v, y_train_n)

df_s = pd.read_csv('passwords_surnames.csv')
X_s = df_s['password']
y_s = df_s['target']
X_train_s, X_test_s, y_train_s, y_test_s = train_test_split(
      X_s, y_s, test_size=0.00001, random_state=42)
vectorizer_s = TfidfVectorizer(tokenizer=createTokens)
X_train_s_v = vectorizer_s.fit_transform(X_train_s)
X_test_s_v = vectorizer_s.transform(X_test_s)
clf_s = LogisticRegression(max_iter=1000).fit(X_train_s_v, y_train_s)

df_d = pd.read_csv('passwords_dates')
df_d = df_d.fillna('')
X_d = df_d['password']
y_d = df_d['target']
X_train_d, X_test_d, y_train_d, y_test_d = train_test_split(
      X_d, y_d, test_size=0.0000001, random_state=42)
vectorizer_d = TfidfVectorizer(tokenizer=createTokens)
X_train_d_v = vectorizer_d.fit_transform(X_train_d)
X_test_d_v = vectorizer_d.transform(X_test_d)
clf_d = LogisticRegression(max_iter=1000).fit(X_train_d_v, y_train_d)

df_k = pd.read_csv('passwords_pets')
X_k = df_k['password']
y_k = df_k['target']
X_train_k, X_test_k, y_train_k, y_test_k = train_test_split(
     X_k, y_k, test_size=0.0000001, random_state=42)
vectorizer_k = TfidfVectorizer(tokenizer=createTokens)
X_train_k_v = vectorizer_k.fit_transform(X_train_k)
X_test_k_v = vectorizer_k.transform(X_test_k)
clf_k = LogisticRegression(max_iter=1000).fit(X_train_k_v, y_train_k)


def clicked():  
    res = entry.get()
    if len(set(res).intersection(set(characters)))!=len(set(res)):
        messagebox.showinfo('Ошибка!', 'Пароль должен содержать только буквы латинского алфавита и цифры!')
        clear_text()
        return 0
    new = [res]
    new_n_v = vectorizer_n.transform(new)
    new_s_v = vectorizer_s.transform(new)
    new_d_v = vectorizer_d.transform(new)
    new_k_v = vectorizer_k.transform(new)
    predictions_n = clf_n.predict_proba(new_n_v)[0][1]
    predictions_s = clf_s.predict_proba(new_s_v)[0][1]
    predictions_d = clf_d.predict_proba(new_d_v)[0][1]
    predictions_k = clf_k.predict_proba(new_k_v)[0][1]
    analiz[0].pack()
    for i in range(1, 7):
        analiz[i].pack(anchor='w')
    analiz[0].config(text="Анализ завершен, вот отчет",font=("Arial Bold", 10),)
    analiz[1].config(text="Ваш пароль: "+res,font=("Arial Bold", 10))
    analiz[2].config(text="Длина пароля: "+ str(len(res)),font=("Arial Bold", 10))
    analiz[3].config(text="Вероятность наличия имени в пароле: "+ str(round(predictions_n,6)),font=("Arial Bold", 10))
    analiz[4].config(text="Вероятность наличия фамилии в пароле: "+ str(round(predictions_s,6)),font=("Arial Bold", 10))
    analiz[5].config(text="Вероятность наличия даты в пароле: "+ str(round(predictions_d,6)),font=("Arial Bold", 10))
    analiz[6].config(text="Вероятность наличия клички животного в пароле: "+ str(round(predictions_k,6)),font=("Arial Bold", 10))

def clear_text():
    entry.delete(0, END)
    for i in range(7):
        analiz[i].config(text="")

window = Tk()  
window.title("Анализатор паролей")  
window.geometry('600x500')  
lbl = Label(window, text="Введите пароль: ")  
lbl.pack()
entry = Entry(window,width=25)  
entry.pack()
analiz = [Label(window, text="") for i in range(7)]
btn = Button(window, text="Анализ!", command=clicked)
btn.pack()
btn_clear = Button(window,text="Очистка!", command=clear_text)
btn_clear.pack()
window.mainloop()