//app.js
const express = require('express') //express 모듈을 가져온다
const app = express() //가져온 express 모듈의 function을 이용해서 새로운 express 앱을 만든다
const port = 3000 

const fs = require('fs');

app.get('/', (req, res) => {
    const filePath = 'log/detected_log.txt'; //log파일 읽기
    fs.readFile(filePath, 'utf8', (err, data) => {
        if (err) {
            console.error(err);
            return res.status(500).send('Error reading file'); // log파일을 읽지 못할 경우, 서버 스크립트 오류에 사용되는 500 에러 반환
        }
            res.send(data); //log 출력
        });
    });

app.listen(port, () => {
    console.log(`app listening at http://localhost:${port}`)
}) //포트 3000번에서 앱을 실행한다