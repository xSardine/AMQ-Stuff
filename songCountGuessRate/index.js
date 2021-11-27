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
        annid INTEGER,
        anime TEXT,
        animeEnglish TEXT,
        song TEXT,
        artist TEXT,
        type INTEGER,
        typenumber INTEGER,
        catbox720 TEXT,
        catbox480 TEXT,
        catboxmp3 TEXT,
        timestamp INTEGER,
        count INTEGER,
        correctcount INTEGER,
        othercount INTEGER,
        UNIQUE("song","artist")
)`)

app.post('/songrec', (req, res) => {
    console.log('POST /songrec')
    console.dir(req.body)

    let response = {
        success: true,
        inDatabase: false,
        songInfo: null,
        lastPlayed: 0,
        playCount: 0,
        correctcount: 0,
        othercount: 0
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
                console.log('found by annid')
                console.dir(row)

                response.inDatabase = true
                response.songInfo = row
                response.lastPlayed = row.timestamp
                response.playCount = row.count
                response.correctcount = row.correctcount
                response.othercount = row.othercount
                console.dir(response)
                res.send(response)

                return
            }

            res.send(response)
        })

        sql = `
            INSERT INTO Songs
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            ON CONFLICT (song, artist)
            DO UPDATE SET   annid=excluded.annid,
                            anime=excluded.anime,
                            animeEnglish=excluded.animeEnglish,
                            song=excluded.song,
                            artist=excluded.artist,
                            catbox720=excluded.catbox720,
                            catbox480=excluded.catbox480,
                            catboxmp3=excluded.catboxmp3,
                            count=count+excluded.count,
                            correctcount=correctcount+excluded.correctcount,
                            othercount=othercount+excluded.othercount,
                            timestamp=excluded.timestamp
        `

        let links = [null, null, null]

        if (req.body.urlMap.hasOwnProperty('catbox')) {
            links = [
                req.body.urlMap.catbox['720'] || null,
                req.body.urlMap.catbox['480'] || null,
                req.body.urlMap.catbox['0'] || null
            ]
        }

        let correctIncrement = 0
        let countIncrement = 0
        let otherIncrement = 0
        if (req.body.isCorrect) {
            correctIncrement = 1
        }

        if (req.body.isSpectator) {
            otherIncrement = 1
        }
        else {
            countIncrement = 1
        }

        params = [
            req.body.annId,
            req.body.animeNames.romaji,
            req.body.animeNames.english,
            req.body.songName,
            req.body.artist,
            req.body.type,
            req.body.typeNumber,
            ...links,
            Date.now(),
            countIncrement,
            correctIncrement,
            otherIncrement
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