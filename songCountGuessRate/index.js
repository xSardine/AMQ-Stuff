const express = require('express')
const cors = require('cors')
const sqlite3 = require('sqlite3').verbose()

const app = express()

const db = new sqlite3.Database('./songs.sqlite3')

const HTTP_PORT = 8010

app.use(cors())

app.use(express.json())

db.run(`
    CREATE TABLE IF NOT EXISTS Songs (
        song TEXT,
        artist TEXT,
        lastTimePlayed INTEGER,
        playCount INTEGER,
        correctCount INTEGER,
        specPlayCount INTEGER,
        UNIQUE("song","artist")
)`)

app.post('/songrec', (req, res) => {
    console.log('POST /songrec')
    console.dir(req.body)

    let response = {
        success: true,
        inDatabase: false,
        lastTimePlayed: 0,
        playCount: 0,
        correctCount: 0,
        specPlayCount: 0
    }

    db.serialize(() => {
        console.log('db.get (annid)')

        let sql = `
            SELECT *
            FROM Songs
            WHERE LOWER(song) = LOWER(?)
            AND LOWER(artist) = LOWER(?)
        `

        let params = [
            req.body.songName,
            req.body.artist,
        ]

        db.get(sql, params, (err, row) => {

            if (err) {
                console.log(err)
                response.success = false
                res.send(response)
                return
            }

            if (row) {
                console.log('song found')
                console.dir(row)

                response.inDatabase = true
                response.lastTimePlayed = row.lastTimePlayed
                response.playCount = row.playCount
                response.correctCount = row.correctCount
                response.specPlayCount = row.specPlayCount
                console.dir(response)
                res.send(response)

                return
            }

            res.send(response)
        })

        sql = `
            INSERT INTO Songs
            VALUES (?,?,?,?,?,?)
            ON CONFLICT (song, artist)
            DO UPDATE SET   song=excluded.song,
                            artist=excluded.artist,
                            playCount=playCount+excluded.playCount,
                            correctCount=correctCount+excluded.correctCount,
                            specPlayCount=specPlayCount+excluded.specPlayCount,
                            lastTimePlayed=excluded.lastTimePlayed
        `

        let correctIncrement = 0
        let countIncrement = 0
        let specIncrement = 0

        if (req.body.isSpectator) {
            specIncrement = 1
        }
        else {
            countIncrement = 1
            if (req.body.isCorrect) {
                correctIncrement = 1
            }
        }

        params = [
            req.body.songName,
            req.body.artist,
            Date.now(),
            countIncrement,
            correctIncrement,
            specIncrement
        ]

        db.run(sql, params, (err) => {
            if (err) console.log(err)
            console.log('db.run: added or updated row')
            console.log(params)
        })
    })
})
app.listen(HTTP_PORT, () => {
    console.log('HTTP Server listening to port ' + HTTP_PORT)
})