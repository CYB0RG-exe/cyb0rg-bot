from tkinter import *
from tkinter import ttk, messagebox
import tkinter as tk
import webbrowser
import pydirectinput
import pyautogui
import threading
import os
import win32gui
import sys
import hashlib
import uuid
import keyboard
import cv2
from vision import Vision
from ekranyakala import ekranYakala
from time import time, sleep
from keyauth import api
import json
from base64 import b64decode
from io import BytesIO
from PIL import Image, ImageTk

class Window(Frame):
    def __init__(self, master=None, saniye=0):
        Frame.__init__(self, master)
        try:
            with open('config.json', 'r') as f:
                self.ayarlar = json.load(f)
        except:
            messagebox.showerror('config.json', 'config.json eksik veya bulunamadı.')
            os._exit(1)
        try:
            self.master = master
            self.saniye = saniye
            F1 = Frame(self.master)
            F1.place(x=375, y=200)
            self.start = Button(F1, text='Başla', command=self.thread, font='LemonMilk', cursor='hand2', fg='red', width=10, height=1)
            self.start.grid(row=0, pady=5)
            self.start.config(state=NORMAL, cursor='hand2', bg='red', fg='white')
            self.stop = Button(F1, text='Durdur | F11', command=self.durdur, font='LemonMilk', cursor='hand2', fg='green', width=10, height=1)
            self.stop.grid(row=1)
            self.stop.config(state=DISABLED, cursor='arrow', bg='white', disabledforeground='red')
            F2 = LabelFrame(self.master, text='Durum', font='bold', fg='red')
            F2.place(x=355, y=25)
            F3 = LabelFrame(self.master, text='Ayarlar', font='bold', fg='red')
            F3.place(x=20, y=25)
            self.metinSayisi = 0
            self.durum = Label(F2, text='Pasif', font='bold', fg='red')
            self.durum.grid()
            self.bulunanMetin = Label(F2, text='Bulunan Metin: 0', fg='blue')
            self.bulunanMetin.grid(row=1, sticky=W)
            self.zaman = Label(F2, text='Geçen Zaman: 00:00:00', fg='green')
            self.zaman.grid(row=2, sticky=W)
            self.ara = Button(F3, text='Ara', width=5, cursor='hand2', command=self.ara)
            self.ara.grid(row=0, column=1, sticky=W, pady=10)
            v1 = StringVar()
            self.windowName = ttk.Combobox(F3, width=20, textvariable=v1, state='readonly')
            self.windowName.grid(row=0, column=0, sticky=W)
            Label(F3, text='Metin Taşı Kesme Süresi').grid(row=2, sticky=W)
            self.kesmesuresi = IntVar()
            self.kesmesuresi.set(int(self.ayarlar['metin_kesme_suresi']))
            self.kesimsuresi = Spinbox(F3, from_=1, to=999, width=5, textvariable=self.kesmesuresi)
            self.kesimsuresi.grid(row=2, sticky=W, column=1)
            self.var1 = IntVar(value=0)
            self.kilitle = Checkbutton(F3, text='Widgetleri Kilitle', command=self.userKilit, variable=self.var1, onvalue=1, offvalue=0)
            self.kilitle.grid(row=3, column=1, pady=5, sticky=W)
            if int(self.ayarlar['gezinti_mod']):
                self.gezinti_var1 = IntVar(value=1)
            else:
                self.gezinti_var1 = IntVar(value=0)
            self.gezinti = Checkbutton(F3, text='Gezinme Modu', variable=self.gezinti_var1, onvalue=1, offvalue=0)
            self.gezinti.grid(row=4, column=0, pady=5, sticky=W)
            if int(self.ayarlar['skill_mod']):
                self.skill_yak_var = IntVar(value=1)
            else:
                self.skill_yak_var = IntVar(value=0)
            self.skill_yak = Checkbutton(F3, text='Skill Yak', variable=self.skill_yak_var, command=self.skillKilit, onvalue=1, offvalue=0)
            self.skill_yak.grid(row=5, column=0, sticky=W)
            self.skil_suresi = IntVar()
            self.skil_suresi.set(int(self.ayarlar['skill_acma_suresi']))
            Label(F3, text='Skill Açma Süresi').grid(row=6, sticky=W)
            self.skill_suresi = Spinbox(F3, from_=1, to=999, width=5, textvariable=self.skil_suresi)
            self.skill_suresi.grid(row=6, sticky=W, column=1)
            Label(F3, text='Skill 1').grid(row=7, column=0, sticky=W)
            self.skill1 = Entry(F3, width=5)
            self.skill1.insert(0, self.ayarlar['skill1'])
            self.skill1.grid(row=7, column=1, sticky=W)
            Label(F3, text='Skill 2').grid(row=8, column=0, sticky=W)
            self.skill2 = Entry(F3, width=5)
            self.skill2.insert(0, self.ayarlar['skill2'])
            self.skill2.grid(row=8, column=1, sticky=W)
            if int(self.ayarlar['esya_mod']):
                self.esya_topla_var = IntVar(value=1)
            else:
                self.esya_topla_var = IntVar(value=0)
            self.esya_topla = Checkbutton(F3, text='Eşya Topla', variable=self.esya_topla_var, command=self.esyaKilit, onvalue=1, offvalue=0)
            self.esya_topla.grid(row=9, column=0, sticky=W)
            self.esya_tusu = Entry(F3, width=5)
            self.esya_tusu.insert(0, self.ayarlar['esya_topla'])
            self.esya_tusu.grid(row=9, column=1, sticky=W)
            self.esyaKilit()

            self.iksir_var = IntVar(value=int(self.ayarlar['iksir_mod']))
            self.iksir_bas = Checkbutton(F3, text='İksir Bas', variable=self.iksir_var, command=self.iksirKilit, onvalue=1, offvalue=0)
            self.iksir_bas.grid(row=10, column=0, sticky=W)
            self.key_label1 = Label(F3, text='Tuş 1:')
            self.key_label1.grid(row=11, column=0, sticky=W)
            self.iksir_1 = Entry(F3, width=5)
            self.iksir_1.insert(0, self.ayarlar['iksir1'])
            self.iksir_1.grid(row=11, column=1, sticky=W)
            self.interval_label1 = Label(F3, text='Süre:')
            self.interval_label1.grid(row=11, column=2, sticky=W)
            self.iksir1_time = Entry(F3, width=5)
            self.iksir1_time.insert(0, self.ayarlar['iksir1_time'])
            self.iksir1_time.grid(row=11, column=3, sticky=W)
            self.key_label2 = Label(F3, text='Tuş 2:')
            self.key_label2.grid(row=12, column=0, sticky=W)
            self.iksir_2 = Entry(F3, width=5)
            self.iksir_2.insert(0, self.ayarlar['iksir2'])
            self.iksir_2.grid(row=12, column=1, sticky=W)
            self.interval_label2 = Label(F3, text='Süre:')
            self.interval_label2.grid(row=12, column=2, sticky=W)
            self.iksir2_time = Entry(F3, width=5)
            self.iksir2_time.insert(0, self.ayarlar['iksir2_time'])
            self.iksir2_time.grid(row=12, column=3, sticky=W)
            self.key_label3 = Label(F3, text='Tuş 3:')
            self.key_label3.grid(row=13, column=0, sticky=W)
            self.iksir_3 = Entry(F3, width=5)
            self.iksir_3.insert(0, self.ayarlar['iksir3'])
            self.iksir_3.grid(row=13, column=1, sticky=W)
            self.interval_label3 = Label(F3, text='Süre:')
            self.interval_label3.grid(row=13, column=2, sticky=W)
            self.iksir3_time = Entry(F3, width=5)
            self.iksir3_time.insert(0, self.ayarlar['iksir3_time'])
            self.iksir3_time.grid(row=13, column=3, sticky=W)
            self.key_label4 = Label(F3, text='Tuş 4:')
            self.key_label4.grid(row=14, column=0, sticky=W)
            self.iksir_4 = Entry(F3, width=5)
            self.iksir_4.insert(0, self.ayarlar['iksir4'])
            self.iksir_4.grid(row=14, column=1, sticky=W)
            self.interval_label4 = Label(F3, text='Süre:')
            self.interval_label4.grid(row=14, column=2, sticky=W)
            self.iksir4_time = Entry(F3, width=5)
            self.iksir4_time.insert(0, self.ayarlar['iksir4_time'])
            self.iksir4_time.grid(row=14, column=3, sticky=W)
            self.config_save_btn = Button(F3, text='Ayarları Kaydet', width=15, cursor='hand2', command=self.config_save)
            self.config_save_btn.grid(row=15, column=0, columnspan=4, pady=10)
            self.iksirKilit()
        except Exception as e:
            messagebox.showerror('Value Error', 'config.json Hatalı Değerler içeriyor.')
            os._exit(1)

    def config_save(self):
        try:
            self.ayarlar['gezinti_mod'] = self.gezinti_var1.get()
            self.ayarlar['esya_mod'] = self.esya_topla_var.get()
            self.ayarlar['skill_mod'] = self.skill_yak_var.get()
            self.ayarlar['metin_kesme_suresi'] = self.kesmesuresi.get()
            self.ayarlar['skill_acma_suresi'] = self.skil_suresi.get()
            self.ayarlar['skill1'] = self.skill1.get()
            self.ayarlar['skill2'] = self.skill2.get()
            self.ayarlar['esya_topla'] = self.esya_tusu.get()
            self.ayarlar['iksir_mod'] = self.iksir_var.get()
            self.ayarlar['iksir1'] = self.iksir_1.get()
            self.ayarlar['iksir2'] = self.iksir_2.get()
            self.ayarlar['iksir3'] = self.iksir_3.get()
            self.ayarlar['iksir4'] = self.iksir_4.get()
            self.ayarlar['iksir1_time'] = self.iksir1_time.get()
            self.ayarlar['iksir2_time'] = self.iksir2_time.get()
            self.ayarlar['iksir3_time'] = self.iksir3_time.get()
            self.ayarlar['iksir4_time'] = self.iksir4_time.get()
            if self.ayarlar['at_inme_suresi']:
                self.ayarlar['at_inme_suresi'] = self.ayarlar['at_inme_suresi']
            else:  # inserted
                self.ayarlar['at_inme_suresi'] = 1
            with open('config.json', 'w') as f:
                json.dump(self.ayarlar, f, indent=4)
            messagebox.showinfo('Başarılı', 'Ayarlar başarıyla kaydedildi.')
        except Exception as e:
            messagebox.showerror('Save Error', f'Dosya varlığını ve değerleri kontrol edin.\n{e}')

    def esyaKilit(self):
        if self.esya_topla_var.get() == 1:
            self.esya_tusu.config(state='normal')
        else:  # inserted
            self.esya_tusu.config(state='disabled')

    def skillKilit(self):
        if self.skill_yak_var.get() == 1:
            state = 'normal'
        else:  # inserted
            state = 'disabled'
        self.skill_suresi.config(state=state)
        self.skill1.config(state=state)
        self.skill2.config(state=state)

    def iksirKilit(self):
        if self.iksir_var.get() == 1:
            state = 'normal'
        else:  # inserted
            state = 'disabled'
        self.iksir_1.config(state=state)
        self.iksir_2.config(state=state)
        self.iksir_3.config(state=state)
        self.iksir_4.config(state=state)
        self.iksir1_time.config(state=state)
        self.iksir2_time.config(state=state)
        self.iksir3_time.config(state=state)
        self.iksir4_time.config(state=state)

    def ara(self):
        liste = []

        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                if win32gui.GetWindowText(hwnd) == '':
                    return
                liste.append(win32gui.GetWindowText(hwnd))
                self.windowName.config(values=liste)
        win32gui.EnumWindows(winEnumHandler, None)

    def userKilit(self, func=None):
        if self.var1.get() == 1 or func:
            self.kesimsuresi.config(state='disabled')
            self.windowName.config(state='disabled')
            self.ara.config(state='disabled')
            self.gezinti.config(state='disabled')
            self.esya_topla_var.set(0)  # esya_topla_var'ı 0 yaparak esya_topla widget'inin durumunu değiştiriyoruz
            self.esya_tusu.config(state='disabled')
            self.skill_yak.config(state='disabled')
            self.skill_suresi.config(state='disabled')
            self.skill1.config(state='disabled')
            self.skill2.config(state='disabled')
            self.config_save_btn.config(state='disabled', cursor='arrow')
            self.start.config(state=DISABLED, cursor='arrow', bg='white', disabledforeground='red')
            self.ara.config(state=DISABLED, cursor='arrow')
            self.iksir_bas.config(state='disabled')
            self.iksir_1.config(state='disabled')
            self.iksir_2.config(state='disabled')
            self.iksir_3.config(state='disabled')
            self.iksir_4.config(state='disabled')
            self.iksir1_time.config(state='disabled')
            self.iksir2_time.config(state='disabled')
            self.iksir3_time.config(state='disabled')
            self.iksir4_time.config(state='disabled')
            if func:
                self.kilitle.config(state='disabled')
        else:
            self.kesimsuresi.config(state='normal')
            self.windowName.config(state='normal')
            self.windowName.config(state='readonly')
            self.ara.config(state='normal', cursor='hand2')
            self.gezinti.config(state='normal')
            self.esya_topla.config(state='normal')  # burada esya_topla widget'inin durumunu 'normal' yapıyoruz
            self.esya_tusu.config(state='normal')
            self.skill_yak.config(state='normal')
            self.skill_suresi.config(state='normal')
            self.skill1.config(state='normal')
            self.skill2.config(state='normal')
            self.config_save_btn.config(state='normal', cursor='hand2')
            self.start.config(state=NORMAL, cursor='hand2', bg='red', fg='white')
            self.sureBaslat = False
            self.durum['text'] = 'Pasif'
            self.iksir_bas.config(state='normal')
            self.iksir_1.config(state='normal')
            self.iksir_2.config(state='normal')
            self.iksir_3.config(state='normal')
            self.iksir_4.config(state='normal')
            self.iksir1_time.config(state='normal')
            self.iksir2_time.config(state='normal')
            self.iksir3_time.config(state='normal')
            self.iksir4_time.config(state='normal')
            self.kilitle.config(state='normal')


    def zamanlayici(self):
        if self.sureBaslat == True:
            self.saniye += 1
            seconds = self.saniye % 86400
            hour = seconds // 3600
            seconds %= 3600
            minutes = seconds // 60
            seconds %= 60
            self.master.after(1000, self.zamanlayici)
            return self.zaman.configure(text='Geçen Zaman: %02d:%02d:%02d' % (hour, minutes, seconds))

    def thread(self):
        threading.Thread(target=self.basla).start()

    def basla(self):
        try:
            if self.windowName.get() == '':
                messagebox.showwarning('Hata', 'Başlamadan Önce Oyun Ekranını Seç')
                print("[Uyarı] Oyun ekranı seçilmedi.")
                return
            print("[INFO] Ekran yakalama başlatılıyor...")
            wincap = ekranYakala(self.windowName.get())
            print("[INFO] Model yükleniyor...")
            self.cascade = cv2.CascadeClassifier('cascade\\cascade.xml')
            self.vision = Vision(None)
            self.loop_time = time()
            self.metine_vur = False
            self.stop_flag = False
            self.s = 1
            self.kontrol = 0
            self.saniye = 0
            self.start.config(state=DISABLED, cursor='arrow', bg='white', disabledforeground='red')
            self.userKilit(func=True)
            anons = Label(self.master, fg='red', font=('Comic Sans MS', 13, 'bold'))
            anons.place(x=75, y=150)
            don = 4
            for _ in range(1, 4):
                don -= 1
                sleep(1)
                print(f"Başlıyor: {don}")
                anons['text'] = ('Başlıyor', don)
            anons.after(1000, anons.destroy)
            print("[INFO] Bot başlatılıyor...")
            self.sureBaslat = True
            self.zamanlayici()
            self.durum['text'] = 'Aktif'
            self.bulunanMetin['text'] = 'Bulunan Metin: 0'
            print("[INFO] Saldırı thread'i başlatılıyor...")
            threading.Thread(target=self.saldir, args=(wincap,)).start()
        except Exception as e:
            print(f"[HATA] basla fonksiyonunda hata: {e}")
            messagebox.showerror('Hata: Ekran Bulunamadı', f'Seçilen isimde ekran bulunamadı.\n{e}')

    def durdur(self):
        self.sureBaslat = False
        self.durum['text'] = 'Pasif'
        self.start.config(state=NORMAL, cursor='hand2', bg='red', fg='white')
        self.kilitle.config(state='normal')
        self.userKilit()

    def stop_script(self):
        self.stop_flag = True
        self.durdur()

    def saldir(self, wincap):
        print('[DEBUG] saldir fonksiyonu başladı')
        try:
            self.metine_vur = False
            self.kontrol = 0
            self.iksir_kontrol = False
            while True:
                print('[DEBUG] saldir döngüsü çalışıyor')
                if self.stop_flag:
                    print('[DEBUG] stop_flag aktif, çıkılıyor')
                    return
                # Lisans kontrolü kısmı
                # print('[DEBUG] Lisans kontrolü atlandı')
                if not self.skill_yak_var.get() or not int(time()) % float(self.skill_suresi.get()) == 0 or self.skill1.get():
                    self.iksir_kontrol = True
                    sleep(1)
                    print('[DEBUG] at_in_bin tuşlarına basılıyor')
                    pydirectinput.keyDown(self.ayarlar['at_in_bin'])
                    pydirectinput.press(self.ayarlar['at_in_bin2'])
                    pydirectinput.keyUp(self.ayarlar['at_in_bin'])
                    if self.stop_flag:
                        print('[DEBUG] stop_flag aktif, çıkılıyor')
                        return
                    sleep(1)
                    print('[DEBUG] skill1 tuşuna basılıyor:', self.skill1.get().lower())
                    pydirectinput.press(self.skill1.get().lower())
                    if self.stop_flag:
                        print('[DEBUG] stop_flag aktif, çıkılıyor')
                        return
                else:
                    sleep(1)
                    print('[DEBUG] at_in_bin tuşlarına basılıyor (else)')
                    pydirectinput.keyDown(self.ayarlar['at_in_bin'])
                    pydirectinput.press(self.ayarlar['at_in_bin2'])
                    pydirectinput.keyUp(self.ayarlar['at_in_bin'])
                    sleep(1)
                if self.skill2.get():
                    self.iksir_kontrol = True
                    sleep(1)
                    if self.stop_flag:
                        print('[DEBUG] stop_flag aktif, çıkılıyor')
                        return
                else:
                    pydirectinput.keyDown(self.ayarlar['at_in_bin'])
                    pydirectinput.press(self.ayarlar['at_in_bin2'])
                    pydirectinput.keyUp(self.ayarlar['at_in_bin'])
                    sleep(1)
                    if self.stop_flag:
                        print('[DEBUG] stop_flag aktif, çıkılıyor')
                        return
                    print('[DEBUG] skill2 tuşuna basılıyor:', self.skill2.get().lower())
                    pydirectinput.press(self.skill2.get().lower())
                    sleep(1)
                    pydirectinput.keyDown(self.ayarlar['at_in_bin'])
                    pydirectinput.press(self.ayarlar['at_in_bin2'])
                    pydirectinput.keyUp(self.ayarlar['at_in_bin'])
                if self.iksir_var.get() == 1:
                    print('[DEBUG] İksir kontrolü başlıyor')
                if self.iksir_var.get() == 1 and (self.iksir_kontrol or (self.iksir_1.get() and self.iksir1_time.get() and (int(time()) % float(self.iksir1_time.get()) == float(0)))):
                    print('[DEBUG] iksir_1 tuşuna basılıyor:', self.iksir_1.get())
                    pydirectinput.press(self.iksir_1.get())
                    if self.iksir_kontrol or (self.iksir_2.get() and self.iksir2_time.get() and (int(time()) % float(self.iksir2_time.get()) == float(0))):
                        print('[DEBUG] iksir_2 tuşuna basılıyor:', self.iksir_2.get())
                        pydirectinput.press(self.iksir_2.get())
                    if self.iksir_kontrol or (self.iksir_3.get() and self.iksir3_time.get() and (int(time()) % float(self.iksir3_time.get()) == float(0))):
                        print('[DEBUG] iksir_3 tuşuna basılıyor:', self.iksir_3.get())
                        pydirectinput.press(self.iksir_3.get())
                    if self.iksir_kontrol or (self.iksir_4.get() and self.iksir4_time.get() and (int(time()) % float(self.iksir4_time.get()) == float(0))):
                        print('[DEBUG] iksir_4 tuşuna basılıyor:', self.iksir_4.get())
                        pydirectinput.press(self.iksir_4.get())
                    self.iksir_kontrol = False
                ss = wincap.get_screenshot()
                print('[DEBUG] Ekran görüntüsü alındı:', type(ss), getattr(ss, 'shape', 'yok'))
                rectangles = self.cascade.detectMultiScale(ss)
                print('[DEBUG] Bulunan dikdörtgenler:', rectangles)
                if not self.metine_vur:
                    self.metine_vur = True
                    print('[DEBUG] metinevur thread başlatılıyor')
                    thrd = threading.Thread(target=self.metinevur, args=(rectangles, wincap))
                    thrd.start()
        except Exception as e:
            print('[HATA] Func: saldir - ', e)
            self.durdur()
            messagebox.showerror('Hata: saldir', f'Hata Oluştu.\n{e}')


    def metinevur(self, rectangles, wincap):
        if len(rectangles) > 0:
            targets = self.vision.get_click_points(rectangles)
            target = wincap.get_screen_position(targets[0])
            pyautogui.moveTo(x=target[0], y=target[1] + 5)
            if self.esya_topla_var.get():
                pydirectinput.press('z', presses=1)
            sleep(0.2)
            pyautogui.click(button='left')
            self.bulunanMetin['text'] = f'Bulunan Metin: {self.s}'
            sleep(float(self.kesimsuresi.get()))
            if self.stop_flag:
                return
            if self.esya_topla_var.get():
                pydirectinput.press('z', presses=5)
            self.s += 1
        else:  # inserted
            if not self.gezinti_var1.get() or self.stop_flag:
                return
            pydirectinput.press('e', presses=3)
            pydirectinput.press('f', presses=6)
            if self.stop_flag:
                return
            self.kontrol += 1
            if self.kontrol >= 3 and self.stop_flag:
                return
            pydirectinput.press('w', presses=6)
            self.kontrol = 0
        self.metine_vur = False

