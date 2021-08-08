import PySimpleGUI as sg
import f1
import cv2
from PIL import Image
import active_contour

sg.theme("DarkTeal12")
sg.theme_background_color('light blue')

filtre = ['Sobel', 'Roberts', 'Windowed', 'Unsharp', 'Prewitt_v', 'Prewitt_h', 'Sato', 'Meijering', 'Threshold_otsu', 'Threshold_yen']
uzaysal = ['Radon', 'Swirl', 'Crop']
histogram_list = ['Histogram Eşitleme', 'Histogram Görüntüleme']
morfolojik = ['Opening', 'Closing', 'Erosion', 'Dilation', 'White Tophat', 'Black Tophat', 'Skeletonize', 'Convex Hull', 'Gradient', 'Remove Small Holes']
video_filtre = ['Flip', 'Canny', 'Blur', 'Hue']

layout = [
          [sg.Text("Bir klasör seçin: ", size=(15, 1)), sg.Input(key='-IN-', change_submits=True), sg.FileBrowse()],
          [sg.Image(key='-IMAGE-', enable_events=True)],
          [sg.HorizontalSeparator(color='DarkBlue9')],
          [sg.Text('Görüntü İyileştirme: ', size=(15, 1)), sg.InputCombo(filtre, size=(20, 6), key='-FILTRE-', change_submits=False),
           sg.Button('Uygula', key='-BUTTON-FILTRE-')],
          [sg.HorizontalSeparator(color='DarkBlue9')],
          [sg.Text('Histogram: ', size=(15, 1)), sg.InputCombo(histogram_list, size=(20, 6), key='-HISTO-', change_submits=False),
           sg.Button('Uygula', key='-BUTTON-H-UYGU-')],
          [sg.HorizontalSeparator(color='DarkBlue9')],
          [sg.Text('Uzaysal Dönüşüm: ', size=(15, 1)), sg.InputCombo(uzaysal, size=(20, 6), key='-UZAYSAL-', change_submits=False),
           sg.Button('Uygula', key='-BUTTON-UZAYSAL-'),sg.Text('Döndürme Derecesi: ',size=(15, 1)), sg.Input(key='-DONDUR-', size=(6, 1)),
           sg.Button('Uygula', key='-BUTTON-DONDUR-'), sg.Text('Resize Değerleri: ',size=(15, 1)), sg.Input(key='-A-', size=(6,1)),
           sg.Input(key='-B-', size=(6,1)), sg.Button('Uygula', key='-BUTTON-RESIZE-')],
          [sg.HorizontalSeparator(color='DarkBlue9')],
          [sg.Text('Morfolojik İşlemler: ', size=(15, 1)), sg.InputCombo(morfolojik, size=(20, 6), key='-MORFO-', change_submits=False),
           sg.Button('Uygula', key='-BUTTON-MORFO-')],
          [sg.HorizontalSeparator(color='DarkBlue9')],
          [sg.Text('Yoğunluk Dönüşümü: ', size=(15, 1)), sg.Input(key='-YOG-MIN-', size=(6, 1)), sg.Input(key='-YOG-MAX-', size=(6, 1)),
           sg.Button('Uygula', key='-BUTTON-YOG-')],
          [sg.HorizontalSeparator(color='DarkBlue9')],
          [sg.Text('Active contour: ', size=(15, 1)), sg.Button('Nedir?', key='-BUTTON-ACTI-NE-'),
           sg.Button('Örnek Uygulama', key='-BUTTON-ACTI-ORN-')],
          [sg.HorizontalSeparator(color='DarkBlue9')],
          [sg.Text('Gizemli Filtre:', size=(15, 1)), sg.Button('Uygula', key='-BUTTON-GIZ-')],
          [sg.HorizontalSeparator(color='DarkBlue9')],
          [sg.Text('Bir klasör seçin: ', size=(15, 1)), sg.Input(key="-INVI-", change_submits=True), sg.FileBrowse()],
          [sg.Text('Video İşlemleri: ', size=(15, 1)), sg.InputCombo(video_filtre, size=(20,6), key='-VIDEO-FILTRE-', change_submits=False),
           sg.Button('Uygula', key='-BUTTON-VIDEO-FILTRE-')],
          [sg.Button('Exit', size=(10, 1)), sg.VerticalSeparator(color='DarkBlue9'), sg.Button('Kaydet',size=(10, 1), key='-SAVE-')],
          ]

