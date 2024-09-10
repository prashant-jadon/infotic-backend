const express = require('express')
const app = express()
const {router} = require('./routes/dataRoute')

app.listen(3000,()=>{
    console.log('port started');
})


app.use(express.json())
app.use('/data',router);