if __name__ == '__main__':
    icon_base = 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAArElEQVQ4y82SPQrCMBiGH8TWGxSHDopOHZW6eJDewKHH8BTewyt06OSmm6Po1CNUl3cImOYLBcEXXhK+n+dLQuDHmsuDmhqAg9bjmOkJ8JCTMYAKeMtVbNMMyIEN0DqAVrFcNV8qddTeaRpyr9qdD/KKADxV69USuAWar8DCeod1ALCK+QdFAF4Adwuwd/YXTd46ubN1hQbogBqYyLVijdWcAicg8+Qy5VL+Sh/0NzhckWKMBAAAAABJRU5ErkJggg=='
    icon_data = b64decode(icon_base)
    icon_image = Image.open(BytesIO(icon_data))
    root = Tk()
    icon_photo = ImageTk.PhotoImage(icon_image)
    root.iconphoto(True, icon_photo)
    root.wm_title(str(uuid.uuid4())[:8])
    windowWidth = root.winfo_reqwidth()
    windowHeight = root.winfo_reqheight()
    positionRight = int(root.winfo_screenwidth() / 3 - windowWidth / 2)
    positionDown = int(root.winfo_screenheight() / 3 - windowHeight / 2)
    root.geometry(f'500x480+{positionRight}+{positionDown}')
    root.resizable(width=False, height=False)
    app = Window(root)

    def callback(url):
        webbrowser.open_new(url)
    me = Label(root, text='Developer: cyb0rg.exe | GÖK Inc.', fg='#6E7371', cursor='hand2', font='Verdana 7 bold')
    me.pack(side=BOTTOM)
    adres = 'https://www.instagram.com/firatcagrigok/'
    me.bind('<Button-1>', lambda e: callback(adres))
    root.mainloop()