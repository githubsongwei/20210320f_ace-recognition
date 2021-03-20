# -*- coding: utf-8 -*-
import face_recognition
import cv2
import time


def Collect_faces(username, cursor):
    # 调用笔记本内置摄像头，所以参数为0，如果有其他的摄像头可以调整参数为1，2
    cap = cv2.VideoCapture(0)
    face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    print('\n Initializing face capture. Look at the camera and wait ...')
    count = 0
    while True:
        # 从摄像头读取图片
        sucess, img = cap.read()
        cv2.imshow('image', img)
        # 转为灰度图片
        # 检测人脸
        faces = face_detector.detectMultiScale(img, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + w), (255, 0, 0))
            count += 1
            # 保存图像,从原始照片中截取人脸尺寸
            img_name = username + '.' + str(count) + '.jpg'
            path_name = "Facedata/" + username + '.' + str(count) + '.jpg'
            cv2.imwrite(path_name, img[y: y + h, x: x + w, :])
            cv2.imshow('image', img)
            cursor.execute("insert into Path values ('%s', '%s');" % (img_name, path_name))
        # 保持画面的持续。
        time.sleep(1)
        k = cv2.waitKey(1)
        if k == 27:  # 通过esc键退出摄像
            break
        elif count >= 10:  # 得到10个样本后退出摄像
            break
    # 关闭摄像头
    cap.release()
    cv2.destroyAllWindows()


def recognize_face(cursor):  # cursor:数据库游标
    known_names = []
    known_encodings = []
    # 数据库读取路径
    cursor.execute("Select * from Path;")
    rows = cursor.fetchall()
    for item in rows:
        load_image = face_recognition.load_image_file(item[1])  # 加载图片
        image_face_encoding = face_recognition.face_encodings(load_image)
        if len(image_face_encoding) != 0:
            known_names.append(item[0].split('.')[0])
            image_face_encoding = image_face_encoding[0]  # 获得128维特征值
            known_encodings.append(image_face_encoding)

    # 打开摄像头，0表示内置摄像头
    video_capture = cv2.VideoCapture(0)
    process_this_frame = True
    time = 0
    result = 'unknown'
    while True:
        time += 1
        ret, frame = video_capture.read()
        # opencv的图像是BGR格式的，而我们需要是的RGB格式的，因此需要进行一个转换。
        rgb_frame = frame[:, :, ::-1]
        face_locations = ''
        face_names = []  # 存储出现在画面中人脸的名字
        if process_this_frame:
            face_locations = face_recognition.face_locations(rgb_frame)  # 获得所有人脸位置
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)  # 获得人脸特征值
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.5)
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_names[first_match_index]
                else:
                    name = "unknown"
                face_names.append(name)

        process_this_frame = not process_this_frame
        # 将捕捉到的人脸显示出来
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, name, (left + 5, top - 5), font, 1.5, (0, 0, 255), 3)
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            if name in known_names:
                result = name
            else:
                result = 'unknown'
            cv2.imshow('camera', frame)  # 弹出摄像头与否
        k = cv2.waitKey(1)
        if k == 27:
            break
        elif time > 30:
            break
    video_capture.release()
    cv2.destroyAllWindows()
    return result  # 返回识别结果：人名或“unknown”
