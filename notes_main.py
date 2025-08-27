import json
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QTextEdit, QListWidget, QLineEdit, QInputDialog, QMessageBox

with open("notes.json", "r", encoding="utf-8") as file:
    note = json.load(file)

def show_note():
    name = list_word.selectedItems()[0].text()
    text_field.setText(note[name]["текст"])
    list_tag.clear()
    list_tag.addItems(note[name]["теги"])

def add_note():
    note_name, ok = QInputDialog.getText(main_window, "Добавить заметку","Название заметки:")

    if ok and note_name !="":
        note[note_name] = {"текст" : "", "теги" : []}
        list_word.addItem(note_name)
    
    elif note_name == "" and ok:
        error_window = QMessageBox()
        error_window.setText('Вы не ввели название заметки!')
        error_window.exec_()


def del_note():
    if list_word.selectedItems():
        name = list_word.selectedItems()[0].text()
        del note[name]
        list_word.clear()
        list_word.addItems(note)

    elif list_word.selectedItems() == []:
        error_window = QMessageBox()
        error_window.setText('Вы не выбрали заметку!')
        error_window.exec_()


def save_note():
    if list_word.selectedItems():
        text = text_field.toPlainText()
        name = list_word.selectedItems()[0].text()
        note[name]["текст"] = text

    elif list_word.selectedItems() == []:
        error_window = QMessageBox()
        error_window.setText('Вы не выбрали заметку!')
        error_window.exec_()


def add_tag():
    if list_word.selectedItems():
        key = list_word.selectedItems()[0].text()
        tag = tag_field.text()
        if not tag in note[key]["теги"] and tag != '':
            note[key]["теги"].append(tag)
            list_tag.addItem(tag)
            tag_field.clear()
        elif tag == '':
            error_window = QMessageBox()
            error_window.setText('Вы не ввели тег')
            error_window.exec_()

    elif list_word.selectedItems() == []:
        error_window = QMessageBox()
        error_window.setText('Вы не выбрали заметку!')
        error_window.exec_()



def del_tag():
    if list_tag.selectedItems():
       key = list_word.selectedItems()[0].text()
       tag = list_tag.selectedItems()[0].text()
       note[key]["теги"].remove(tag)
       list_tag.clear()
       list_tag.addItems(note[key]["теги"])

    elif list_word.selectedItems() == []:
        error_window = QMessageBox()
        error_window.setText('Вы не выбрали заметку!')
        error_window.exec_()
   
    elif list_tag.selectedItems() == []:
        error_window = QMessageBox()
        error_window.setText('Вы не выбрали тег')
        error_window.exec_()



def search_tag():
    tag = tag_field.text()
    if big_button2.text() == 'Искать заметки по тегу' and tag != '':
        notes_filtered = {}
        for i in note:
            if tag in note[i]["теги"]:
                notes_filtered[i]=note[i]
        
        big_button2.setText('Сбросить поиск')
        list_word.clear()
        list_tag.clear()
        list_word.addItems(notes_filtered)
    elif big_button2.text() == 'Сбросить поиск':
        tag_field.clear()
        list_tag.clear()
        list_word.clear()
        list_word.addItems(note)
        big_button2.setText('Искать заметки по тегу')
    
    elif list_tag.selectedItems() == []:
        error_window = QMessageBox()
        error_window.setText('Вы не ввели тег')
        error_window.exec_()



app = QApplication([])
main_window = QWidget()
main_window.setWindowTitle('Умные заметки')
main_window.resize(800, 600)
text_field = QTextEdit()
small_button1 = QPushButton('Создать заметку')
small_button2 = QPushButton('Удалить заметку')
small_button3 = QPushButton('Добавить к заметке')
small_button4 = QPushButton('Открепить от заметки')
big_button1 = QPushButton('Сохранить заметку')
big_button2 = QPushButton('Искать заметки по тегу')
label_list = QLabel('Список заметок')
label_tag = QLabel('Список тегов')
list_word = QListWidget()
list_tag = QListWidget()
tag_field = QLineEdit()
tag_field.setPlaceholderText('Введите тег...')

mini_button_layout1 = QHBoxLayout()
mini_button_layout2 = QHBoxLayout()
right_layout = QVBoxLayout()
main_layout = QHBoxLayout()

mini_button_layout1.addWidget(small_button1)
mini_button_layout1.addWidget(small_button2)
mini_button_layout2.addWidget(small_button3)
mini_button_layout2.addWidget(small_button4)
right_layout.addWidget(label_list)
right_layout.addWidget(list_word)
right_layout.addLayout(mini_button_layout1)
right_layout.addWidget(big_button1)
right_layout.addWidget(label_tag)
right_layout.addWidget(list_tag)
right_layout.addWidget(tag_field)
right_layout.addLayout(mini_button_layout2)
right_layout.addWidget(big_button2)
main_layout.addWidget(text_field, 60)
main_layout.addLayout(right_layout, 40)
main_window.setLayout(main_layout)

list_word.addItems(note)
list_word.itemClicked.connect(show_note)
small_button1.clicked.connect(add_note)
small_button2.clicked.connect(del_note)
big_button1.clicked.connect(save_note)
small_button3.clicked.connect(add_tag)
small_button4.clicked.connect(del_tag)
big_button2.clicked.connect(search_tag)

main_window.show()
app.exec_()

with open("notes.json", "w", encoding="utf-8") as file:
    json.dump(note,file)

