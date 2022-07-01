from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import os
import easyocr

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api_uri")
def get_api_uri():
    return {"API URI": "/ocr_api", "Demo URI": "/test_json"}


@app.get("/test_json")
def get_demo_test_json():
    jdict = [{
            "x1": 312,
            "y1": 65,
            "x2": 976,
            "y2": 140,
            "eye_sight": "0.3",
            "text": "자가 시력 축정 시스템 사용법",
            "confidence": "0.5846381449443497"
        },
        {
            "x1": 94,
            "y1": 228,
            "x2": 124,
            "y2": 262,
            "eye_sight": "0.8",
            "text": "1.",
            "confidence": "0.77092670993224"
        },
        {
            "x1": 143,
            "y1": 223,
            "x2": 295,
            "y2": 267,
            "eye_sight": "0.6",
            "text": "Pycharm",
            "confidence": "0.9850412764080322"
        },
        {
            "x1": 584,
            "y1": 218,
            "x2": 851,
            "y2": 271,
            "eye_sight": "0.5",
            "text": "python mainpy",
            "confidence": "0.8683678661663818"
        },
        {
            "x1": 971,
            "y1": 223,
            "x2": 1075,
            "y2": 265,
            "eye_sight": "0.6",
            "text": "Enter",
            "confidence": "0.9975331647626222"
        },
        {
            "x1": 493,
            "y1": 279,
            "x2": 563,
            "y2": 323,
            "eye_sight": "0.6",
            "text": "번호",
            "confidence": "0.9998904199524544"
        },
        {
            "x1": 478,
            "y1": 334,
            "x2": 594,
            "y2": 366,
            "eye_sight": "0.8",
            "text": "글자 인식률",
            "confidence": "0.8770995574533583"
        },
        {
            "x1": 337,
            "y1": 377,
            "x2": 509,
            "y2": 421,
            "eye_sight": "0.6",
            "text": "결과 이미지",
            "confidence": "0.9998432431602375"
        },
        {
            "x1": 472,
            "y1": 428,
            "x2": 576,
            "y2": 456,
            "eye_sight": "0.9",
            "text": "작업표시출",
            "confidence": "0.6023921408632577"
        }]
    return jdict


@app.post("/ocr_api")
async def ocr_api(files: List[UploadFile] = File(...)):
    for file in files:
        contents = await file.read()
        with open(os.path.join("./", file.filename), "wb") as fp:
            fp.write(contents)

        reader = easyocr.Reader(['ko', 'en'], gpu=False)
        bounds = reader.readtext(file.filename)
        bounding_boxes = []

        for bound in bounds:
            top_left = tuple(bound[0][0])
            bottom_right = tuple(bound[0][2])
            text = str(bound[1])
            conf = str(bound[2])
            n_pixel = min(bottom_right[1] - top_left[1], bottom_right[0] - top_left[0])
            eye_sight = str(round(25 / n_pixel, 1))

            bbox = {'x1': int(top_left[0]), 'y1': int(top_left[1]), 'x2': int(bottom_right[0]),
                    'y2': int(bottom_right[1]), 'eye_sight': eye_sight, 'text': text, 'confidence': conf}

            bounding_boxes.append(bbox)

    return bounding_boxes