#Building Window
window = sg.Window("Görüntü İşleme Arayüzü",size=(1000,600),resizable=True).Layout(
        [[sg.Column(layout, size=(1200,900),scrollable=True,justification="c")]])

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Exit':
        break

#image path
    elif event == '-IN-':
        path = values['-IN-']
        image = Image.open(path)
        path = path[:-4] + '_edit.png'
        image.save(path)
        window['-IMAGE-'].update(data = f1.gui_images(path, resize = (450,450)))
        sg.popup("Görünmeyen işlemleri görebilmek için lütfen arayüzü tam sayfa yapınız.",title='Arayüz Boyutu', keep_on_top=True)

#görüntü iyileştirme filtreleri
    elif event == '-BUTTON-FILTRE-':
        if values['-FILTRE-'] == 'Sobel':
            path = f1.sobel_f(path)
            window['-IMAGE-'].update(data = f1.gui_images(path, resize = (450,450)))

        elif values['-FILTRE-'] == 'Roberts':
            path = f1.roberts_f(path)
            window['-IMAGE-'].update(data = f1.gui_images(path, resize = (450,450)))

        elif values['-FILTRE-'] == 'Windowed':
            path = f1.windowed_f(path)
            window['-IMAGE-'].update(data = f1.gui_images(path, resize = (450,450)))

        elif values['-FILTRE-'] == 'Unsharp':
            path = f1.unsharp_f(path)
            window['-IMAGE-'].update(data = f1.gui_images(path, resize = (450,450)))

        elif values['-FILTRE-'] == 'Prewitt_v':
            path = f1.prewitt_v_f(path)
            window['-IMAGE-'].update(data = f1.gui_images(path, resize = (450,450)))

        elif values['-FILTRE-'] == 'Prewitt_h':
            path = f1.prewitt_h_f(path)
            window['-IMAGE-'].update(data = f1.gui_images(path, resize = (450,450)))

        elif values['-FILTRE-'] == 'Sato':
            path = f1.sato_f(path)
            window['-IMAGE-'].update(data = f1.gui_images(path, resize = (450,450)))

        elif values['-FILTRE-'] == 'Meijering':
            path = f1.meijering_f(path)
            window['-IMAGE-'].update(data = f1.gui_images(path, resize = (450,450)))

        elif values['-FILTRE-'] == 'Threshold_otsu':
            path = f1.threshold_otsu_f(path)
            window['-IMAGE-'].update(data = f1.gui_images(path, resize = (450,450)))

        elif values['-FILTRE-'] == 'Threshold_yen':
            path = f1.threshold_yen_f(path)
            window['-IMAGE-'].update(data = f1.gui_images(path, resize = (450,450)))


#histogram
    elif event == '-BUTTON-H-UYGU-':
        if values['-HISTO-'] == 'Histogram Eşitleme':
            path, histo = f1.hist_equalize(path)
            window['-IMAGE-'].update(data=f1.gui_images(path, resize=(450, 450)))

        elif values['-HISTO-'] == 'Histogram Görüntüleme':
            f1.show_histo(path, histo)

#uzaysal dönüşüm
    elif event == '-BUTTON-UZAYSAL-':
        if values['-UZAYSAL-'] == 'Radon':
            path = f1.radon_u(path)
            window['-IMAGE-'].update(data = f1.gui_images(path, resize = (450,450)))

        elif values['-UZAYSAL-'] == 'Swirl':
            path = f1.swirl_u(path)
            window['-IMAGE-'].update(data = f1.gui_images(path, resize = (450,450)))

        elif values['-UZAYSAL-'] == 'Crop':
            path = f1.crop_u(path)
            window['-IMAGE-'].update(data=f1.gui_images(path, resize=(450, 450)))

#uzaysal dönüşüm döndürme
    elif event == '-BUTTON-DONDUR-':
        dondurme = values['-DONDUR-']
        path = f1.rotate_u(path, dondurme)
        window['-IMAGE-'].update(data = f1.gui_images(path, resize = (450,450)))


#uzaysal dönüşüm resize
    elif event == '-BUTTON-RESIZE-':
        a = values['-A-']
        b = values['-B-']
        path = f1.resize_u(path, a, b)
        window['-IMAGE-'].update(data = f1.gui_images(path, resize= (int(a), int(b))))


