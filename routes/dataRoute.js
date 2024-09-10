const {extractTag} = require('../controller/getDataOnKeyWord')
const express = require('express')
const router = express.Router()

router.post('/',extractTag);

module.exports = {
    router
}