#morfolojik işlemler
    elif event == '-BUTTON-MORFO-':
        if values['-MORFO-'] == 'Opening':
            path = f1.opening_m(path)
            window['-IMAGE-'].update(data = f1.gui_images(path, resize = (450,450)))

        elif values['-MORFO-'] == 'Closing':
            path = f1.closing_m(path)
            window['-IMAGE-'].update(data = f1.gui_images(path, resize = (450,450)))

        elif values['-MORFO-'] == 'Erosion':
            path = f1.erosion_m(path)
            window['-IMAGE-'].update(data = f1.gui_images(path, resize = (450,450)))

        elif values['-MORFO-'] == 'Dilation':
            path = f1.dilation_m(path)
            window['-IMAGE-'].update(data=f1.gui_images(path, resize=(450, 450)))

        elif values['-MORFO-'] == 'White Tophat':
            path = f1.white_tophat_m(path)
            window['-IMAGE-'].update(data = f1.gui_images(path, resize = (450,450)))

        elif values['-MORFO-'] == 'Black Tophat':
            path = f1.black_tophat_m(path)
            window['-IMAGE-'].update(data = f1.gui_images(path, resize = (450,450)))

        elif values['-MORFO-'] == 'Skeletonize':
            path = f1.skeletonize_m(path)
            window['-IMAGE-'].update(data = f1.gui_images(path, resize = (450,450)))

        elif values['-MORFO-'] == 'Convex Hull':
            path = f1.convex_hull_m(path)
            window['-IMAGE-'].update(data = f1.gui_images(path, resize = (450,450)))

        elif values['-MORFO-'] == 'Gradient':
            path = f1.gradient_m(path)
            window['-IMAGE-'].update(data = f1.gui_images(path, resize = (450,450)))

        elif values['-MORFO-'] == 'Remove Small Holes':
            path = f1.remove_small_holes_m(path)
            window['-IMAGE-'].update(data = f1.gui_images(path, resize = (450,450)))

#yoğunluk dönüşümü
    elif event == '-BUTTON-YOG-':
        min_yog = values['-YOG-MIN-']
        max_yog = values['-YOG-MAX-']
        path = f1.rescale_y(path, min_yog, max_yog)
        window['-IMAGE-'].update(data = f1.gui_images(path, resize = (450,450)))

#active contour
    elif event == '-BUTTON-ACTI-NE-':
        my_text = 'Yılan olarak da adlandırılan aktif kontur modeli, Michael Kass, Andrew Witkin ve Demetri Terzopoulos tarafından gürültülü bir 2D görüntüden bir nesne taslağını tanımlamak için tanıtılan bir bilgisayar görüşü çerçevesidir. Yılan modeli bilgisayarla görmede popülerdir ve yılanlar, nesne izleme, şekil tanıma, bölümleme, kenar algılama ve stereo eşleştirme gibi uygulamalarda yaygın olarak kullanılmaktadır.'
        sg.popup_scrolled(my_text, title='Actieve Contour Nedir?', keep_on_top=True)

    elif event == '-BUTTON-ACTI-ORN-':
        active_contour.örnek()

#gizemli filtre
    elif event == '-BUTTON-GIZ-':
        path = f1.gizem_f(path)
        window['-IMAGE-'].update(data = f1.gui_images(path, resize = (450,450)))

#save
    elif event == '-SAVE-':
        sg.popup("Başarıyla kaydedilmiştir.",title='Save', keep_on_top=True)

#video path
    elif event == '-INVI-':
        path_video = values ['-INVI-']
        path_video_new = path_video[:-4] + '_edit.mp4'

#video filtreleme
    elif event == '-BUTTON-VIDEO-FILTRE-':

        cap = cv2.VideoCapture(path_video)
        # Define the codec, frame height, frame weight, fps and create VideoWriter object
        fw = int(cap.get(3))
        fh = int(cap.get(4))
        fps = cap.get(cv2.CAP_PROP_FPS)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')

        if values['-VIDEO-FILTRE-'] == 'Canny':
            f1.canny_v(path_video_new, fourcc, fps, fw, fh, cap)

        elif values['-VIDEO-FILTRE-'] == 'Flip':
            f1.flip_v(path_video_new, fourcc, fps, fw, fh, cap)

        elif values['-VIDEO-FILTRE-'] == 'Blur':
            f1.blur_v(path_video_new, fourcc, fps, fw, fh, cap)

        elif values['-VIDEO-FILTRE-'] == 'Hue':
            f1.hue_v(path_video_new, fourcc, fps, fw, fh, cap)